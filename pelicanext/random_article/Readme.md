Random Article Plugin For Pelican
========================

This plugin generates a html file which redirect to a random article
using javascript's window.location. The generated html file is 
saved at SITEURL.

Only published articles are listed to redirect.


Installation
------------

To enable, ensure that `random_article.py` is put somewhere that is accessible.
Then use as follows by adding the following to your settings.py:

    PLUGINS = ["random_article"]

An easy way to find where pelican is installed is to verbose list the
available themes by typing `pelican-themes -l -v`.

Once the pelican folder is found, copy `random_article.py` to the `plugins` folder. Then
add to settings.py like this:

    PLUGINS = ["pelican.plugins.random_article"]

Usage
-----

To use it you have to add in your config file the name of the file to use:

    RANDOM = 'random.html'

Then in some template you add:

    <a href="{{ SITEURL }}/{{ RANDOM }}">random article</a>
