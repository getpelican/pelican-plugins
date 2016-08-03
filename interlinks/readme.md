Interlinks
==========

This plugin lets you add frequently-used URLs to your markup using short keywords.
Short URL format is `keyword>rest-of-url` where `keyword` is defined in your Pelican
settings file. This is subsequently replaced with the actual URL in the generated
HTML output.


Requirements
------------

This plugin requires BeautifulSoup:

	pip install beautifulsoup4

Installation
------------

Put the plugin into your plugins folder, then add Interlinks in your settings file:

	PLUGINS = ["interlinks"]

Usage
-----

Interlinks are specified in your settings file. Here is an example:

	INTERLINKS = {
	    'wikipedia_en': 'http://en.wikipedia.org/wiki/',
	    'wikipedia_es': 'http://es.wikipedia.org/wiki/',
	    'ddg': 'https://duckduckgo.com/?q='
	}

There's also a default key, `this`, that is mapped to the `SITEURL` variable.

Then, in your content, you just create a normal link but add the `keyword>` syntax as the URL scheme, followed by the rest of the URL.

Example (Markdown syntax)
-------------------------

	[Normal boring link](http://www.example.com). But this is a [cool link](this>) that links to this site.

	Search in [Wikipedia](wikipedia_en>python), ([here](wikipedia_es>python) in Spanish). You can also [search](ddg>python) it.

All the above will be rendered as:

	<p><a href="http://www.example.com">Normal boring link</a>. But this is a <a href="http://[yoursite]/index.html">cool link</a> that links to this site.</p>

	<p>Search in <a href="http://en.wikipedia.org/wiki/python">Wikipedia</a>, (<a href="http://es.wikipedia.org/wiki/python">here</a> in Spanish). You can also <a href="https://duckduckgo.com/?q=python">search</a> it.</p>
