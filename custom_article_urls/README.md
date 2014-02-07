#Custom Article URLs#

This plugin adds support for defining different default URLs for different
categories, or different subcategories if using the subcategory plugin.

##Usage##

After adding `custom_article_urls` to your `PLUGINS`, add a
`CUSTOM_ARTICLE_URLS` setting, which is a dictionary of rules. The rules are
also a dictionary, consisting of the `URL` and the `SAVE_AS` values.

For example, if you had two categories, *Category 1* and *Category 2*, and you
would like *Category 1* saved as `category-1/article-slug/` and *Category 2*
saved as `/year/month/article-slug/`, you would add:

    CUSTOM_ARTICLE_URLS = {
        'Category 1': {'URL': '{category}/{slug}/,
            'SAVE_AS': '{category}/{slug}/index.html},
        'Category 2': {'URL': '{date:%Y}/{date:%B}/{slug}/,
            'SAVE_AS': '{date:%Y}/{date:%B}/{slug}/index.html},
        }

If you had any other categories, they would use the default `ARTICLE_SAVE_AS`
and `ARTICLE_URL` settings.

If you are using the subcategory plugin, you can define them the same way.
For example, if *Category 1* had a subcategory called *Sub Category*, you could
define its rules with::

    'Category 1/Sub Category`: ...

##Other Usage: Article Metadata##

If you define `URL` and `Save_as` in your article metadata, then this plugin
will not alter that value. So you can still specify special one-off URLs as
you normally would.
