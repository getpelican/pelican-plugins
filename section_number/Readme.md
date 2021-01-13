Section Number
--------------

This plugin adds section numbers to an article's context, in the form of `X.X.X`. Sections are indicated via Markdown headers, which appear as `<h1> – <h6>` in the generated HTML.


# Settings

By default, up to three section levels will be prefixed with numbers. You can customize this value by defining `SECTION_NUMBER_MAX` in your settings file:

    SECTION_NUMBER_MAX = 5


# Caveat

The first section in the article will be marked as the top section level. Namely, if `<h3>` is the first section encountered, the plugin assumes that no `<h1>` or `<h2>` sections will be present. Otherwise an exception may result.


# Example

The following Markdown content...

    # section
    blabla
    ## subsection
    blabla
    ## subsection
    blabla
    # section
    blabla

... will be rendered as:

>#1 section
>blabla
>##1.1 subsection
>blabla
>##1.2 subsection
>blabla
>#2 section
>blabla
