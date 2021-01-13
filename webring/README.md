# Webring Plugin

**NOTE: [This plugin has been moved to its own repository](https://github.com/pelican-plugins/webring). Please file any issues/PRs there. Once all plugins have been migrated to the [new Pelican Plugins organization](https://github.com/pelican-plugins), this monolithic repository will be archived.**

This plugin retrieves the latest posts from a list of web feeds and makes
them available in templates, effectively creating a [partial webring][1]. Posts
are sorted from newer to older.

It is inspired by [openring](https://git.sr.ht/~sircmpwn/openring), a tool for
generating an HTML file to include in your [SSG][2] from a template and a list of
web feeds.

## Requirements

It requires the `feedparser` module:

    $ pip install feedparser

`feedparser` supports many common and not so common feed formats (e.g RSS/Atom). [See a list here](https://pythonhosted.org/feedparser/introduction.html).

## Settings

```
WEBRING_FEED_URLS = []
```
A list of web feeds in the form of a URL or local file.

```
WEBRING_MAX_ARTICLES = 3
```
The maximum number of articles.

```
WEBRING_ARTICLES_PER_FEED = 1
```
The maximum number of articles per feed.

```
WEBRING_SUMMARY_LENGTH = 128
```
The maximum length of post summaries.

```
WEBRING_CLEAN_SUMMARY_HTML = True
```
Whether to clean html tags from post summaries or not.

### Example
Let's suppose we have two blogs in our webring and want to show two articles
per blog. We would also like to show a quite short summary.

```
WEBRING_FEED_URLS = [
    'https://justinmayer.com/feeds/all.atom.xml',
    'https://danluu.com/atom.xml'
]
WEBRING_ARTICLES_PER_FEED = 2
WEBRING_MAX_ARTICLES = 4
WEBRING_SUMMARY_LENGTH = 25
```

## Templates
The plugin makes available the resulting web feed articles in the variable
`webring_articles`, which is a list of `Article` objects whose attributes are:

- `title`: The article title.
- `link`: The article URL.
- `date`: The article date as a Pelican `utils.SafeDatetime` object, which can
be used with [Pelican's Jinja filter `strftime`](https://docs.getpelican.com/en/stable/themes.html#date-formatting).
- `summary`: The article summary, as provided in the web feed and modified
according to this plugin's settings.
- `source_title`: The title of the web feed.
- `source_link`: A link to the web feed.
- `source_id`: An identification field provided in some web feeds.

See the following section for an example on how to iterate the article list.

### Example
Imagine we'd like to put our webring in the bottom of the default Pelican
template (ie. notmyidea). To simplify, we'll use the existing CSS classes.

Edit the `notmyidea/templates/base.html` file and make it look like this:

```
        ...
        <section id="extras" class="body">
        {% if WEBRING_FEED_URLS %}
            <div class="webring">
                <h2>Webring</h2>
                {% for article in webring_articles %}
                <p><a href="{{ article.link }}">{{ article.title }}</a></p>
                <p>{{ article.date|strftime('%d %B %Y') }} - {{ article.summary}}</p>
                {% endfor %}
            </div>
        {% endif %}
        {% if LINKS %}
        ...
```

If there were no links or social widgets, the result would be like in the
image below:

![Example of Webring](https://github.com/getpelican/pelican-plugins/raw/master/webring/example.png)


[1]: https://en.wikipedia.org/wiki/Webring "In a proper webring, websites would be linked in a circular structure."
[2]: https://en.wikipedia.org/wiki/Category:Static_website_generators "Static Site Generator"
