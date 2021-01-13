# Always Modified

Say you want to sort by modified date/time in a theme template, but not all
your articles have modified date/timestamps explicitly defined in article
metadata. This plugin facilitates that sorting by assuming the modified date
(if undefined) is equal to the created date.

## Usage

1. Add `ALWAYS_MODIFIED = True` to your settings file.
2. Now you can sort by modified date in your templates:

    {% for article in articles|sort(reverse=True,attribute='modified') %}

