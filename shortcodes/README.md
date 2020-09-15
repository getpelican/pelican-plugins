# pelican-shortcodes

This plugin allows to define macros called shortcodes in content pages that will be expanded as jinja2 templates.

_inspired by [lektor-shortcodes](https://github.com/skorokithakis/lektor-shortcodes)_

The purpose of this plugin is to allow explicit and quick jinja2 templating in your content without compromising markdown/rst.

# Example

    #pelicanconf.py

    SHORTCODES = {
        'image': "<img src=/images/{{src}}>{{desc|title}}<img>"""
    }

Then in your content:

    [% image src=foo.png desc="this is a test" %]

will become:

    <img src=/images/foo.png>This Is A Test<img>

# Rules

Shortcode patterns follows:

    [% shortcode_name kwarg=value kwarg="value" kwarg='value' %]

Shortcode pattern rules:

* shortcodes must be single line
* spaces are important, i.e. there should be space after `[%` and before `%]`
* shortcode_name cannot contain spaces
* kwargs are separated by a space
* kwargs can be surrounded by quotes but not necessary

# Recipes

Some shortcode examples:

    SHORTCODES = {
        # image with caption
        'image': "<img src=/images/{{src}} title={{desc}}></img><figcaption>{{desc}}</figcatpion>"

        # embed looping mp4 gifs
        'mp4gif': " <video width="480" height="240" autoplay loop muted title="{{title}}"><source src="/gifs/{{gif}}" type="video/mp4"></video>
    }

## Install

    #pelicanconf.py    
    PLUGINS = ['shortcodes']
    SHORTCODES = {
        # your shortcodes go here
        # shortcode_name: jinja2 template string
        'image': "<img src=/images/{{src}}>{{desc|title}}<img>"""
    }
    
    
