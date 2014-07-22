Interlinks
=========================

This plugin lets you add frequently used URLs to your markup using short keywords. Short URL format is 
``keyword>rest-of-url`` where ``keyword`` is defined in the settings.py. Later it is replaced with acutal URL in
the generated HTML output.


Requirements
--------------------
``interlinks`` requires BeautifulSoup

	pip install beautifulsoup4

Installation
--------------------

Install the plugin normally (plugins folder), then add interlinks in the settings.py:

	PLUGINS = ["interlinks"]
	
Usage
------------------

The interlinks are specified in the settings.py file as (example):

	INTERLINKS = {
	    'wikipedia_en': 'http://en.wikipedia.org/wiki/',
	    'wikipedia_es': 'http://es.wikipedia.org/wiki/',
	    'ddg': 'https://duckduckgo.com/?q='
	}

There's also a default key, ``this``, that is mapped to the ``SITEURL`` variable.

Then, in a blog post, you just create a normal link but adding the ``keyword>`` syntax in the url specification, followed by the rest of the url. 

Example 
-------------------
(markdown syntax)

	[Normal boring link](http://www.example.com). But this is a [cool link](this>) that links to this site.

	Search in [Wikipedia](wikipedia_en>python), ([here](wikipedia_es>python) in spanish). Also can [search](ddg>python) it.

All the above will be rendered as: 

	<p><a href="http://www.example.com">Normal boring link</a>. But this is a <a href="http://[yoursite]/index.html">cool link</a> that links to this site.</p>
	
	<p>Search in <a href="http://en.wikipedia.org/wiki/python">Wikipedia</a>, (<a href="http://es.wikipedia.org/wiki/python">here</a> in spanish). Also can <a href="https://duckduckgo.com/?q=python">search</a> it.</p>
