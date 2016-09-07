import os
import os.path as path
import re
from pelican import signals

import logging
logger = logging.getLogger(__name__)

try:
    from PIL import Image, ImageOps
    enabled = True
except ImportError:
    logging.warning("Unable to load PIL, disabling thumbnailer")
    enabled = False

DEFAULT_IMAGE_DIR = "pictures"
DEFAULT_THUMBNAIL_DIR = "thumbnails"
DEFAULT_THUMBNAIL_SIZES = {
    'thumbnail_square': '150',
    'thumbnail_wide': '150x?',
    'thumbnail_tall': '?x150',
}
DEFAULT_TEMPLATE = """<a href="{url}" rel="shadowbox" title="{filename}"><img src="{thumbnail}" alt="{filename}"></a>"""
DEFAULT_GALLERY_THUMB = "thumbnail_square"

class _resizer(object):
    """ Resizes based on a text specification, see readme """

    REGEX = re.compile(r'(\d+|\?)x(\d+|\?)')

    def __init__(self, name, spec, root):
        self._name = name
        self._spec = spec
        # The location of input images from _image_path.
        self._root = root

    def _null_resize(self, w, h, image):
        return image

    def _exact_resize(self, w, h, image):
        retval = ImageOps.fit(image, (w,h), Image.BICUBIC)
        return retval

    def _aspect_resize(self, w, h, image):
        retval = image.copy()
        retval.thumbnail((w, h), Image.ANTIALIAS)

        return retval

    def resize(self, image):
        resizer = self._null_resize

        # Square resize and crop
        if 'x' not in self._spec:
            resizer = self._exact_resize
            targetw = int(self._spec)
            targeth = targetw
        else:
            matches = self.REGEX.search(self._spec)
            tmpw = matches.group(1)
            tmph = matches.group(2)

            # Full Size
            if tmpw == '?' and tmph == '?':
                targetw = image.size[0]
                targeth = image.size[1]
                resizer = self._null_resize

            # Set Height Size
            if tmpw == '?':
                targetw = image.size[0]
                targeth = int(tmph)
                resizer = self._aspect_resize

            # Set Width Size
            elif tmph == '?':
                targetw = int(tmpw)
                targeth = image.size[1]
                resizer = self._aspect_resize

            # Scale and Crop
            else:
                targetw = int(tmpw)
                targeth = int(tmph)
                resizer = self._exact_resize

        logging.debug("Using resizer {0}".format(resizer.__name__))
        return resizer(targetw, targeth, image)

    def get_thumbnail_name(self, in_path):
        # Find the partial path + filename beyond the input image directory.
        prefix = path.commonprefix([in_path, self._root])
        new_filename = in_path[len(prefix) + 1:]

        # Generate the new filename.
        (basename, ext) = path.splitext(new_filename)
        return "{0}_{1}{2}".format(basename, self._name, ext)

    def resize_file_to(self, in_path, out_path, keep_filename=False):
        """ Given a filename, resize and save the image per the specification into out_path

        :param in_path: path to image file to save.  Must be supported by PIL
        :param out_path: path to the directory root for the outputted thumbnails to be stored
        :return: None
        """
        if keep_filename:
            filename = path.join(out_path, path.basename(in_path))
        else:
            filename = path.join(out_path, self.get_thumbnail_name(in_path))
        out_path = path.dirname(filename)
        if not path.exists(out_path):
            os.makedirs(out_path)
        if not path.exists(filename):
            try:
                image = Image.open(in_path)
                thumbnail = self.resize(image)
                thumbnail.save(filename)
                logger.info("Generated Thumbnail {0}".format(path.basename(filename)))
            except IOError:
                logger.info("Generating Thumbnail for {0} skipped".format(path.basename(filename)))


def resize_thumbnails(pelican):
    """ Resize a directory tree full of images into thumbnails

    :param pelican: The pelican instance
    :return: None
    """
    global enabled
    if not enabled:
        return

    in_path = _image_path(pelican)

    sizes = pelican.settings.get('THUMBNAIL_SIZES', DEFAULT_THUMBNAIL_SIZES)
    resizers = dict((k, _resizer(k, v, in_path)) for k,v in sizes.items())
    logger.debug("Thumbnailer Started")
    for dirpath, _, filenames in os.walk(in_path):
        for filename in filenames:
            if not filename.startswith('.'):
                for name, resizer in resizers.items():
                    in_filename = path.join(dirpath, filename)
                    out_path = get_out_path(pelican, in_path, in_filename, name)
                    resizer.resize_file_to(
                        in_filename,
                        out_path, pelican.settings.get('THUMBNAIL_KEEP_NAME'))


def get_out_path(pelican, in_path, in_filename, name):
    base_out_path = path.join(pelican.settings['OUTPUT_PATH'],
                         pelican.settings.get('THUMBNAIL_DIR', DEFAULT_THUMBNAIL_DIR))
    logger.debug("Processing thumbnail {0}=>{1}".format(in_filename, name))
    if pelican.settings.get('THUMBNAIL_KEEP_NAME', False):
        if pelican.settings.get('THUMBNAIL_KEEP_TREE', False):
            return path.join(base_out_path, name, path.dirname(path.relpath(in_filename, in_path)))
        else:
            return path.join(base_out_path, name)
    else:
        return base_out_path


def _image_path(pelican):
    return path.join(pelican.settings['PATH'],
        pelican.settings.get("IMAGE_PATH", DEFAULT_IMAGE_DIR)).rstrip('/')


def expand_gallery(generator, metadata):
    """ Expand a gallery tag to include all of the files in a specific directory under IMAGE_PATH

    :param pelican: The pelican instance
    :return: None
    """
    if "gallery" not in metadata or metadata['gallery'] is None:
        return  # If no gallery specified, we do nothing

    lines = [ ]
    base_path = _image_path(generator)
    in_path = path.join(base_path, metadata['gallery'])
    template = generator.settings.get('GALLERY_TEMPLATE', DEFAULT_TEMPLATE)
    thumbnail_name = generator.settings.get("GALLERY_THUMBNAIL", DEFAULT_GALLERY_THUMB)
    thumbnail_prefix = generator.settings.get("")
    resizer = _resizer(thumbnail_name, '?x?', base_path)
    for dirpath, _, filenames in os.walk(in_path):
        for filename in filenames:
            if not filename.startswith('.'):
                url = path.join(dirpath, filename).replace(base_path, "")[1:]
                url = path.join('/static', generator.settings.get('IMAGE_PATH', DEFAULT_IMAGE_DIR), url).replace('\\', '/')
                logger.debug("GALLERY: {0}".format(url))
                thumbnail = resizer.get_thumbnail_name(filename)
                thumbnail = path.join('/', generator.settings.get('THUMBNAIL_DIR', DEFAULT_THUMBNAIL_DIR), thumbnail).replace('\\', '/')
                lines.append(template.format(
                    filename=filename,
                    url=url,
                    thumbnail=thumbnail,
                ))
    metadata['gallery_content'] = "\n".join(lines)


def register():
    signals.finalized.connect(resize_thumbnails)
    signals.article_generator_context.connect(expand_gallery)
