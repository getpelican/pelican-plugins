from pelican import signals
from pelican.writers import Writer
import six
from jinja2 import Markup
from six.moves.urllib.parse import urlparse
from pelican.utils import set_date_tzinfo


macros = None


def load_template(generator):
    try:
        global macros
        macros = generator.get_template("feed").module
    except Exception:
        pass


def get_writer(pelican_object):
    if macros is not None:
        return FeedCustomizationWriter
    else:
        return None


class FeedCustomizationWriter(Writer):
    def _add_item_to_the_feed(self, feed, item):
        """
        Custom function for adding articles to the feed.

        Can replaces original one from the pelican.writers.Writer class
        and adds processing article data using template macros.
        """
        title = Markup(item.title).striptags()
        link = '%s/%s' % (self.site_url, item.url)
        content = item.get_content(self.site_url)
        feed.add_item(
            title=macros.title(item) if hasattr(macros, 'title') else title,
            link=macros.link(item, self.site_url) if hasattr(macros, 'link') else link,
            unique_id='tag:%s,%s:%s' % (urlparse(link).netloc,
                                        item.date.date(),
                                        urlparse(link).path.lstrip('/')),
            description=macros.description(item, self.site_url) if hasattr(macros, 'description') else content,
            categories=item.tags if hasattr(item, 'tags') else None,
            author_name=getattr(item, 'author', ''),
            pubdate=set_date_tzinfo(
                item.modified if hasattr(item, 'modified') else item.date,
                self.settings.get('TIMEZONE', None)))


def register():
    signals.article_generator_init.connect(load_template)
    signals.get_writer.connect(get_writer)
