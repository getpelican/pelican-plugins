"""i18n_subsites plugin creates i18n-ized subsites of the default site

This plugin is designed for Pelican 3.4 and later
"""


import os
import six
import logging
import posixpath

from copy import copy
from itertools import chain
from operator import attrgetter
from collections import OrderedDict
from contextlib import contextmanager
from six.moves.urllib.parse import urlparse

import gettext
import locale

from pelican import signals
from pelican.generators import ArticlesGenerator, PagesGenerator
from pelican.settings import configure_settings
from pelican.contents import Draft


# Global vars
_MAIN_SETTINGS = None     # settings dict of the main Pelican instance
_MAIN_LANG = None         # lang of the main Pelican instance
_MAIN_SITEURL = None      # siteurl of the main Pelican instance
_MAIN_STATIC_FILES = None # list of Static instances the main Pelican instance
_SUBSITE_QUEUE = {}   # map: lang -> settings overrides
_SITE_DB = OrderedDict()           # OrderedDict: lang -> siteurl
_SITES_RELPATH_DB = {}       # map: (lang, base_lang) -> relpath
# map: generator -> list of removed contents that need interlinking
_GENERATOR_DB = {}
_NATIVE_CONTENT_URL_DB = {} # map: source_path -> content in its native lang
_LOGGER = logging.getLogger(__name__)


@contextmanager
def temporary_locale(temp_locale=None):
    '''Enable code to run in a context with a temporary locale

    Resets the locale back when exiting context.
    Can set a temporary locale if provided
    '''
    orig_locale = locale.setlocale(locale.LC_ALL)
    if temp_locale is not None:
        locale.setlocale(locale.LC_ALL, temp_locale)
    yield
    locale.setlocale(locale.LC_ALL, orig_locale)


def initialize_dbs(settings):
    '''Initialize internal DBs using the Pelican settings dict

    This clears the DBs for e.g. autoreload mode to work
    '''
    global _MAIN_SETTINGS, _MAIN_SITEURL, _MAIN_LANG, _SUBSITE_QUEUE
    _MAIN_SETTINGS = settings
    _MAIN_LANG = settings['DEFAULT_LANG']
    _MAIN_SITEURL = settings['SITEURL']
    _SUBSITE_QUEUE = settings.get('I18N_SUBSITES', {}).copy()
    prepare_site_db_and_overrides()
    # clear databases in case of autoreload mode
    _SITES_RELPATH_DB.clear()
    _NATIVE_CONTENT_URL_DB.clear()
    _GENERATOR_DB.clear()


def prepare_site_db_and_overrides():
    '''Prepare overrides and create _SITE_DB

    _SITE_DB.keys() need to be ready for filter_translations
    '''
    _SITE_DB.clear()
    _SITE_DB[_MAIN_LANG] = _MAIN_SITEURL
    # make sure it works for both root-relative and absolute
    main_siteurl = '/' if _MAIN_SITEURL == '' else _MAIN_SITEURL
    for lang, overrides in _SUBSITE_QUEUE.items():
        if 'SITEURL' not in overrides:
            overrides['SITEURL'] = posixpath.join(main_siteurl, lang)
        _SITE_DB[lang] = overrides['SITEURL']
        # default subsite hierarchy
        if 'OUTPUT_PATH' not in overrides:
            overrides['OUTPUT_PATH'] = os.path.join(
                _MAIN_SETTINGS['OUTPUT_PATH'], lang)
        if 'CACHE_PATH' not in overrides:
            overrides['CACHE_PATH'] = os.path.join(
                _MAIN_SETTINGS['CACHE_PATH'], lang)
        if 'STATIC_PATHS' not in overrides:
            overrides['STATIC_PATHS'] = []
        if ('THEME' not in overrides and 'THEME_STATIC_DIR' not in overrides and
                'THEME_STATIC_PATHS' not in overrides):
            relpath = relpath_to_site(lang, _MAIN_LANG)
            overrides['THEME_STATIC_DIR'] = posixpath.join(
                relpath, _MAIN_SETTINGS['THEME_STATIC_DIR'])
            overrides['THEME_STATIC_PATHS'] = []
        # to change what is perceived as translations
        overrides['DEFAULT_LANG'] = lang


def subscribe_filter_to_signals(settings):
    '''Subscribe content filter to requested signals'''
    for sig in settings.get('I18N_FILTER_SIGNALS', []):
        sig.connect(filter_contents_translations)


def initialize_plugin(pelican_obj):
    '''Initialize plugin variables and Pelican settings'''
    if _MAIN_SETTINGS is None:
        initialize_dbs(pelican_obj.settings)
        subscribe_filter_to_signals(pelican_obj.settings)


def get_site_path(url):
    '''Get the path component of an url, excludes siteurl

    also normalizes '' to '/' for relpath to work,
    otherwise it could be interpreted as a relative filesystem path
    '''
    path = urlparse(url).path
    if path == '':
        path = '/'
    return path


def relpath_to_site(lang, target_lang):
    '''Get relative path from siteurl of lang to siteurl of base_lang

    the output is cached in _SITES_RELPATH_DB
    '''
    path = _SITES_RELPATH_DB.get((lang, target_lang), None)
    if path is None:
        siteurl = _SITE_DB.get(lang, _MAIN_SITEURL)
        target_siteurl = _SITE_DB.get(target_lang, _MAIN_SITEURL)
        path = posixpath.relpath(get_site_path(target_siteurl),
                                 get_site_path(siteurl))
        _SITES_RELPATH_DB[(lang, target_lang)] = path
    return path


def save_generator(generator):
    '''Save the generator for later use

    initialize the removed content list
    '''
    _GENERATOR_DB[generator] = []


def article2draft(article):
    '''Transform an Article to Draft'''
    draft = Draft(article._content, article.metadata, article.settings,
                  article.source_path, article._context)
    draft.status = 'draft'
    return draft


def page2hidden_page(page):
    '''Transform a Page to a hidden Page'''
    page.status = 'hidden'
    return page


class GeneratorInspector(object):
    '''Inspector of generator instances'''

    generators_info = {
        ArticlesGenerator: {
            'translations_lists': ['translations', 'drafts_translations'],
            'contents_lists': [('articles', 'drafts')],
            'hiding_func': article2draft,
            'policy': 'I18N_UNTRANSLATED_ARTICLES',
        },
        PagesGenerator: {
            'translations_lists': ['translations', 'hidden_translations'],
            'contents_lists': [('pages', 'hidden_pages')],
            'hiding_func': page2hidden_page,
            'policy': 'I18N_UNTRANSLATED_PAGES',
        },
    }

    def __init__(self, generator):
        '''Identify the best known class of the generator instance

        The class '''
        self.generator = generator
        self.generators_info.update(generator.settings.get(
            'I18N_GENERATORS_INFO', {}))
        for cls in generator.__class__.__mro__:
            if cls in self.generators_info:
                self.info = self.generators_info[cls]
                break
        else:
            self.info = {}

    def translations_lists(self):
        '''Iterator over lists of content translations'''
        return (getattr(self.generator, name) for name in
                self.info.get('translations_lists', []))

    def contents_list_pairs(self):
        '''Iterator over pairs of normal and hidden contents'''
        return (tuple(getattr(self.generator, name) for name in names)
                for names in self.info.get('contents_lists', []))

    def hiding_function(self):
        '''Function for transforming content to a hidden version'''
        hiding_func = self.info.get('hiding_func', lambda x: x)
        return hiding_func

    def untranslated_policy(self, default):
        '''Get the policy for untranslated content'''
        return self.generator.settings.get(self.info.get('policy', None),
                                           default)

    def all_contents(self):
        '''Iterator over all contents'''
        translations_iterator = chain(*self.translations_lists())
        return chain(translations_iterator,
                     *(pair[i] for pair in self.contents_list_pairs()
                       for i in (0, 1)))


def filter_contents_translations(generator):
    '''Filter the content and translations lists of a generator

    Filters out
        1) translations which will be generated in a different site
        2) content that is not in the language of the currently
        generated site but in that of a different site, content in a
        language which has no site is generated always. The filtering
        method bay be modified by the respective untranslated policy
    '''
    inspector = GeneratorInspector(generator)
    current_lang = generator.settings['DEFAULT_LANG']
    langs_with_sites = _SITE_DB.keys()
    removed_contents = _GENERATOR_DB[generator]

    for translations in inspector.translations_lists():
        for translation in translations[:]:    # copy to be able to remove
            if translation.lang in langs_with_sites:
                translations.remove(translation)
                removed_contents.append(translation)

    hiding_func = inspector.hiding_function()
    untrans_policy = inspector.untranslated_policy(default='hide')
    for (contents, other_contents) in inspector.contents_list_pairs():
        for content in other_contents: # save any hidden native content first
            if content.lang == current_lang: # in native lang
                # save the native URL attr formatted in the current locale
                _NATIVE_CONTENT_URL_DB[content.source_path] = content.url
        for content in contents[:]:        # copy for removing in loop
            if content.lang == current_lang: # in native lang
                # save the native URL attr formatted in the current locale
                _NATIVE_CONTENT_URL_DB[content.source_path] = content.url
            elif content.lang in langs_with_sites and untrans_policy != 'keep':
                contents.remove(content)
                if untrans_policy == 'hide':
                    other_contents.append(hiding_func(content))
                elif untrans_policy == 'remove':
                    removed_contents.append(content)


def install_templates_translations(generator):
    '''Install gettext translations in the jinja2.Environment

    Only if the 'jinja2.ext.i18n' jinja2 extension is enabled
    the translations for the current DEFAULT_LANG are installed.
    '''
    if 'jinja2.ext.i18n' in generator.settings['JINJA_EXTENSIONS']:
        domain = generator.settings.get('I18N_GETTEXT_DOMAIN', 'messages')
        localedir = generator.settings.get('I18N_GETTEXT_LOCALEDIR')
        if localedir is None:
            localedir = os.path.join(generator.theme, 'translations')
        current_lang = generator.settings['DEFAULT_LANG']
        if current_lang == generator.settings.get('I18N_TEMPLATES_LANG',
                                                  _MAIN_LANG):
            translations = gettext.NullTranslations()
        else:
            langs = [current_lang]
            try:
                translations = gettext.translation(domain, localedir, langs)
            except (IOError, OSError):
                _LOGGER.error((
                    "Cannot find translations for language '{}' in '{}' with "
                    "domain '{}'. Installing NullTranslations.").format(
                        langs[0], localedir, domain))
                translations = gettext.NullTranslations()
        newstyle = generator.settings.get('I18N_GETTEXT_NEWSTYLE', True)
        generator.env.install_gettext_translations(translations, newstyle)


def add_variables_to_context(generator):
    '''Adds useful iterable variables to template context'''
    context = generator.context             # minimize attr lookup
    context['relpath_to_site'] = relpath_to_site
    context['main_siteurl'] = _MAIN_SITEURL
    context['main_lang'] = _MAIN_LANG
    context['lang_siteurls'] = _SITE_DB
    current_lang = generator.settings['DEFAULT_LANG']
    extra_siteurls = _SITE_DB.copy()
    extra_siteurls.pop(current_lang)
    context['extra_siteurls'] = extra_siteurls


def interlink_translations(content):
    '''Link content to translations in their main language

    so the URL (including localized month names) of the different subsites
    will be honored
    '''
    lang = content.lang
    # sort translations by lang
    content.translations.sort(key=attrgetter('lang'))
    for translation in content.translations:
        relpath = relpath_to_site(lang, translation.lang)
        url = _NATIVE_CONTENT_URL_DB[translation.source_path]
        translation.override_url = posixpath.join(relpath, url)


def interlink_translated_content(generator):
    '''Make translations link to the native locations

    for generators that may contain translated content
    '''
    inspector = GeneratorInspector(generator)
    for content in inspector.all_contents():
        interlink_translations(content)


def interlink_removed_content(generator):
    '''For all contents removed from generation queue update interlinks

    link to the native location
    '''
    current_lang = generator.settings['DEFAULT_LANG']
    for content in _GENERATOR_DB[generator]:
        url = _NATIVE_CONTENT_URL_DB[content.source_path]
        relpath = relpath_to_site(current_lang, content.lang)
        content.override_url = posixpath.join(relpath, url)


def interlink_static_files(generator):
    '''Add links to static files in the main site if necessary'''
    if generator.settings['STATIC_PATHS'] != []:
        return                               # customized STATIC_PATHS
    filenames = generator.context['filenames'] # minimize attr lookup
    relpath = relpath_to_site(generator.settings['DEFAULT_LANG'], _MAIN_LANG)
    for staticfile in _MAIN_STATIC_FILES:
        if staticfile.get_relative_source_path() not in filenames:
            staticfile = copy(staticfile) # prevent override in main site
            staticfile.override_url = posixpath.join(relpath, staticfile.url)
            generator.add_source_path(staticfile)


def save_main_static_files(static_generator):
    '''Save the static files generated for the main site'''
    global _MAIN_STATIC_FILES
    # test just for current lang as settings change in autoreload mode
    if static_generator.settings['DEFAULT_LANG'] == _MAIN_LANG:
        _MAIN_STATIC_FILES = static_generator.staticfiles


def update_generators():
    '''Update the context of all generators

    Ads useful variables and translations into the template context
    and interlink translations
    '''
    for generator in _GENERATOR_DB.keys():
        install_templates_translations(generator)
        add_variables_to_context(generator)
        interlink_static_files(generator)
        interlink_removed_content(generator)
        interlink_translated_content(generator)


def get_pelican_cls(settings):
    '''Get the Pelican class requested in settings'''
    cls = settings['PELICAN_CLASS']
    if isinstance(cls, six.string_types):
        module, cls_name = cls.rsplit('.', 1)
        module = __import__(module)
        cls = getattr(module, cls_name)
    return cls


def create_next_subsite(pelican_obj):
    '''Create the next subsite using the lang-specific config

    If there are no more subsites in the generation queue, update all
    the generators (interlink translations and removed content, add
    variables and translations to template context). Otherwise get the
    language and overrides for next the subsite in the queue and apply
    overrides.  Then generate the subsite using a PELICAN_CLASS
    instance and its run method. Finally, restore the previous locale.
    '''
    global _MAIN_SETTINGS
    if len(_SUBSITE_QUEUE) == 0:
        _LOGGER.debug(
            'i18n: Updating cross-site links and context of all generators.')
        update_generators()
        _MAIN_SETTINGS = None             # to initialize next time
    else:
        with temporary_locale():
            settings = _MAIN_SETTINGS.copy()
            lang, overrides = _SUBSITE_QUEUE.popitem()
            settings.update(overrides)
            settings = configure_settings(settings)      # to set LOCALE, etc.
            cls = get_pelican_cls(settings)

            new_pelican_obj = cls(settings)
            _LOGGER.debug(("Generating i18n subsite for language '{}' "
                           "using class {}").format(lang, cls))
            new_pelican_obj.run()


# map: signal name -> function name
_SIGNAL_HANDLERS_DB = {
    'get_generators': initialize_plugin,
    'article_generator_pretaxonomy': filter_contents_translations,
    'page_generator_finalized': filter_contents_translations,
    'get_writer': create_next_subsite,
    'static_generator_finalized': save_main_static_files,
    'generator_init': save_generator,
}


def register():
    '''Register the plugin only if required signals are available'''
    for sig_name in _SIGNAL_HANDLERS_DB.keys():
        if not hasattr(signals, sig_name):
            _LOGGER.error((
                'The i18n_subsites plugin requires the {} '
                'signal available for sure in Pelican 3.4.0 and later, '
                'plugin will not be used.').format(sig_name))
            return

    for sig_name, handler in _SIGNAL_HANDLERS_DB.items():
        sig = getattr(signals, sig_name)
        sig.connect(handler)
