import os
import sys
import logging
from pkg_resources import EntryPoint

from jinja2 import Template, TemplateNotFound

try:
    import plim
except ImportError:
    plim = None

try:
    import mako.lookup
except ImportError:
    mako = None

try:
    from bs4 import BeautifulSoup as bs
except ImportError:
    bs = None

try:
    from htmlmin import minify
except ImportError:
    minify = None

from pelican.writers import Writer, is_selected_for_writing
from pelican.paginator import Paginator
from pelican import signals

logger = logging.getLogger(__name__)

def get_writer(sender):

    class PlimWriter(Writer):
        def write_file(self, name, template, context, relative_urls=False,
                       paginated=None, override_output=False, **kwargs):
            """Render the template and write the file.
            :param name: name of the file to output
            :param template: template to use to generate the content
            :param context: dict to pass to the templates.
            :param relative_urls: use relative urls or absolutes ones
            :param paginated: dict of article list to paginate - must have the
                same length (same list in different orders)
            :param override_output: boolean telling if we can override previous
                output with the same name (and if next files written with the same
                name should be skipped to keep that one)
            :param **kwargs: additional variables to pass to the templates
            """

            if name is False or name == "" or\
               not is_selected_for_writing(self.settings,\
                   os.path.join(self.output_path, name)):
                return
            elif not name:
                # other stuff, just return for now
                return

            def _render_using_plim(filename, localcontext):
                """Render the template using Plim."""

                root_dir = os.path.dirname(os.path.abspath(filename))
                template_file = os.path.basename(filename)
                lookup = mako.lookup.TemplateLookup(
                    directories=[root_dir],
                    input_encoding='utf-8',
                    output_encoding='utf-8',
                    preprocessor=plim.preprocessor,
                    strict_undefined=True,
                    default_filters=['trim'])

                output = lookup.get_template(template_file).render_unicode(
                    **localcontext)
                if ('SLIM_OPTIONS' in self.settings and
                        'PRETTYIFY' in self.settings['SLIM_OPTIONS'] and
                        self.settings['SLIM_OPTIONS']['PRETTYIFY']):
                    output = bs(output, 'html.parser').prettify() # prettify the html
                else:
                    output = minify(output) # minify the html
                return output

            def _write_file(template, localcontext, output_path, name, override):
                """Render the template write the file."""
                # set localsiteurl for context so that Contents can adjust links
                if localcontext['localsiteurl']:
                    context['localsiteurl'] = localcontext['localsiteurl']

                output = _render_using_plim(template.filename, localcontext)
                # output = template.render(localcontext) # render using jinja2

                path = os.path.join(output_path, name)
                try:
                    os.makedirs(os.path.dirname(path))
                except Exception:
                    pass

                with self._open_w(path, 'utf-8', override=override) as f:
                    f.write(output)
                logger.info('Writing %s', path)

                # Send a signal to say we're writing a file with some specific
                # local context.
                signals.content_written.send(path, context=localcontext)

            def _get_localcontext(context, name, kwargs, relative_urls):
                localcontext = context.copy()
                localcontext['localsiteurl'] = localcontext.get(
                    'localsiteurl', None)
                if relative_urls:
                    relative_url = path_to_url(get_relative_path(name))
                    localcontext['SITEURL'] = relative_url
                    localcontext['localsiteurl'] = relative_url
                localcontext['output_file'] = name
                localcontext.update(kwargs)
                return localcontext

            # pagination
            if paginated:

                # pagination needed, init paginators
                paginators = {key: Paginator(name, val, self.settings)
                              for key, val in paginated.items()}

                # generated pages, and write
                for page_num in range(list(paginators.values())[0].num_pages):
                    paginated_kwargs = kwargs.copy()
                    for key in paginators.keys():
                        paginator = paginators[key]
                        previous_page = paginator.page(page_num) \
                            if page_num > 0 else None
                        page = paginator.page(page_num + 1)
                        next_page = paginator.page(page_num + 2) \
                            if page_num + 1 < paginator.num_pages else None
                        paginated_kwargs.update(
                            {'%s_paginator' % key: paginator,
                             '%s_page' % key: page,
                             '%s_previous_page' % key: previous_page,
                             '%s_next_page' % key: next_page})

                    localcontext = _get_localcontext(context, page.save_as,
                        paginated_kwargs, relative_urls)
                    _write_file(template, localcontext, self.output_path,
                                page.save_as, override_output)
            else:
                # no pagination
                localcontext = _get_localcontext(context, name, kwargs,
                    relative_urls)
                _write_file(template, localcontext, self.output_path, name,
                            override_output)

    return PlimWriter

def register():
    """Plugin registration."""
    if not plim:
        logger.warning('`slim` failed to load dependency `plim`. '
                       '`slim` plugin not loaded.')
        return
    if not mako:
        logger.warning('`slim` failed to load dependency `mako`. '
                       '`slim` plugin not loaded.')
        return
    if not bs:
        logger.warning('`slim` failed to load dependency `BeautifulSoup4`. '
                       '`slim` plugin not loaded.')
        return
    if not minify:
        logger.warning('`slim` failed to load dependency `htmlmin`. '
                       '`slim` plugin not loaded.')
        return

    signals.get_writer.connect(get_writer)
