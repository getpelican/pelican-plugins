# -*- coding: utf-8 -*-
'''
PDF Generator
-------

The pdf plugin generates PDF files from RST sources.
'''

from __future__ import unicode_literals, print_function

from pelican import signals
from pelican.generators import Generator
from rst2pdf.createpdf import RstToPdf

import os
import logging

logger = logging.getLogger(__name__)


class PdfGenerator(Generator):
    """Generate PDFs on the output dir, for all articles and pages coming from
    rst"""
    def __init__(self, *args, **kwargs):
        super(PdfGenerator, self).__init__(*args, **kwargs)
        
        pdf_style_path = os.path.join(self.settings['PDF_STYLE_PATH'])
        pdf_style = self.settings['PDF_STYLE']
        self.pdfcreator = RstToPdf(breakside=0,
                                   stylesheets=[pdf_style],
                                   style_path=[pdf_style_path])

    def _create_pdf(self, obj, output_path):
        if obj.source_path.endswith('.rst'):
            filename = obj.slug + ".pdf"
            output_pdf = os.path.join(output_path, filename)
            # print('Generating pdf for', obj.source_path, 'in', output_pdf)
            with open(obj.source_path) as f:
                self.pdfcreator.createPdf(text=f.read(), output=output_pdf)
            logger.info(' [ok] writing %s' % output_pdf)

    def generate_context(self):
        pass

    def generate_output(self, writer=None):
        # we don't use the writer passed as argument here
        # since we write our own files
        logger.info(' Generating PDF files...')
        pdf_path = os.path.join(self.output_path, 'pdf')
        if not os.path.exists(pdf_path):
            try:
                os.mkdir(pdf_path)
            except OSError:
                logger.error("Couldn't create the pdf output folder in " +
                             pdf_path)

        for article in self.context['articles']:
            self._create_pdf(article, pdf_path)

        for page in self.context['pages']:
            self._create_pdf(page, pdf_path)


def get_generators(generators):
    return PdfGenerator


def register():
    signals.get_generators.connect(get_generators)
