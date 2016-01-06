Members
-------

This plugin looks for a ``members`` metadata header containing key/value pairs
and makes them available for use in templates.

The first line of this metadata defines each key, and the following line should
contain corresponding values for each member.

The keys must be in the same first line as the ``members`` metadata header,
and the next line containing the corresponding values must have an identation
before it.

Example for reStructuredText::

    :members: name, email, twitter, github, site_nome, site_href
        Danilo Shiga, daniloshiga@gmail.com, @daneoshiga, daneoshiga, Danilo Shiga, http://daniloshiga.com

Example for Markdown::

    members: name, email, twitter, github, site_nome, site_href
        Danilo Shiga, daniloshiga@gmail.com, @daneoshiga, daneoshiga, Danilo Shiga, http://daniloshiga.com
