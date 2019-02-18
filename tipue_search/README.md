Tipue Search
============

A Pelican plugin to serialize generated HTML to a JS variable that can be used by jQuery plugin - Tipue Search.

Copyright (c) Talha Mansoor

Author          | Talha Mansoor
----------------|-----
Author Email    | talha131@gmail.com 
Author Homepage | http://onCrashReboot.com 
Github Account  | https://github.com/talha131 

Why do you need it?
===================

Static sites do not offer search feature out of the box. [Tipue Search](http://www.tipue.com/search/)
is a jQuery plugin that search the static site without using any third party service, like DuckDuckGo or Google.

Tipue search requires the textual content of site in a JS variable.

Requirements
============

Tipue Search requires BeautifulSoup.

```bash
pip install beautifulsoup4
```

How Tipue Search works
=========================

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

How to use
==========

Your theme needs to have Tipue Search properly configured in it. [Official documentation](http://www.tipue.com/search/help/) has the required details.

In addition to the instructions from Tipue, the following has to be added in `pelicanconf.py`.

```python
PLUGIN_PATH = 'plugins'
PLUGINS = ['tipue_search']
DIRECT_TEMPLATES = ['index', 'tags', 'categories', 'authors', 'archives', 'search']
```

Furthermore, the generated JavaScript variable has to be sourced in the relevant html pages.

```html
<script src="{{ SITEURL }}tipuesearch_content.js"></script>
```

Pelican [Elegant Theme](https://github.com/talha131/pelican-elegant) and [Plumage theme](https://github.com/kdeldycke/plumage) have Tipue Search configured. You can view their code to understand the configuration.

Backward Compatibility
======================

This plugin requires Tipue Search Version 7.0 or higher.

Tipue used to expect content in a json file. Around Version 7.0, Tipue maintainers made a switch to JavaScript variable. tipue_search plugin was updated to reflect this change in commit `4a5f171fc`. Latest version of tipue_search plugin will not work with older versions of Tipue Search.

If you are using older Tipue Search, prior to 7.0 release, then you will find old version of tipue_search plugin in commit `2dcdca8c8`. 
