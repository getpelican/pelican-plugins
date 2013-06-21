from .magic_set import magic_set
from jinja2 import Markup
from pelican import signals
from pelican.writers import Writer
from pelican.utils import set_date_tzinfo, truncate_html_words
import re

"""
Feed Summary
-------

This plugin allows summaries to be used in feeds instead of the full length article.
"""


@magic_set(Writer)
def _add_item_to_the_feed(self, feed, item):
    title = Markup(item.title).striptags()

    # Determine what is being used for the article summary
    full_article = item.get_content(self.site_url)
    continuation_delim = '...'

    if self.settings['FEED_USE_SUMMARY']:
        if hasattr(item, '_summary'):
            description = item._update_content(item._summary,self.site_url)
        elif self.settings['FEED_SUMMARY_LENGTH']:
            description = truncate_html_words(full_article, num=self.settings['FEED_SUMMARY_LENGTH'], end_text=continuation_delim)
        elif self.settings['SUMMARY_MAX_LENGTH']:
            description = truncate_html_words(full_article, num=self.settings['SUMMARY_MAX_LENGTH'], end_text=continuation_delim)
        else:
            description = truncate_html_words(full_article, num=50, end_text=continuation_delim)

        # Determine if "read more" link should be added based on word counts
        # Attempt to remove tags and extra spaces before counting words
        re_tag = re.compile(r"""<(/)?([^ ]+?)(?: (/)| .*?)?>""")
        full_article_strip = re.sub(re_tag, '', full_article).strip()
        description_strip = re.sub(re_tag, '', description).strip()

        full_article_word_count = len(re.split(r"""\s+""", full_article_strip))
        description_word_count = len(re.split(r"""\s+""", description_strip))
        
        if description_word_count < full_article_word_count:
            if hasattr(item, '_summary'):
                description = re.sub(r"""</p>$""", ' ' + continuation_delim + "</p>", description).rstrip()
            description += '<p><a href="%s/%s">Read More</a></p>' % (self.site_url, item.url)
    else:
        description = full_article

    # Add the item to the feed
    feed.add_item(
        title=title,
        link='%s/%s' % (self.site_url, item.url),
        unique_id='tag:%s,%s:%s' % (self.site_url.replace('http://', ''),
                                    item.date.date(), item.url),
        description=description,
        categories=item.tags if hasattr(item, 'tags') else None,
        author_name=getattr(item, 'author', ''),
        pubdate=set_date_tzinfo(item.date,
            self.settings.get('TIMEZONE', None)))

def initialized(pelican):
    from pelican.settings import _DEFAULT_CONFIG
    _DEFAULT_CONFIG.setdefault('FEED_USE_SUMMARY', False)
    _DEFAULT_CONFIG.setdefault('FEED_SUMMARY_LENGTH', False)

    if pelican:
        pelican.settings.setdefault('FEED_USE_SUMMARY', False)
        pelican.settings.setdefault('FEED_SUMMARY_LENGTH', False)

def mod_pelican_writer(object):
    @magic_set(object)
    def get_writer(self):
        return Writer(self.output_path,settings=self.settings)

def register():
    signals.initialized.connect(initialized)
    signals.initialized.connect(mod_pelican_writer)
