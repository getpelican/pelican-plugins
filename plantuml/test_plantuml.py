import os
from os.path import dirname, join
import unittest

from .generateUmlDiagram import generate_uml_image


PARENT_DIR = dirname(__file__)


class GenerateUmlDiagramTest(unittest.TestCase):
    def test_sequence_diagram(self):
        with open(join(PARENT_DIR, 'test_data/sequence.uml')) as sequence_file:
            generated_img_path = join(PARENT_DIR, generate_uml_image(PARENT_DIR, sequence_file.read(), 'svg'))
        with open(join(PARENT_DIR, 'test_data/sequence.svg')) as expected_svg_file:
            with open(generated_img_path) as actual_svg_file:
                self.assertListEqual(expected_svg_file.readlines(), actual_svg_file.readlines())
        os.remove(generated_img_path)
