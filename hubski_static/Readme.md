# Static Discussion via Hubski
*Author: St John Karp <stjohn@fuzzjunket.com>*

Scrape comments from a Hubski post and embed them in your articles. This is a static version of Hubski's own "Discussion via Hubski", which embeds the comments section on your website using a dynamic JavaScript query.

## Installation

This plugin requires Beautiful Soup 4 to be installed on your system. This module takes care of all the web scraping required to get the comments from Hubski. On Debian you can install BS4 from the official repo:

    apt-get install python-bs4

Then download the python-plugins repo and add this to your PLUGINS definition:

    PLUGINS = ['hubski-static',]

## Usage

For each article that has a Hubski post, put the post ID in the metadata with the key Hubski_ID. For example in a Markdown article you might have:

    Hubski_ID: 12345

When you generate the site, Static DvH will query Hubski for each article that has an ID. It will then populate three properties on the `article` object — `article.hubski_comment_count`, `article.hubski_comments`, and `article.hubski_post_url`.

`article.hubski_comment_count` is simply the number of comments on this Hubski post.

    {% if article.hubski_comment_count %}
        <div class="comments">
            <p><a href="{{ SITEURL }}/{{ article.url }}#comments">{{ article.hubski_comment_count }} Comments</a></p>
        </div><!-- #comments -->
    {% endif %}

`article.hubski_comments` contains the HTML dump of the comments section. It does not parse out the comments into an iterable. `article.hubski_post_url` contains the full URL of this post on Hubski.

    <div id="comments">
        <h3>Discussion via Hubski</h3>
        <p><strong>Check out <a href="{{ article.hubski_post_url }}">Hubski</a> to comment or reply!</strong></p>
        {% if article.hubski_comments %}
            {{ article.hubski_comments }}
        {% endif %}
    </div><!-- #comments -->

## Styling

Some simple styling can be achieved by indenting replies to give the comments structure.

    div.subcom {
        margin-left: 15px;
    }

## Settings

If Hubski were to change its URLs, this plugin would break. In case that ever happens, you can override the URL structure in your settings file. These are the default values:

    HUBSKI_URL = 'https://hubski.com'
    HUBSKI_POST_URL = HUBSKI_URL + '/pub?id='

The ID of each post then gets appended to the `HUBSKI_POST_URL`.
