import os
from PIL import Image
from pelican import signals
from pilkit.processors import *  # NOQA


def process_images(generator):

    resize = generator.settings['RESIZE']

    output_path = generator.settings['OUTPUT_PATH']
    images_output_path = os.path.join(output_path, 'static', 'images')

    for path, suffix, processes in resize:

        processor = ProcessorPipeline(processes)

        process_path = os.path.join(images_output_path, path)

        for dir_path, dir_names, file_names in os.walk(process_path):
            for name in file_names:
                image_path = os.path.join(dir_path, name)

                # Find output path
                rel_path = os.path.join(os.path.rel_path(dir_path, process_path), name)  # NOQA

                thumbnail_path = os.path.join(images_output_path, path + suffix)  # NOQA
                output_image_path = os.path.join(thumbnail_path, rel_path)

                # Create output directory if it doesnt exist
                (d_path, d_file) = os.path.split(output_image_path)
                if not os.path.isdir(d_path):
                    os.makedirs(d_path)

                # Process image
                image = Image.open(image_path)
                image = processor.process(image)

                image.save_image(output_image_path)


def register():
    signals.finalized.connect(process_images)
