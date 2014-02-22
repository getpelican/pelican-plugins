# Include Markdown #

This plugin provides the template tag *include_markdown*, which
enables you to include a markdown file from within a (Jinja2)
template.  The *include_markdown* tag expects a path to a markdown
file, located under the Pelican "siteroot".

## Template Example ##

    {% include_markdown content/pages/foo/bar.md %}

## Installation ##

Ensure that `include_markdown.py` is put somewhere that is accessible,
e.g. under the `PLUGIN_PATH`.
To load the plugin add it's name to the `PLUGINS` list.

    PLUGIN_PATH = 'path/to/pelican-plugins'
    PLUGINS = ['include_markdown']