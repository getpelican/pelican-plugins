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

    link_templates = dict(
        mail = "mailto:?subject={title}&amp;body={url}",
        diaspora = "https://sharetodiaspora.github.io/?title={title}&url={url}",
        facebook = "https://www.facebook.com/sharer/sharer.php?u={url}",
        twitter = "https://twitter.com/intent/tweet?text={title}&url={url}{via}{hashtags}",
        hackernews = "https://news.ycombinator.com/submitlink?t={title}&u={url}",
        linkedin = "https://www.linkedin.com/shareArticle?mini=true&url={url}&title={title}&summary={summary}&source={url}",
        reddit = "https://www.reddit.com/submit?url={url}&title={title}",
        mastodon = "https://toot.karamoff.dev/?text={title}%0D%0A{url}",
        telegram = "https://telegram.me/share/url?url={url}",
        whatsapp = "https://api.whatsapp.com/send/?phone&text={title}%0D%0A{url}&app_absent=0",
    )
    fillin = dict(
        title = article_title(content),
        url = article_url(content),
        summary = article_summary(content),
        hashtags = twitter_hastags(content),
        via = twitter_via(content),
    )
    content.share_post = dict([
        (network, link_template.format(**fillin))
        for network, link_template in link_templates.items()
    ])


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
