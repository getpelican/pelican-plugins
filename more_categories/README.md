#Subcategory Plugin
This plugin adds support for multiple categories per article, and for nested
categories. It requires Pelican 3.8 or newer.

##Multiple categories
To indicate that an article belongs to multiple categories, use a
comma-separated string:

    Category: foo, bar, bazz

This will add the article to the categories `foo`, `bar` and `bazz`.

###Templates
Existing themes that use `article.category` will display only the first of
these categories, `foo`. This plugin adds `article.categories` that you can
loop over instead. To accomodate this plugin in a theme whether it is present
or not, use:

    {% for cat in article.categories or [article.category] %}
        <a href="{{ SITEURL }}/{{ cat.url }}">{{ cat }}</a>{{ ', ' if not loop.last }}
    {% endfor %}

##Nested categories
(This is a reimplementation of the `subcategory` plugin.)

To indicate that a category is a child of another category, use a
slash-separated string:

    Category: foo/bar/bazz

This will add the article to the categories `foo/bar/bazz`, `foo/bar` and
`foo`.

###Templates
Existing themes that use `article.category` will display the full path to the
most specific of these categories, `foo/bar/bazz`. For any category `cat`, this
plugin adds `cat.shortname`, which in this case is `bazz`, `cat.parent`, which
in this case is the category `foo/bar`, and `cat.ancestors`, which is a list of
the category's ancestors, ending with the category itself. For instance, to
also include a link to each of the ancestor categories on an article page, in
case this plugin in present, use:

    {% for cat in article.category.ancestors or [article.category] %}
        <a href="{{ SITEURL }}/{{ cat.url }}">{{ cat.shortname or cat }}</a>{{ '/' if not loop.last }}
    {% endfor %}

Likewise, `category.shortname`, `category.parent` and `category.ancestors` can
also be used on the category template.

###Slug
The slug of a category is generated recursively by slugifying the shortname of
the category and its ancestors, and preserving slashes:

    slug-of-(foo/bar/baz) := slug-of-foo/slug-of-bar/slug-of-baz

###Category folders
To specify categories using the directory structure, you can configure
`PATH_METADATA` to extract the article path into the `category` metadata. The
following settings would use the entire structure:

    PATH_METADATA = '(?P<category>.*)/.*'

If you store all articles in a single `articles/` folder that you want to
ignore for this purpose, use:

    PATH_METADATA = 'articles/(?P<category>.*)/.*'

###Categories in templates
The list `categories` of all pairs of categories with their corresponding
articles, which is available in the context and can be used in templates (e.g.
to make a menu of available categories), is ordered lexicographically, so
categories always follow their parent:

    aba
    aba/dat
    abaala