Section number
---------------

This plugin adds section number to the article's context, in the form of `X.X.X`. Sections are indicated by `<h1>-<h6>` in the parsed html format. 

# Setting

By default, up to 3 levels of sections are numbered. You can customize this value by defining `SECTION_NUMBER_MAX` in your setting file:

```
SECTION_NUMBER_MAX = 5
```

# caution

The first section in the article will be marked as the top section level. Namely, if `<h3>` is the first encountered section, no `<h1>` or `<h2>` is supposed to exist. Else, exception may be thrown out.

# Example
the following markdown content:
```
# section
blabla
## subsection
blabla
## subsection
blabla
# section
blabla
```
will be

>#1 section
>blabla
>##1.1 subsection
>blabla
>##1.2 subsection
>blabla
>#2 section
>blabla