# Better Tables

This pelican plugin removes the excess attributes and elements in the HTML
tables generated from RST. Trimming this fat allows them to pass HTML5
validation. Hopefully rst2html5 will be merged into pelican at some point, but
until then, this hacky approach is needed.

This approach has the advantage of restoring sanity to tables, and allows their
column with to flow normally. All styling is default and must be styled by CSS
rather than in HTML attributes.

I make no claim that /all/ HTML table crimes generated are corrected, merely
the ones which I have stumbled across.

## Requirements

* Beautiful Soup 4

## What does it do?

At the moment, the following is stripped from tables (though when in doubt,
check the source as it may be updated out of sync with this document).

* <colgroup> element (and its evil <col> children)
* table's "border" attribute
* <tbody> and <thead>'s valign attribute

## Usage

Enable the plugin in your pelicanconf.py

```
PLUGINS = [
    # ...
    'better_tables',
    # ...
]
```

And that's it. Life's simple like that sometimes.
