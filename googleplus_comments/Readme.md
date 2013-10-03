GooglePlus Comments Plugin For Pelican
==================================

Adds GooglePlus comments to Pelican

Add the plugin to `pelicanconf.py`:

    PLUGIN_PATH = 'pelican-plugins'
    PLUGINS = ["googleplus_comments"]

Add a `<div>` for comments to the `article.html` of your template:

    <div id="commentswrap">
    <div id="comments"></div>
    </div>
    {{ article.metadata.googleplus_comments }}

See it working, and ask for support:

<http://zonca.github.io/2013/09/google-plus-comments-plugin-for-pelican.html>
