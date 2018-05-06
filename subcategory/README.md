# Subcategory Plugin

This plugin adds support for subcategories in addition to article categories.

Subcategories are hierarchical. Each subcategory has a parent, which is either a regular category or another subcategory.

Feeds can be generated for each subcategory, just like categories and tags.

## Usage

### Metadata

Subcategories are an extension to categories. Add subcategories to an article's category metadata using a `/` like this:

```
Category: Regular Category/Sub-Category/Sub-Sub-category
```

Then create a `subcategory.html` template in your theme, similar to the `category.html` or `tag.html` templates.

In your templates, `article.category` continues to act the same way. Your subcategories are stored in the `articles.subcategories` list. To create breadcrumb-style navigation you might try something like this:

```
<nav class="breadcrumb">
<ol>
    <li>
        <a href="{{ SITEURL }}/{{ article.category.url }}">{{ article.category}}</a>
    </li>
{% for subcategory in article.subcategories %}
    <li>
        <a href="{{ SITEURL }}/{{ subcategory.url }}">{{ subcategory.shortname }}</a>
    </li>
{% endfor %}
</ol>
</nav>
```

### Subcategory folders

To specify subcategories using folders you can configure `PATH_METADATA`<br>
to extract the article path (containing all category and subcategory folders) into the `subcategory_path` metadata. The following settings would use all available subcategories for the hierarchy:

```
PATH_METADATA= '(?P<subcategory_path>.*)/.*'
```

You can limit the depth of generated subcategories by adjusting the regular expression to only include a specific number of path separators (`/`). For example, the following would generate only a single level of subcategories regardless of the folder tree depth:

```
PATH_METADATA= '(?P<subcategory_path>[^/]*/[^/]*)/.*'
```

## Subcategory Names

Each subcategory's full name is a `/`-separated list of it parents and itself. This is necessary to keep each subcategory unique. It means you can have `Category 1/Foo` and `Category 2/Foo` and they won't interfere with each other. Each subcategory has an attribute `shortname` which is just the name without its parents associated. For example if you had...

```
Category/Sub Category1/Sub Category2
```

... the full name for Sub Category2 would be `Category/Sub Category1/Sub Category2` and the "short name" would be `Sub Category2`.

If you need to use the slug, it is generated from the short name -- not the full name.

## Settings

Consistent with the default settings for Tags and Categories, the default settings for subcategories are:

```
'SUBCATEGORY_SAVE_AS' = os.path.join('subcategory', '{savepath}.html')
'SUBCATEGORY_URL' = 'subcategory/(fullurl).html'
```

`savepath` and `fullurl` are generated recursively, using slugs. So the full URL would be:

```
category-slug/sub-category-slug/sub-sub-category-slug
```

... with `savepath` being similar but joined using `os.path.join`.

Similarly, you can save subcategory feeds by adding one of the following to your Pelican configuration file:

```
SUBCATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'
SUBCATEGORY_FEED_RSS = 'feeds/%s.rss.xml'
```

... and this will create a feed with `fullurl` of the subcategory. For example:

```
feeds/category/subcategory.atom.xml
```

Article urls can also use the values of `subpath` and `suburl` in their definitions. These are equivalent to the `fullurl` and `savepath` of the most specific subcategory. If you have articles that don't have subcategories these values are set to the category slug.

```
ARTICLE_SAVE_AS = os.path.join('{subpath}' 'articles' '{slug}.html')
ARTICLE_URL = '{suburl}/articles/{slug}.html'
```
