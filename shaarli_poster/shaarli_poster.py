# -*- coding: utf-8 -*-
import json
import logging
import os
import re
from argparse import ArgumentParser, Namespace
from base64 import b64encode
from collections import defaultdict

from pelican import signals
from pelican.generators import ArticlesGenerator
from pelican.settings import read_settings
from shaarli_client.client import ShaarliV1Client
from shaarli_client.config import get_credentials


DEFAULT_TAG = 'FromPelican'
LOGGER = logging.getLogger(__name__)


def upload_new_articles(generators):
    article_generator = next(g for g in generators if isinstance(g, ArticlesGenerator))
    client = build_shaarli_client(article_generator.settings)
    articles_urls_on_shaarli = get_published_articles_urls(client, article_generator.settings)
    for article in article_generator.articles:
        if article.status == 'published' and article.url not in articles_urls_on_shaarli:
            LOGGER.info('Publishing article %s', article.url)
            publish_new_article(client, article_generator.settings, article)

def build_shaarli_client(settings):
    args = Namespace(
        config=settings.get('SHAARLI_POSTER_CONFIG_FILE_PATH'),
        instance=settings.get('SHAARLI_POSTER_INSTANCE'),
        secret=None,
        url=None,
    )
    return ShaarliV1Client(*get_credentials(args))

def get_published_articles_urls(client, pelican_settings):
    args = Namespace(
        endpoint_name='get-links',
        limit='all',
        searchtags=pelican_settings.get('SHAARLI_POSTER_TAG', DEFAULT_TAG)
    )
    response = client.request(args)
    response.raise_for_status()
    return set(link['url'].rsplit('/', 1)[1] for link in response.json())

def publish_new_article(client, pelican_settings, article):
    description, tags = get_desc_and_tags(article, pelican_settings)
    args = Namespace(
        endpoint_name='post-link',
        url=os.path.join(pelican_settings['SITEURL'], article.url),
        title=article.title,
        description=description,
        tags=tags
    )
    response = client.request(args)
    response.raise_for_status()

def get_desc_and_tags(article, pelican_settings):
    tags = [tag.name for tag in article.tags] + [pelican_settings.get('SHAARLI_POSTER_TAG', DEFAULT_TAG)]
    # We transform relative images URLs into absolute ones:
    description = re.sub(' src="(?!http)', ' src="' + os.path.join(pelican_settings['SITEURL'], ''), article.summary)
    return description, tags

def main():
    args_parser = ArgumentParser()
    args_parser.add_argument('--all', action='store_true', help='Do not filter out articles already published')
    args_parser.add_argument('--starting-id', type=int, default=1)
    args_parser.add_argument('--timezone', default='Europe/Berlin')
    args_parser.add_argument('--timezone-type', type=int, default=3)
    args_parser.add_argument('pelican_config_file')
    args = args_parser.parse_args()
    settings = read_settings(args.pelican_config_file)
    article_generator = build_article_generator(settings, settings['PATH'])
    articles_urls_on_shaarli = set() if args.all else get_published_articles_urls(client, settings)
    links = []
    for i, article in enumerate(article_generator.articles):
        if article.status == 'published' and article.url not in articles_urls_on_shaarli:
            id = args.starting_id + i
            description, tags = get_desc_and_tags(article, settings)
            url = os.path.join(settings['SITEURL'], article.url)
            links.append({
                'url': url,
                'real_url': url,
                'title': article.title,
                'description': description,
                'created': {
                    'date': article.date.strftime('%Y-%m-%d %H:%M:%S.%f'),
                    'timezone_type': args.timezone_type,
                    'timezone': args.timezone
                },
                'tags': ' '.join(tags),
                'id': id,
                'shorturl': small_hash(article.date, id),
                'private': 0,
            })
    print(json.dumps(links, indent=4, sort_keys=True))

def build_article_generator(settings, content_path, output_path=None):
    context = settings.copy()
    context['generated_content'] = dict()
    context['static_links'] = set()
    article_generator = ArticlesGenerator(
        context=context, settings=settings,
        path=content_path, theme=settings['THEME'], output_path=output_path)
    article_generator.generate_context()
    return article_generator

def small_hash(date, id):
    'Reference: https://github.com/shaarli/Shaarli/blob/master/application/Utils.php#L24'
    text = date.strftime('%Y%m%d_%H%M%S') + str(id)
    return b64encode(php_crc32(text.encode()).to_bytes(4, 'big')).decode().replace('=', '')

def php_crc32(a):
    '''
    References:
    - https://www.php.net/manual/en/function.hash-file.php#104836
    - https://stackoverflow.com/a/50843127/636849
    '''
    crc = 0xffffffff
    for x in a:
        crc ^= x << 24;
        for k in range(8):
            crc = (crc << 1) ^ 0x04c11db7 if crc & 0x80000000 else crc << 1
    crc = ~crc
    crc &= 0xffffffff
    # Convert from big endian to little endian:
    return int.from_bytes(crc.to_bytes(4, 'big'), 'little')

def register():
    signals.all_generators_finalized.connect(upload_new_articles)


if __name__ == '__main__':
    main()
