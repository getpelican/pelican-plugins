Twitter Bootstrap Directive for restructured text
-------------------------------------------------

This plugin defines some rst directive that enable a clean usage of the twitter bootstrap CSS and Javascript components.

Directives
----------

Implemented directives:

    label,
    alert,
    panel,
    media

Implemented roles:

    glyph,
    code,
    kbd

Usage
-----

For more informations about the usage of each directive, read the corresponding class description.
Or checkout this demo page.

Dependencies
------------

In order to use this plugin, you need to use a template that supports bootstrap 3.1.1 with the glyph font setup
correctly. Usually you should have this structure::

    static
    ├──  css
    |     └──  bootstrap.min.css
    ├──  font
    |     └──  glyphicons-halflings-regular.ttf
    └──  js
          └──     

Warning
-------

In order to support some unique features and avoid conflicts with bootstrap, this plugin will use a custom html writer which
is modifying the traditional docutils output.