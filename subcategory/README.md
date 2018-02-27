#Subcategory Plugin#

This plugin adds support for subcategories: nested categories that have another category as their parent.

##Usage##

###Metadata###

Subcategories are an extension to categories. Add subcategories to an article's
category metadata using a `/` like this:

    Category: Category/Subcategory/Subsubcategory

In your templates, `article.category` is the most specific subcategory of your article,
whereas `articles.category_branch` also stores its parents, in descending order. To create
breadcrumb-style navigation you might try something like this:

    <nav class="breadcrumb">
    <ol>
    {% for cat in article.category_branch %}
        <li>
            <a href="{{ SITEURL }}/{{ cat.url }}">{{ cat.shortname }}</a>
        </li>
    {% endfor %}
    </ol>
    </nav>

###Category folders###

To specify categories using folders you can configure `PATH_METADATA`
to extract the article path (containing all category folders)
into the `category_path` metadata. The following settings would use all available
subcategories for the hierarchy:

    PATH_METADATA = '(?P<category_path>.*)/.*'

If you store all articles in a single `articles/` folder that you want to ignore for the purpose of subcategories, use:

    PATH_METADATA = 'articles/(?P<category_path>.*)/.*'

You can limit the depth of generated categories by adjusting the regular expression
to only include a specific number of path separators (`/`). For example, the following
would generate only a single level of subcategories under the category level,
regardless of the folder tree depth:

    PATH_METADATA= '(?P<category_path>[^/]*/[^/]*)/.*'

##Category Names##

Each category's full name is a `/`-separated list of it parents and itself.
This is necessary to keep each category unique. It means you can have
`Category 1/Foo` and `Category 2/Foo` and they won't interfere with each other.
Each category has an attribute `shortname` which is just the name without
its parents associated. For example if you had…

    Category/Sub Category1/Sub Category2

… the full name for Sub Category2 would be `Category/Sub Category1/Sub Category2` and
the "short name" would be `Sub Category2`.

If you need to use the slug, it is generated recursively from the full name by slugifying the shortname of the
subcategory and its parents:

    slugified-category/slugified-sub-category/slugified-sub-sub-category

##Categories in templates##
The list `categories` of all pairs of categories with their corresponding articles, which is available in the context
and can be used in templates, e.g. to make a menu of available categories, is ordered lexicographically,
so categories always follow their parent:

    aba
    aba/dat
    abaala
