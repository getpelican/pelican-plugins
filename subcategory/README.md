#Subcategory Plugin#

This plugin adds support for subcategories in addition to article categories.

Subcategories are hierarchical. Top-level subcategories correspond to categories,
all other subcategories have another subcategory as their parent.

Feeds can be generated for each subcategory, just like categories and tags.

##Usage##

###Metadata###

Subcategories are an extension to categories. Add subcategories to an article's
category metadata using a `/` like this:

    Category: Regular Category/Sub-Category/Sub-Sub-category

Then create a `subcategory.html` template in your theme, similar to the
`category.html` or `tag.html` templates.

In your templates, `article.category` continues to act the same way. Your
subcategories are stored in the `articles.subcategories` list. To create
breadcrumb-style navigation you might try something like this:

    <nav class="breadcrumb">
    <ol>
    {% for subcategory in article.subcategories %}
        <li>
            <a href="{{ SITEURL }}/{{ subcategory.url }}">{{ subcategory.shortname }}</a>
        </li>
    {% endfor %}
    </ol>
    </nav>

###Subcategory folders###

To specify subcategories using folders you can configure `PATH_METADATA`  
to extract the article path (containing all category and subcategory folders) 
into the `subcategory_path` metadata. The following settings would use all available 
subcategories for the hierarchy:

    PATH_METADATA = '(?P<subcategory_path>.*)/.*'

If you store all articles in a single `articles/` folder that you want to ignore for the purpose of subcategories, use:

    PATH_METADATA = 'articles/(?P<subcategory_path>.*)/.*'

You can limit the depth of generated subcategories by adjusting the regular expression
to only include a specific number of path separators (`/`). For example, the following 
would generate only a single level of subcategories under the category level,
regardless of the folder tree depth:

    PATH_METADATA= '(?P<subcategory_path>[^/]*/[^/]*)/.*'

##Subcategory Names##

Each subcategory's full name is a `/`-separated list of it parents and itself.
This is necessary to keep each subcategory unique. It means you can have
`Category 1/Foo` and `Category 2/Foo` and they won't interfere with each other.
Each subcategory has an attribute `shortname` which is just the name without
its parents associated. For example if you had…

    Category/Sub Category1/Sub Category2

… the full name for Sub Category2 would be `Category/Sub Category1/Sub Category2` and
the "short name" would be `Sub Category2`.

If you need to use the slug, it is generated recursively from the full name by slugifying the shortname of the
subcategory and its parents:

    slugified-category/slugified-sub-category/slugified-sub-sub-category

##Settings##

Consistent with the default settings for Tags and Categories, the default
settings for subcategories are:

    'SUBCATEGORY_SAVE_AS' = os.path.join('subcategory', '{savepath}.html')
    'SUBCATEGORY_URL' = 'subcategory/(slug).html'

`savepath` is identical to the slug, except that `savepath` is joined using `os.path.join`.

Similarly, you can save subcategory feeds by adding one of the following
to your Pelican configuration file:

    SUBCATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'
    SUBCATEGORY_FEED_RSS = 'feeds/%s.rss.xml'

… and this will create a feed with `slug` of the subcategory. For example:

    feeds/category/subcategory.atom.xml

Article urls can also use the values of `subpath` and `suburl` in their
definitions. These are equivalent to the `savepath` and `slug` of the most
specific subcategory.

    ARTICLE_SAVE_AS = os.path.join('{subpath}', 'articles', '{slug}.html')
    ARTICLE_URL = '{suburl}/articles/{slug}.html'

##Subcategories in templates##
The list `subcategories` of all pairs of subcategories with their corresponding articles is available in the context
analogous to `categories`, and can be used in templates, e.g. to make a menu of available subcategories.
This list is ordered lexicographically, so subcategories always follow their parent:

    aba
    aba/dat
    abaala

The order may be reversed by setting:

    REVERSE_SUBCATEGORY_ORDER = False

… to `True`, analogous to `REVERSE_CATEGORY_ORDER`.