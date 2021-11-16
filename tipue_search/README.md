Tipue Search
============

> :warning: **Instead of this plugin, please use the [Pelican Search](https://github.com/pelican-plugins/search) plugin.**

> :warning: **This plugin, and the jQuery code upon which it depends, _is abandoned and no longer maintained_.**


Purpose
-------

Serialize generated HTML content to a JS variable for use by the Tipue static search jQuery plugin.


Installation
------------

This plugin can be installed via:

    python -m pip install -e "git+https://github.com/getpelican/pelican-plugins/#egg=pelican-tipue-search&subdirectory=tipue_search"


Why Do You Need It?
-------------------

Static sites do not offer search feature out of the box. [Tipue Search](https://web.archive.org/web/20200703134724/https://tipue.com/search/)
is a jQuery plugin that search the static site without using any third party service, like DuckDuckGo or Google.

Tipue search requires the textual content of site in a JS variable.


How Tipue Search Works
----------------------

Tipue Search serializes the generated HTML into JSON and saves it into a JS variable. Format of JSON is as follows

```javascript
var tipuesearch = {
    "pages": [
        {
            "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer nec odio. Praesent libero. Sed cursus ante dapibus diam. Sed nisi. Nulla quis sem at nibh elementum imperdiet. Duis sagittis ipsum. Praesent mauris. Fusce nec tellus sed augue semper porta. Mauris massa. Vestibulum lacinia arcu eget nulla. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Curabitur sodales ligula in libero.",
            "tags": "Example Category",
            "url" : "http://oncrashreboot.com/plugin-example.html",
            "title": "Everything you want to know about Lorem Ipsum"
        },
        {
            "text": "Sed dignissim lacinia nunc. Curabitur tortor. Pellentesque nibh. Aenean quam. In scelerisque sem at dolor. Maecenas mattis. Sed convallis tristique sem. Proin ut ligula vel nunc egestas porttitor. Morbi lectus risus, iaculis vel, suscipit quis, luctus non, massa. Fusce ac turpis quis ligula lacinia aliquet. Mauris ipsum. Nulla metus metus, ullamcorper vel, tincidunt sed, euismod in, nibh.",
            "tags": "Example Category",
            "url" : "http://oncrashreboot.com/plugin-example-2.html",
            "title": "Review of the book Lorem Ipsum"
        }
    ]
};
```

JS variable is written to file `tipuesearch_content.js` which is created in the root of `output` directory.


How to Use
----------

Your theme needs to have Tipue Search properly configured in it. [Official documentation](https://web.archive.org/web/20200703134724/https://tipue.com/search/help/) has the required details.

In addition to the instructions from Tipue, the following has to be added in `pelicanconf.py`.

```python
DIRECT_TEMPLATES = ['index', 'tags', 'categories', 'authors', 'archives', 'search']
```

Furthermore, the generated JavaScript variable has to be sourced in the relevant HTML pages.

```html
<script src="{{ SITEURL }}tipuesearch_content.js"></script>
```

Pelican [Plumage theme](https://github.com/kdeldycke/plumage) has Tipue Search configured. Check out its code to understand the configuration.


Backward Compatibility
----------------------

This plugin requires Tipue Search Version 7.0 or higher.

Tipue used to expect content in a JSON file. Around Version 7.0, Tipue maintainers made a switch to JavaScript variable. tipue_search plugin was updated to reflect this change in commit `4a5f171fc`. Latest version of tipue_search plugin will not work with older versions of Tipue Search.

If you are using older Tipue Search, prior to 7.0 release, then you will find old version of tipue_search plugin in commit `2dcdca8c8`.


Source Archive
--------------

The Tipue Search project itself seems to have been long abandoned. There is no
longer any official canonical reference of source code or documentation. There
only some artifacts left that were archived by the community:

* [Archived Tipue Search homepage](https://web.archive.org/web/20200703134724/https://tipue.com/search/)
* [Archived Tipue plugin help page](https://web.archive.org/web/20200703134724/https://tipue.com/search/help/)
* [Archived Tipue Search code v7.1](https://web.archive.org/web/20200703134724/https://www.tipue.com/search/tipuesearch.zip)
* [GitHub repository copy](https://notabug.org/jorgesumle/Tipue-Search)
