# Feed Filter Plugin

This plugin allows to filter elements in feeds.

## Requirements
None.

## Settings

### `FEED_FILTER = {}`
Define feed paths and include/exclude filters to apply to matching feeds. Both feed paths and filters are matched using [Unix shell-stye wildcards][1].

Filters are defined as:
* `include.item attribute`
* `exclude.item_attribute`

where `item_attribute` can be any [feed item attribute][2], ie. `title`, `link`, `author_name`, `categories`, ...

You can also match `pubdate` and `updateddate` item attributes as strings formatted with the following format: `%a, %d %b %Y %H:%M:%S` (e.g. 'Thu, 28 Jun 2001 14:17:15')

**Filter priorities**

If an inclusion filter is defined, only feed elements that match the filter will be included in the feed.

If an exclusion filter is defined, all feed elements except those which match the filter will be included in the feed.

If both include and exclude filters are defined, all feed elements except those which match some exclusion filter but no inclusion filter, will be included in the feed.

## Examples
* Include only posts in some categories into the global feed:
```
#
FEED_ATOM = 'feed/atom'
FEED_RSS = 'feed/rss'
FEED_FILTER = {
    'feed/*': {
        'include.categories': ('software-development', 'programming')
    }
}
```

* Exclude an author from a category feed:
```
CATEGORY_FEED_ATOM = 'feed/{slug}.atom'
CATEGORY_FEED_RSS = 'feed/{slug}.rss'
FEED_FILTER = {
    'feed/a-category-slug.*': {
        'exclude.author_name': 'An Author name'
    }
}
```

* Exclude an author from all category feeds:
```
CATEGORY_FEED_ATOM = 'feed/{slug}.atom'
CATEGORY_FEED_RSS = 'feed/{slug}.rss'
FEED_FILTER = {
    'feed/*.*': {
        'exclude.author_name': 'An Author name'
    }
}
```

* In the global feed, exclude all posts in a category, except if written by a given author:
```
FEED_ATOM = 'feed/atom'
FEED_RSS = 'feed/rss'
FEED_FILTER = {
    'feed/*': {
        'include.author_name': 'An Author name',
        'exclude.category': 'software-development'
    }
}
```

* In the global feed, exclude all posts whose title starts with "Review":
```
FEED_ATOM = 'feed/atom'
FEED_RSS = 'feed/rss'
FEED_FILTER = {
    'feed/*': {
        'exclude.title': 'Review*'
    }
}
```

[1]: https://docs.python.org/3/library/fnmatch.html "Fnmatch Python module"
[2]: https://github.com/getpelican/feedgenerator/blob/master/feedgenerator/django/utils/feedgenerator.py#L132 "Feed item attributes"
