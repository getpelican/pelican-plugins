Members
-------

This plugin looks for a ``members`` metadata header containing key/value pairs
and makes them available for use in templates

The first line of the members metadata defines each key, and the following
lines contain corresponding values for each member.

The key line must be in the same line as the metadata name 'members', and each
member data must have an identation before it.

In ReSTructuredText::

    :members: nome, email, twitter, github, site_nome, site_href
        Danilo Shiga, daniloshiga@gmail.com, @daneoshiga, daneoshiga, Danilo Shiga, http://daniloshiga.com


In Markdown::

    members: nome, email, twitter, github, site_nome, site_href
        Danilo Shiga, daniloshiga@gmail.com, @daneoshiga, daneoshiga, Danilo Shiga, http://daniloshiga.com
