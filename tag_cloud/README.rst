tag_cloud
=========

This plugin generates a tag-cloud.

Installation
------------

In order to use to use this plugin, you have to edit(*) or create(+) the following files::

      blog/
        ├── pelicanconf.py *
        ├── content
        ├── plugins +
        │     └── tag_cloud.py +
        └── themes
              └── mytheme
                    ├── templates
                    │      └── base.html *
                    └── static
                          └── css
                               └── style.css *

In **pelicanconf.py** you have to activate the plugin::

    PLUGIN_PATHS = ["plugins"]
    PLUGINS = ["tag_cloud"]

Into your **plugins** folder, you should add tag_cloud.py (from this repository).

In your theme files, you should change **base.html** to apply formats (and sizes) defined in **style.css**, as specified in "Settings", below.

Settings
--------

================================================    =====================================================
Setting name (followed by default value)            What does it do?
================================================    =====================================================
``TAG_CLOUD_STEPS = 4``                             Count of different font sizes in the tag
                                                    cloud.
``TAG_CLOUD_MAX_ITEMS = 100``                       Maximum number of tags in the cloud.
``TAG_CLOUD_SORTING = 'random'``                    The tag cloud ordering scheme.  Valid values:
                                                    random, alphabetically, alphabetically-rev, size and
                                                    size-rev
``TAG_CLOUD_BADGE = True``                          Optionnal setting : can bring **badges**, which mean
                                                    say : display the number of each tags present
                                                    on all articles.
================================================    =====================================================

The default theme does not include a tag cloud, but it is pretty easy to add one::

    <ul class="tagcloud">
        {% for tag in tag_cloud %}
            <li class="tag-{{ tag.1 }}">
                <a href="{{ SITEURL }}/{{ tag.0.url }}">
                {{ tag.0 }}
                    {% if TAG_CLOUD_BADGE %}
                        <span class="badge">{{ tag.2 }}</span>
                    {% endif %}
                </a>
            </li>
        {% endfor %}
    </ul>

You should then also define CSS styles with appropriate classes (tag-1 to tag-N,
where N matches ``TAG_CLOUD_STEPS``), tag-1 being the most frequent, and
define a ``ul.tagcloud`` class with appropriate list-style to create the cloud.
You should copy/paste this **badge** CSS rule ``ul.tagcloud .list-group-item <span>.badge``
if you're using ``TAG_CLOUD_BADGE`` setting. (this rule, potentially long , is suggested to avoid
conflicts with CSS libs as twitter Bootstrap)

For example::

    ul.tagcloud {
      list-style: none;
        padding: 0;
    }

    ul.tagcloud li {
        display: inline-block;
    }

    li.tag-1 {
        font-size: 150%;
    }

    li.tag-2 {
        font-size: 120%;
    }

    /* ... add li.tag-3 etc, as much as needed */

    ul.tagcloud .list-group-item span.badge {
        background-color: grey;
        color: white;
    }

By default the tags in the cloud are sorted randomly, but if you prefers to have it alphabetically use the `alphabetically` (ascending) and `alphabetically-rev` (descending). Also is possible to sort the tags by it's size (number of articles with this specific tag) using the values `size` (ascending) and `size-rev` (descending).
