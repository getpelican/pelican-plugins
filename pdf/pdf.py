# -*- coding: utf-8 -*-
'''
PDF Generator
-------

The pdf plugin generates PDF files from reStructuredText and Markdown sources.
'''

from __future__ import unicode_literals, print_function

from io import open
from pelican import signals
from pelican.generators import Generator
from pelican.readers import MarkdownReader

import os
import logging

logger = logging.getLogger(__name__)

import xhtml2pdf.util
if 'pyPdf' not in dir(xhtml2pdf.util):
    try:
        from xhtml2pdf.util import PyPDF2
        xhtml2pdf.util.pyPdf = PyPDF2
    except ImportError:
        logger.error('Failed to monkeypatch xhtml2pdf. ' +
                     'You have missing dependencies')
        raise

from rst2pdf.createpdf import RstToPdf


class PdfGenerator(Generator):
    "Generate PDFs on the output dir, for all articles and pages"

    supported_md_fields = ['date']

    def __init__(self, *args, **kwargs):
        super(PdfGenerator, self).__init__(*args, **kwargs)

        if 'PDF_STYLE_PATH' in self.settings:
            pdf_style_path = [self.settings['PDF_STYLE_PATH']]
        else:
            pdf_style_path = []

        if 'PDF_STYLE' in self.settings:
            pdf_style = [self.settings['PDF_STYLE']]
        else:
            pdf_style = []

        self.pdfcreator = RstToPdf(breakside=0,
                                   stylesheets=pdf_style,
                                   style_path=pdf_style_path,
                                   raw_html=True)

    def _create_pdf(self, obj, output_path):
        filename = obj.slug + '.pdf'
        output_pdf = os.path.join(output_path, filename)
        mdreader = MarkdownReader(self.settings)
        _, ext = os.path.splitext(obj.source_path)
        if ext == '.rst':
            with open(obj.source_path, encoding='utf-8') as f:
                text = f.read()
            header = ''
        elif ext[1:] in mdreader.file_extensions and mdreader.enabled:
            text, meta = mdreader.read(obj.source_path)
            header = ''

            if 'title' in meta:
                title = meta['title']
                header = title + '\n' + '#' * len(title) + '\n\n'
                del meta['title']

            for k in meta.keys():
                # We can't support all fields, so we strip the ones that won't
                # look good
                if k not in self.supported_md_fields:
                    del meta[k]

            header += '\n'.join([':%s: %s' % (k, meta[k]) for k in meta])
            header += '\n\n.. raw:: html\n\n\t'
            text = text.replace('\n', '\n\t')

            # rst2pdf casts the text to str and will break if it finds
            # non-escaped characters. Here we nicely escape them to XML/HTML
            # entities before proceeding
            text = text.encode('ascii', 'xmlcharrefreplace')
        else:
            # We don't support this format
            logger.warn('Ignoring unsupported file ' + obj.source_path)
            return

        logger.info(' [ok] writing %s' % output_pdf)
        self.pdfcreator.createPdf(text=(header+text),
                                  output=output_pdf)

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
