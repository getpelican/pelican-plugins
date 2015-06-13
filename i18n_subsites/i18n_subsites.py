"""i18n_subsites plugin creates i18n-ized subsites of the default site"""



import os
import six
import logging
from itertools import chain
from collections import defaultdict, OrderedDict

import gettext

from pelican import signals
from pelican.contents import Page, Article
from pelican.settings import configure_settings

from ._regenerate_context_helpers import regenerate_context_articles



# Global vars
_main_site_generated = False
_main_site_lang = "en"
_main_siteurl = ''
_lang_siteurls = None
logger = logging.getLogger(__name__)



def disable_lang_vars(pelican_obj):
    """Set lang specific url and save_as vars to the non-lang defaults

    e.g. ARTICLE_LANG_URL = ARTICLE_URL
    They would conflict with this plugin otherwise
    """
    global _main_site_lang, _main_siteurl, _lang_siteurls
    s = pelican_obj.settings
    for content in ['ARTICLE', 'PAGE']:
        for meta in ['_URL', '_SAVE_AS']:
            s[content + '_LANG' + meta] = s[content + meta]
    if not _main_site_generated:
        _main_site_lang = s['DEFAULT_LANG']
        _main_siteurl = s['SITEURL']
        _lang_siteurls = [(lang, _main_siteurl + '/' + lang) for lang in s.get('I18N_SUBSITES', {}).keys()]
        # To be able to use url for main site root when SITEURL == '' (e.g. when developing)
        _lang_siteurls = [(_main_site_lang, ('/' if _main_siteurl == '' else _main_siteurl))] + _lang_siteurls
        _lang_siteurls = OrderedDict(_lang_siteurls)
        

    
def create_lang_subsites(pelican_obj):
    """For each language create a subsite using the lang-specific config

    for each generated lang append language subpath to SITEURL and OUTPUT_PATH
    and set DEFAULT_LANG to the language code to change perception of what is translated
    and set DELETE_OUTPUT_DIRECTORY to False to prevent deleting output from previous runs
    Then generate the subsite using a PELICAN_CLASS instance and its run method.
    """
    global _main_site_generated
    if _main_site_generated:      # make sure this is only called once
        return
    else:
        _main_site_generated = True

    orig_settings = pelican_obj.settings
    for lang, overrides in orig_settings.get('I18N_SUBSITES', {}).items():
        settings = orig_settings.copy()
        settings.update(overrides)
        settings['SITEURL'] = _lang_siteurls[lang]
        settings['OUTPUT_PATH'] = os.path.join(orig_settings['OUTPUT_PATH'], lang, '')
        settings['DEFAULT_LANG'] = lang   # to change what is perceived as translations
        settings['DELETE_OUTPUT_DIRECTORY'] = False  # prevent deletion of previous runs
        settings = configure_settings(settings)      # to set LOCALE, etc.

        cls = settings['PELICAN_CLASS']
        if isinstance(cls, six.string_types):
            module, cls_name = cls.rsplit('.', 1)
            module = __import__(module)
            cls = getattr(module, cls_name)

        pelican_obj = cls(settings)
        logger.debug("Generating i18n subsite for lang '{}' using class '{}'".format(lang, str(cls)))
        pelican_obj.run()
    _main_site_generated = False          # for autoreload mode



def move_translations_links(content_object):
    """This function points translations links to the sub-sites

    by prepending their location with the language code
    or directs an original DEFAULT_LANG translation back to top level site
    """
    for translation in content_object.translations:
        if translation.lang == _main_site_lang:
        # cannot prepend, must take to top level
            lang_prepend = '../'
        else:
            lang_prepend = translation.lang + '/'
        translation.override_url =  lang_prepend + translation.url



def update_generator_contents(generator, *args):
    """Update the contents lists of a generator

    Empty the (hidden_)translation attribute of article and pages generators
    to prevent generating the translations as they will be generated in the lang sub-site
    and point the content translations links to the sub-sites

    Hide content without a translation for current DEFAULT_LANG
    if HIDE_UNTRANSLATED_CONTENT is True
    """
    generator.translations = []
    is_pages_gen = hasattr(generator, 'pages')
    if is_pages_gen:
        generator.hidden_translations = []
        for page in chain(generator.pages, generator.hidden_pages):
            move_translations_links(page)
    else:                                    # is an article generator
        for article in chain(generator.articles, generator.drafts):
            move_translations_links(article)

    if not generator.settings.get('HIDE_UNTRANSLATED_CONTENT', True):
        return
    contents = generator.pages if is_pages_gen else generator.articles
    hidden_contents = generator.hidden_pages if is_pages_gen else generator.drafts
    default_lang = generator.settings['DEFAULT_LANG']
    for content_object in contents[:]:   # loop over copy for removing
        if content_object.lang != default_lang:
            if isinstance(content_object, Article):
                content_object.status = 'draft'
            elif isinstance(content_object, Page):
                content_object.status = 'hidden'
            contents.remove(content_object)
            hidden_contents.append(content_object)
    if not is_pages_gen: # regenerate categories, tags, etc. for articles
        if hasattr(generator, '_generate_context_aggregate'):                  # if implemented
            # Simulate __init__ for fields that need it
            generator.dates = {}
            generator.tags = defaultdict(list)
            generator.categories = defaultdict(list)
            generator.authors = defaultdict(list)
            generator._generate_context_aggregate()
        else:                             # fallback for Pelican 3.3.0
            regenerate_context_articles(generator)



def install_templates_translations(generator):
    """Install gettext translations for current DEFAULT_LANG in the jinja2.Environment

    if the 'jinja2.ext.i18n' jinja2 extension is enabled
    adds some useful variables into the template context
    """
    generator.context['main_siteurl'] = _main_siteurl
    generator.context['main_lang'] = _main_site_lang
    generator.context['lang_siteurls'] = _lang_siteurls
    current_def_lang = generator.settings['DEFAULT_LANG']
    extra_siteurls = _lang_siteurls.copy()
    extra_siteurls.pop(current_def_lang)
    generator.context['extra_siteurls'] = extra_siteurls
    
    if 'jinja2.ext.i18n' not in generator.settings['JINJA_EXTENSIONS']:
        return
    domain = generator.settings.get('I18N_GETTEXT_DOMAIN', 'messages')
    localedir = generator.settings.get('I18N_GETTEXT_LOCALEDIR')
    if localedir is None:
        localedir = os.path.join(generator.theme, 'translations')
    if current_def_lang == generator.settings.get('I18N_TEMPLATES_LANG', _main_site_lang):
        translations = gettext.NullTranslations()
    else:
        languages = [current_def_lang]
        try:
            translations = gettext.translation(domain, localedir, languages)
        except (IOError, OSError):
            logger.error("Cannot find translations for language '{}' in '{}' with domain '{}'. Installing NullTranslations.".format(languages[0], localedir, domain))
            translations = gettext.NullTranslations()
    newstyle = generator.settings.get('I18N_GETTEXT_NEWSTYLE', True)
    generator.env.install_gettext_translations(translations, newstyle)    



def register():
    signals.initialized.connect(disable_lang_vars)
    signals.generator_init.connect(install_templates_translations)
    signals.article_generator_finalized.connect(update_generator_contents)
    signals.page_generator_finalized.connect(update_generator_contents)
    signals.finalized.connect(create_lang_subsites)
