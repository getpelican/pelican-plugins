import os
from PIL import Image
from pelican import signals
from pilkit.processors import *


def process_images(generator):

    resize = generator.settings.get('RESIZE')
    if resize is None:
        print "\033[1;33mWARNING\033[00m: No Resize Option Provided"
        return

    output_path = generator.settings['OUTPUT_PATH']
    images_output_path = os.path.join(output_path, 'static', 'images')

    try:
        for path, suffix, processes in resize:

            processor = ProcessorPipeline(processes)

            process_path = os.path.join(images_output_path, path)

            for dir_path, dir_names, file_names in os.walk(process_path):
                for name in file_names:
                    image_path = os.path.join(dir_path, name)

                    # Find output path
                    rel_path = os.path.join(os.path.relpath(dir_path, process_path), name)

                    thumbnail_path = os.path.join(images_output_path, path + suffix)
                    output_image_path = os.path.join(thumbnail_path, rel_path)

                    # Create output directory if it doesnt exist
                    (d_path, d_file) = os.path.split(output_image_path)
                    if not os.path.isdir(d_path):
                        os.makedirs(d_path)

                    # Process image
                    image = Image.open(image_path)
                    image = processor.process(image)

                    image.save(output_image_path)

    except (TypeError, AttributeError, ValueError):
        print """\nEnsure the presense of the following setting in pelicanconf.py. Paying particular attention to [], () and ''\n\n
        RESIZE = [
            ('gallery', 'suffix', [SmartResize(100, 100)]), # Path within images to resize, Thumbnail folder suffix (Empty to overwrite), pilkit settings
            ('posts', '', [Adjust(color=0), ResizeToFit(100, 100)])
        ]\n\n"""

        raise


def register():
    signals.finalized.connect(process_images)
