# Static Discussion via Hubski
*Author: St John Karp <stjohn@fuzzjunket.com>*

Query comments for a Hubski post via their API and embed them in your articles. This is a static version of Hubski's own "Discussion via Hubski", which embeds the comments section on your website using a dynamic JavaScript query.

## Installation

This plugin requires Beautiful Soup 4 to be installed on your system. This module takes care of any manipulation required on the HTML of the comments. On Debian you can install BS4 from the official repo:

    apt-get install python-bs4

Then download the python-plugins repo and add this to your PLUGINS definition:

    PLUGINS = ['hubski-static',]

## Usage

For each article that has a Hubski post, put the post ID in the metadata with the key Hubski_ID. For example in a Markdown article you might have:

    Hubski_ID: 12345

When you generate the site, Static DvH will query the Hubski API for each article that has an ID. It will then populate two properties on the `article` object — `article.hubski_comment_count` and `article.hubski_comments`.

`article.hubski_comment_count` is simply the number of comments on this Hubski post.

    {% if article.hubski_comment_count %}
        <div class="comments">
            <p><a href="{{ SITEURL }}/{{ article.url }}#comments">{{ article.hubski_comment_count }} Comments</a></p>
        </div><!-- #comments -->
    {% endif %}

`article.hubski_comments` contains the a list of comment objects as defined in the [Hubski API](https://hubski.com/pub?id=266825). The comments are largely unaltered, with the exception of adding an `iso_date` field and converting all relative links in the comment HTML to absolute links.

    {% if article.hubski_id %}
        <div id="comments">
            <h3><img src="{{ SITEURL }}/theme/images/hubski_logo.png" style="margin-right: 10px;" /><span style="position: relative; top: -10px;">Discussion via Hubski</span></h3>
            <p><strong>Check out <a href="{{ HUBSKI_POST_URL }}{{ article.hubski_id }}">Hubski</a> to comment or reply!</strong></p>
            {% for comment in article.hubski_comments recursive %}
                <div class="comment">
                    <p><a href="{{ HUBSKI_USER_URL }}{{ comment.user }}" target="_blank">{{ comment.user }}</a> {{ comment.iso_date }} · <a href="{{ HUBSKI_POST_URL }}{{ comment.id }}" target="_blank">link</a></p>
                    {{ comment.text }}
                    {% if comment.children %}
                        {{ loop(comment.children) }}
                    {% endif %}
                </div>
            {% endfor %}
        </div><!-- #comments -->
    {% endif %}

## Styling

Some simple styling can be achieved by indenting replies to give the comments structure.

    div.comment {
        border-left: 1px solid gray;
        padding-left: 10px;
    }

    div.comment > div.comment {
        margin-left: 15px;
    }

## Settings

Add the following handy settings to your conf file. Some of these are required by Static Discussion via Hubski, while others are just handy to use in your templates:

    HUBSKI_URL = 'https://hubski.com'
    HUBSKI_POST_URL = HUBSKI_URL + '/pub?id='
    HUBSKI_USER_URL = HUBSKI_URL + '/user?id='
    HUBSKI_API_TREE_URL = HUBSKI_URL + '/api/publication/$id/tree'

These are all straightforward strings which can be used in your templates, with the exception of the tree URL setting which is intended to be used as a string template by the plugin.
