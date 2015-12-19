"""
Feed Template Pelican plugin allows to customize article title, link and description in RSS feeds using a template.
"""
from pelican import signals
from pelican.writers import Writer
import six
from jinja2 import Markup
from six.moves.urllib.parse import urlparse
from pelican.utils import set_date_tzinfo


def load_template(generator):
    """Load 'feed' template and store its macros in FeedCustomizationWriter."""
    try:
        tpl_macros = generator.get_template("feed").make_module(generator.context)
        FeedCustomizationWriter.macros = tpl_macros
    except Exception:
        pass


def get_writer(pelican_object):
    """Provide customuzed writer."""
    return FeedCustomizationWriter


class FeedCustomizationWriter(Writer):
    """Writer that allows to customize feeds using template macros."""
    macros = None  # Template macros

    def _add_item_to_the_feed(self, feed, item):
        if self.macros is None:
            # Fall back to default behaviour if macros was not loaded
            return Writer._add_item_to_the_feed(self, feed, item)
        title = Markup(item.title).striptags()
        link = '%s/%s' % (self.site_url, item.url)
        content = item.get_content(self.site_url)
        feed.add_item(
            title=self.macros.title(item) if hasattr(self.macros, 'title') else title,
            link=self.macros.link(item).strip() if hasattr(self.macros, 'link') else link,
            unique_id='tag:%s,%s:%s' % (urlparse(link).netloc,
                                        item.date.date(),
                                        urlparse(link).path.lstrip('/')),
            description=self.macros.description(item) if hasattr(self.macros, 'description') \
                                                      else content,
            categories=item.tags if hasattr(item, 'tags') else None,
            author_name=getattr(item, 'author', ''),
            pubdate=set_date_tzinfo(
                item.modified if hasattr(item, 'modified') else item.date,
                self.settings.get('TIMEZONE', None)))


def register():
    signals.article_generator_init.connect(load_template)
    signals.get_writer.connect(get_writer)
