# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import itertools
import json
import logging
import multiprocessing
import os
import pprint
import re
import sys

from pelican.generators import ArticlesGenerator
from pelican.generators import PagesGenerator
from pelican.settings import DEFAULT_CONFIG
from pelican import signals
from pelican.utils import pelican_open

logger = logging.getLogger(__name__)

try:
    import tagpy
    from shutil import copyfile
except ImportError:
    logger.error('music: tagpy and/or shutil modules not found')

MUSIC_ROOT_OUTPUT = 'music'
def initialized(pelican):
    p = os.path.expanduser('~/Music')

    DEFAULT_CONFIG.setdefault('MUSIC_LIBRARY', p)
    DEFAULT_CONFIG.setdefault('MUSIC_COVER', 'cover.jpg')
    DEFAULT_CONFIG['plugin_dir'] = os.path.dirname(os.path.realpath(__file__))

    if pelican:
        pelican.settings.setdefault('MUSIC_LIBRARY', p)
        pelican.settings.setdefault('MUSIC_COVER', 'cover.jpg')

#
# check if copy is needed :DONE:
#
def check_copy(src, dest):
    if not os.path.exists(src):
        logger.warn('music: Source {} does not exist!!!'.format(src))
        return False

    if not os.path.exists(dest):
        logger.info('music: Destination {} does not exist yet.'.format(dest))
        return True

    if os.path.getmtime(src) > os.path.getmtime(dest):
        logger.info('music: Destination {} is older than source {}.'.format(dest, src))
        return True

    logger.info('music: Source {} is older than destination {}.'.format(src, dest))
    return False

#
# read json tags from previsouly processed tracks :DONE:
#
def read_tags(filename):
    tag = {}
    with pelican_open(filename) as text:
        tag = json.loads(text)
    return tag

#
# guess if file is a image (e.g: a cover.jpg) :DONE:
#
def is_image(path):
    return path.endswith('.jpeg') or path.endswith('.JPEG') or path.endswith('.jpg') or path.endswith('.JPG') or path.endswith('.png') or path.endswith('.PNG') or path.endswith('.gif') or path.endswith('.GIF')

#
# scan '{music}' contents in HTML and proccess accordingly. :DONE:
#
def replace_music_entities(content):
    library = os.path.expanduser(content.settings['MUSIC_LIBRARY'])

    site = content.settings['SITEURL']
    if site == None:
        site = ''

    relative = not site.startswith('http')
    siteslash = site.endswith('/')

    if relative:
        outputmusic = os.path.join(site, MUSIC_ROOT_OUTPUT)
    elif siteslash:
        outputmusic = site + MUSIC_ROOT_OUTPUT
    else:
        outputmusic = site + '/' + MUSIC_ROOT_OUTPUT

    content._content = content._content.replace('{music}', outputmusic)

#
# generates a music_album context object from album header :DONE:
#
def process_album_header(generator, content, header):
    library = os.path.expanduser(generator.settings['MUSIC_LIBRARY'])

    albumtitle = header
    if re.match('^{music}.*{[^}]+}$', albumtitle):
        albumtitle = re.sub('^{music}.*{([^}]+)}$', '\\1', albumtitle)
    else:
        albumtitle = re.sub('^{music}.*/(.+)/?$', '\\1', albumtitle)
    logger.info('music: albumtitle {}'.format(albumtitle))

    albumpath = header
    if re.match('^{music}.*{[^}]+}$', albumpath):
        albumpath = re.sub('^({music}.*){[^}]*}$', '\\1', albumpath)
    logger.info('music: albumpath {}'.format(albumpath))

    albumpath = albumpath.replace('{music}', library)
    coverpath = os.path.join(albumpath, generator.settings['MUSIC_COVER'])

    albumout = header
    if re.match('^{music}.*{[^}]+}$', albumout):
        albumout = re.sub('^({music}.*){[^}]*}$', '\\1', albumout)
    albumout = albumout.replace('{music}', MUSIC_ROOT_OUTPUT)
    absalbumout = os.path.join(generator.output_path, albumout)
    logger.info('music: albumout {}'.format(albumout))

    coverout = os.path.join(albumout, generator.settings['MUSIC_COVER'])
    abscoverout = os.path.join(absalbumout, generator.settings['MUSIC_COVER'])

    if not os.path.exists(absalbumout):
        try:
            os.makedirs(absalbumout)
        except Exception:
            logger.exception('music: Could not create {}'.format(absalbumout))

    # copy cover file to the output directory
    if check_copy(coverpath, abscoverout):
        copyfile(coverpath, abscoverout) 

    tagsfiles = []
    # copy all track files to the output directory
    sortedfiles = os.listdir(albumpath);
    sortedfiles.sort()
    for f in sortedfiles:
        path = os.path.join(albumpath, f)
        if os.path.isfile(path) and not f.endswith('.tags') and not is_image(f):
            trackout = os.path.join(albumout, f)
            abstrackout = os.path.join(absalbumout, f)

            # copy audio file if needed
            if check_copy(path, abstrackout):
                copyfile(path, abstrackout)

            # create tags json file if needed
            tagspath = os.path.splitext(path)[0] + '.tags'
            if check_copy(path, tagspath):
                make_tags(path, tagspath)

    tracks = []
    # rescan now for json tag files
    sortedfiles = os.listdir(albumpath);
    sortedfiles.sort()
    for f in sortedfiles:
        path = os.path.join(albumpath, f)
        if os.path.isfile(path) and f.endswith('.tags'):
            tag = read_tags(path)
            track = {
                "artist": tag.get('artist', ''),
                "album": tag.get('album', ''),
                "cover": coverout,
                "path": os.path.join(albumout, tag.get('file', '')),
                "title": tag.get('title', ''),
                "track": tag.get('track', 0),
                "year": tag.get('year', 1970) }
            tracks.append(track)

    content.music_album = {
        "path": albumout,
        "title": albumtitle,
        "cover": coverout,
        "tracks": tracks }

def check_tag(tag):
    return {
        'artist': getattr(tag, 'artist', '(unknown)'),
        'album': getattr(tag, 'album', '(unknown)'),
        'title': getattr(tag, 'title', '(unknown)'),
        'track': getattr(tag, 'track', 0),
        'year': getattr(tag, 'year', 1970) }

#
# make .tags json file from audio file :DONE:
#
def make_tags(infile, outfile):
    try:
        insong = tagpy.FileRef(infile).file()
    except Exception as e:
        logger.exception('music: Could not open for reading {}'.format(infile))
        return

    tag = insong.tag()
    if tag is  None:
        tag = {
            "artist": '',
            "album": '',
            "title": '',
            "track": 0,
            "year": 1970 }
    else:
        tag = check_tag(tag)

    tag['file'] = os.path.basename(infile)

    try:
        outtags = open(outfile, 'w')
    except Exception as e:
        logger.exception('music: Could not open for writing {}'.format(outname))
        return

    jss = json.dumps(tag)
    outtags.write(jss)
    outtags.close()

#
# generates a music_track context object from track header :DONE:
#
def process_track_header(generator, content, header):
    library = os.path.expanduser(generator.settings['MUSIC_LIBRARY'])

    trackpath = header
    trackpath = trackpath.replace('{music}', library)
    tagspath = os.path.splitext(trackpath)[0] + '.tags'

    trackout = header
    trackout = trackout.replace('{music}', MUSIC_ROOT_OUTPUT)
    abstrackout = os.path.join(generator.output_path, trackout)

    cover = generator.settings['MUSIC_COVER']
    coverpath = os.path.join(os.path.dirname(trackpath), cover)
    coverout = os.path.join(os.path.dirname(trackout), cover)
    abscoverout = os.path.join(generator.output_path, coverout)

    if check_copy(trackpath, tagspath):
        make_tags(trackpath, tagspath)

    # copy the audio file in output directory
    directory = os.path.dirname(abstrackout)
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except Exception:
            logger.exception('music: Could not create {}'.format(directory))

    if check_copy(trackpath, abstrackout):
        copyfile(trackpath, abstrackout) 
    if check_copy(coverpath, abscoverout):
        copyfile(coverpath, abscoverout) 

    tag = read_tags(tagspath)

    content.music_track = {
        "artist": tag.get('artist', ''),
        "album": tag.get('album', ''),
        "cover": coverout,
        "path": trackout,
        "title": tag.get('title', ''),
        "track": tag.get('track', 0),
        "year": tag.get('year', 1970) }


    if isinstance(generator, ArticlesGenerator):
        #print(generator)
        return
    if isinstance(generator, PagesGenerator):
        #print(generator)
        return

#
# detect header Track: or Album: and process them :DONE:
#
def on_all_generators_finalized(generators):
    for generator in generators:
        if isinstance(generator, ArticlesGenerator):
            for article in itertools.chain(generator.articles, generator.translations, generator.drafts):
                track = article.metadata.get('track', None)
                if track and track.startswith('{music}'):
                    process_track_header(generator, article, track)
                album = article.metadata.get('album', None)
                if album and album.startswith('{music}'):
                    process_album_header(generator, article, album)
        elif isinstance(generator, PagesGenerator):
            for page in itertools.chain(generator.pages, generator.translations, generator.hidden_pages):
                track = page.metadata.get('track', None)
                if track and track.startswith('{music}'):
                    process_track_header(generator, page, track)
                album = article.metadata.get('album', None)
                if album and album.startswith('{music}'):
                    process_album_header(generator, page, album)

#
# entry point.
#
def register():
    """Uses the new style of registration based on GitHub Pelican issue #314."""
    signals.initialized.connect(initialized)
    try:
        signals.content_object_init.connect(replace_music_entities)
        signals.all_generators_finalized.connect(on_all_generators_finalized)
        #signals.article_writer_finalized.connect(on_writer_finalized)
    except Exception as e:
        logger.exception('music: Plugin failed to execute: {}'.format(pprint.pformat(e)))
