"""
This plugin uses the metadata from JPEG images (EXIF and IPTC) to construct a meaningful page or gallery.
Possible uses are gallery pages or a blog article that's mainly about an image.
With this tool, it's posible to just dump an image without any extra data/linkage to create coherent output.
The note here is that the extension is `jpeg_article` so it doesn't pick up {attach} or other static resources.
"""

import logging
from datetime import datetime
from os import makedirs, sep
from os.path import join, dirname, isdir, splitext
from typing import Tuple

from PIL import Image
from pelican import signals
from pelican.readers import BaseReader
from pelican.urlwrappers import URLWrapper, Category, Author, Tag

from .constants import Exiv, PelicanConfig, PelicanMetadata, PelicanClass
from .exiv2_parser import Exiv2Parser


class JpegReader(BaseReader):
    logger = logging.getLogger('JpegReader')
    enabled = True
    file_extensions = ('jpeg_article')
    thumb_size = 250, 250

    def __init__(self, settings):
        super(JpegReader, self).__init__(settings)

    def read(self, source_path):
        try:
            if Exiv2Parser.get_exiv2_version() is not None:
                content, metadata = self.parse_jpeg(source_path=source_path)

        except ValueError:      # if file can't be parsed, ignore it
            pass
        else:
            return content, metadata

    def parse_jpeg(self, *, source_path: str) -> Tuple[str, dict]:
        JpegReader.logger.info(source_path)

        img = Image.open(source_path)

        image_data = Exiv2Parser.get_values(source_path)

        title = image_data.get(Exiv.DESCRIPTION.value, 'Untitled')
        author = image_data.get(Exiv.ARTIST.value, 'Unknown')
        date_string = image_data.get(Exiv.DATETIME.value, '')

        date = datetime.strptime(date_string, "%Y:%m:%d %H:%M:%S")
        slug = URLWrapper(image_data.get(Exiv.HEADLINE.value, title), self.settings).slug
        description_long = image_data.get(Exiv.COMMENT.value, '')
        summary = image_data.get(Exiv.CAPTION.value, description_long[:140])

        tags = [Tag(tag, self.settings) for tag in image_data.get(Exiv.KEYWORDS.value, list())]

        content_root = self.settings[PelicanConfig.PATH.value]
        path_output = self.settings[PelicanConfig.OUTPUT_PATH.value]
        relative_source = dirname(source_path[len(content_root):]).lstrip(sep)
        if self.settings[PelicanConfig.USE_FOLDER_AS_CATEGORY.value]:
            category = relative_source.split(sep)[-1]
        else:
            category = image_data.get(Exiv.CATEGORY.value, None)

        type_of_content = relative_source.split(sep)[0]  # either 'blog' or 'pages' as far as I know.
        url_site = self.settings[PelicanConfig.SITE_URL.value]

        if type_of_content.lower() == PelicanClass.PAGES.value:
            url_document = self.settings[PelicanConfig.PAGE_URL.value]
            document_save_as = self.settings[PelicanConfig.PAGE_SAVE_AS.value]
        else:  # Assume PelicanClass.BLOG
            url_document = self.settings[PelicanConfig.ARTICLE_URL.value]
            document_save_as = self.settings[PelicanConfig.ARTICLE_SAVE_AS.value]

        page_url_complete = join(url_site, url_document)

        author_wrapper = Author(author, self.settings)

        # Move image in place:
        metadata = {PelicanMetadata.TITLE.value: title, PelicanMetadata.AUTHORS.value: [author_wrapper],
                    PelicanMetadata.DATE.value: date, PelicanMetadata.SLUG.value: slug,
                    PelicanMetadata.TAGS.value: tags,
                    PelicanMetadata.CUSTOM_ALL.value: image_data}
        if category is not None:
            metadata[PelicanMetadata.CATEGORY.value] = Category(category, self.settings)

        thumb_name = '{0}_thumb.jpg'.format(slug)
        original_name = '{0}.jpg'.format(slug)

        path_output_html = join(path_output, document_save_as).format(**metadata)
        path_output_dir = dirname(path_output_html)
        path_output_original = join(path_output_dir, original_name)
        path_output_thumb = join(path_output_dir, thumb_name)

        # Here we generate the summary info incase this is used for articles we get nice thumbnails and summary
        metadata[PelicanMetadata.SUMMARY.value] = summary
        metadata[PelicanMetadata.FEATURED_IMAGE.value] = join(url_site, path_output_thumb[len(path_output):])
        if Exiv.OBJECT_NAME.value in image_data:
            metadata[PelicanMetadata.TEMPLATE.value] = image_data[Exiv.OBJECT_NAME.value]

        # Write the size/HTML out before we reduce the image to a thumb
        content = "<img src='{src}' alt='{alt}' style='width: {width}px; height: auto; max-width: 100%;'></img><p>{body}</p>" \
            .format(src=original_name, alt=title, width=img.width, height=img.height, body=description_long)

        # Ensure the directory levels exist
        if not isdir(path_output_dir):
            makedirs(path_output_dir)
        img.save(path_output_original)
        img.thumbnail(self.thumb_size)
        img.save(path_output_thumb)

        # Debug info if we need it
        JpegReader.logger.debug(content)
        JpegReader.logger.debug(str(metadata))
        JpegReader.logger.debug(path_output_html)

        return content, metadata


def add_reader(readers):
    readers.reader_classes['jpeg_article'] = JpegReader


def register():
    signals.readers_init.connect(add_reader)