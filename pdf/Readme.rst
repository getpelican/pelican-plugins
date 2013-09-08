-------------
PDF Generator
-------------

The PDF Generator plugin automatically exports RST articles and pages
as PDF files as part of the site-generation process. PDFs are saved to
output/pdf/

Requirements
------------
You should ensure you have the ```rst2pdf`` module installed::

	pip install rst2pdf
	
Usage
-----
In order to use this plugin you should add the following to your config file::

	PDF_STYLE = ''
	PDF_STYLE_PATH = ''

Known Issues
------------
Relative links in the form of ``|filename|images/test.png`` are not yet handled 
by the pdf generator
