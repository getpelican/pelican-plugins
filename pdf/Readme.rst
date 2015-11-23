-------------
PDF Generator
-------------

The PDF Generator plugin automatically exports articles and pages as PDF files
as part of the site-generation process. PDFs are saved to output/pdf/

Requirements
------------
You should ensure you have the ``rst2pdf`` module installed::

	pip install rst2pdf

If you are converting Markdown sources to PDF, you also need the ``xhtml2pdf``
module::

    pip install xhtml2pdf

Usage
-----
To customize the pdf output, you can use the following settings in your
configuration file::

	PDF_STYLE = ''
	PDF_STYLE_PATH = ''

``PDF_STYLE_PATH`` defines a new path where rst2pdf will look for style sheets,
while ``PDF_STYLE`` defines which style you want to use. For a description of
the available styles, please read `rst2pdf's documentation`_.

.. _rst2pdf's documentation: http://rst2pdf.ralsina.me/handbook.html#styles

Known Issues
------------
Relative links in the form of ``|filename|images/test.png`` are not yet handled
by the pdf generator
