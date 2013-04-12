Random Article Plugin For Pelican
========================

This plugin generates a html file which redirect to a random article
using javascript's `window.location`. The generated html file is 
saved at `SITEURL`.

Only published articles are listed to redirect.

Usage
-----

To use it you have to add in your config file the name of the file to use:

    RANDOM = 'random.html'

Then in some template you add:

    <a href="{{ SITEURL }}/{{ RANDOM }}">random article</a>
