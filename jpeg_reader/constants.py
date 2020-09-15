from enum import Enum


class Exiv(Enum):
    DESCRIPTION = 'Exif.Image.ImageDescription'
    ARTIST = 'Exif.Image.Artist'
    DATETIME = 'Exif.Photo.DateTimeOriginal'
    HEADLINE = 'Iptc.Application2.Headline'
    COMMENT = 'Exif.Photo.UserComment'
    CAPTION = 'Iptc.Application2.Caption'
    KEYWORDS = 'Iptc.Application2.Keywords'
    CATEGORY = 'Iptc.Application2.SuppCategory'
    OBJECT_NAME = 'Iptc.Application2.ObjectName'


class PelicanConfig(Enum):
    PATH = 'PATH'
    OUTPUT_PATH = 'OUTPUT_PATH'
    USE_FOLDER_AS_CATEGORY = 'USE_FOLDER_AS_CATEGORY'
    SITE_URL = 'SITEURL'
    PAGE_URL = 'PAGE_URL'
    PAGE_SAVE_AS = 'PAGE_SAVE_AS'
    ARTICLE_URL = 'ARTICLE_URL'
    ARTICLE_SAVE_AS = 'ARTICLE_SAVE_AS'


class PelicanMetadata(Enum):
    TITLE = 'title'
    AUTHORS = 'authors'
    DATE = 'date'
    SLUG = 'slug'
    TAGS = 'tags'
    CATEGORY = 'category'
    SUMMARY = 'summary'
    FEATURED_IMAGE = 'featured_image'  # Acts as a thumbnail
    TEMPLATE = 'template'
    CUSTOM_ALL = 'exiv2'  # Not officially part of metadata, but we add it ourselves


class PelicanClass(Enum):
    BLOG = 'blog'
    PAGES = 'pages'
