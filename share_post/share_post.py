"""
Share Post plugin.

This plugin adds share URL to article. These links are textual which means no
online tracking of your readers.
"""

from bs4 import BeautifulSoup

from pelican import contents, signals
from pelican.generators import ArticlesGenerator, PagesGenerator

try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote


def article_title(content):
    main_title = BeautifulSoup(content.title, 'html.parser').get_text().strip()
    sub_title = ''
    if hasattr(content, 'subtitle'):
        sub_title = ' ' + BeautifulSoup(content.subtitle, 'html.parser').get_text().strip()  # noqa
    return quote(('%s%s' % (main_title, sub_title)).encode('utf-8'))


def article_url(content):
    site_url = content.settings['SITEURL']
    return quote(('%s/%s' % (site_url, content.url)).encode('utf-8'))


def article_summary(content):
    return quote(BeautifulSoup(content.summary, 'html.parser').get_text().strip().encode('utf-8'))  # noqa


def twitter_hastags(content):
    tags = getattr(content, 'tags', [])
    hashtags = ','.join((tag.slug for tag in tags))
    return '' if not hashtags else '&hashtags=%s' % hashtags


def twitter_via(content):
    twitter_username = content.settings.get('TWITTER_USERNAME', '')
    return '' if not twitter_username else '&via=%s' % twitter_username


def share_post(content):
    if isinstance(content, contents.Static):
        return

    title = article_title(content)
    url = article_url(content)
    summary = article_summary(content)
    hastags = twitter_hastags(content)
    via = twitter_via(content)

    mail_link = 'mailto:?subject=%s&amp;body=%s' % (title, url)
    diaspora_link = 'https://sharetodiaspora.github.io/?title=%s&url=%s' % (
        title, url)
    facebook_link = 'https://www.facebook.com/sharer/sharer.php?u=%s' % url
    twitter_link = 'https://twitter.com/intent/tweet?text=%s&url=%s%s%s' % (
        title, url, via, hastags)
    hackernews_link = 'https://news.ycombinator.com/submitlink?t=%s&u=%s' % (
        title, url)
    linkedin_link = 'https://www.linkedin.com/shareArticle?mini=true&url=%s&title=%s&summary=%s&source=%s' % (  # noqa
        url, title, summary, url
    )
    reddit_link = 'https://www.reddit.com/submit?url=%s&title=%s' % (
        url, title)

    content.share_post = {
        'diaspora': diaspora_link,
        'twitter': twitter_link,
        'facebook': facebook_link,
        'linkedin': linkedin_link,
        'hacker-news': hackernews_link,
        'email': mail_link,
        'reddit': reddit_link,
    }


def run_plugin(generators):
    for generator in generators:
        if isinstance(generator, ArticlesGenerator):
            for article in generator.articles:
                share_post(article)
                for translation in article.translations:
                    share_post(translation)
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
