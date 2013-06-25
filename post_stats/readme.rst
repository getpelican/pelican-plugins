Post Statistics
==================

A Pelican plugin to calculate various statistics about a post and store them in an article.stats dictionary:

- ``wc``: how many words
- ``read_mins``: how many minutes would it take to read this article, based on 250 wpm (http://en.wikipedia.org/wiki/Words_per_minute#Reading_and_comprehension)
- ``word_counts``: frquency count of all the words in the article; can be used for tag/word clouds
- ``fi``: Flesch-kincaid Index/ Reading Ease (see: http://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests)
- ``fk``: Flesch-kincaid Grade Level

Example:

.. code-block:: python

    {
        'wc': 2760,
        'fi': '65.94',
        'fk': '7.65',
        'word_counts': Counter({u'to': 98, u'a': 90, u'the': 83, u'of': 50, ...}),
        'read_mins': 12
    }

This allows you to output these values in your templates, like this, for example:

.. code-block:: html+jinja

	<p title="~{{ article.stats['wc'] }} words">~{{ article.stats['read_mins'] }} min read</p>
	<ul>
	    <li>Flesch-kincaid Index/ Reading Ease: {{ article.stats['fi'] }}</li>
	    <li>Flesch-kincaid Grade Level: {{ article.stats['fk'] }}</li>
	</ul>

The ``word_counts`` variable is a python ``Counter`` dictionary and looks something like this, with each unique word and it's frequency:

.. code-block:: python

	Counter({u'to': 98, u'a': 90, u'the': 83, u'of': 50, u'karma': 50, .....

and can be used to create a tag/word cloud for a post.

Requirements
----------------

`post_stats` requires BeautifulSoup.

.. code-block:: console

    $ pip install beautifulsoup4
