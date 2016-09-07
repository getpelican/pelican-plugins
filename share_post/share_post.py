"""
Share Post
==========

This plugin adds share URL to article. These links are textual which means no
online tracking of your readers.
"""

from bs4 import BeautifulSoup
try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote
from pelican import signals, contents
from pelican.generators import ArticlesGenerator, PagesGenerator


def article_title(content):
    main_title = BeautifulSoup(content.title, 'html.parser').get_text().strip()
    sub_title = ''
    if hasattr(content, 'subtitle'):
        sub_title = ' ' + BeautifulSoup(content.subtitle, 'html.parser').get_text().strip()
    return quote(('%s%s' % (main_title, sub_title)).encode('utf-8'))


def article_url(content):
    site_url = content.settings['SITEURL']
    return quote(('%s/%s' % (site_url, content.url)).encode('utf-8'))


def article_summary(content):
    return quote(BeautifulSoup(content.summary, 'html.parser').get_text().strip().encode('utf-8'))


def share_post(content):
    if isinstance(content, contents.Static):
        return
    title = article_title(content)
    url = article_url(content)
    summary = article_summary(content)

    tweet = ('%s%s%s' % (title, quote(' '), url)).encode('utf-8')
    diaspora_link = 'https://sharetodiaspora.github.io/?title=%s&url=%s' % (title, url)
    facebook_link = 'http://www.facebook.com/sharer/sharer.php?u=%s' % url
    gplus_link = 'https://plus.google.com/share?url=%s' % url
    twitter_link = 'http://twitter.com/home?status=%s' % tweet
    linkedin_link = 'https://www.linkedin.com/shareArticle?mini=true&url=%s&title=%s&summary=%s&source=%s' % (
        url, title, summary, url
    )

    mail_link = 'mailto:?subject=%s&amp;body=%s' % (title, url)

    share_links = {
                   'diaspora': diaspora_link,
                   'twitter': twitter_link,
                   'facebook': facebook_link,
                   'google-plus': gplus_link,
                   'linkedin': linkedin_link,
                   'email': mail_link
                   }
    content.share_post = share_links


def run_plugin(generators):
    for generator in generators:
        if isinstance(generator, ArticlesGenerator):
            for article in generator.articles:
                share_post(article)
        elif isinstance(generator, PagesGenerator):
            for page in generator.pages:
                share_post(page)


def register():
    try:
        signals.all_generators_finalized.connect(run_plugin)
    except AttributeError:
        # NOTE: This results in #314 so shouldn't really be relied on
        # https://github.com/getpelican/pelican-plugins/issues/314
        signals.content_object_init.connect(share_post)

