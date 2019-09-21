import os
from os.path import dirname, join
import unittest

from .generateUmlDiagram import generate_uml_image


PARENT_DIR = dirname(__file__)


class GenerateUmlDiagramTest(unittest.TestCase):
    maxDiff = None
    def test_sequence_diagram(self):
        with open(join(PARENT_DIR, 'test_data/sequence.uml')) as sequence_file:
            generated_img_path = join(PARENT_DIR, generate_uml_image(PARENT_DIR, sequence_file.read(), 'svg'))
        with open(generated_img_path) as actual_svg_file:
            self.assertIn('<svg ', actual_svg_file.read())
        os.remove(generated_img_path)
