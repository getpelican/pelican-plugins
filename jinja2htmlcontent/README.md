# Jinja2 in HTML articles and pages

This plugin enables the use of Jinja2 directives inside Pelican 
**HTML** articles and pages. 

This plugin is a shameless rip-off the `jinja2content` plugin.
It was adapted in order to work with `.html` content files.
This enables creating complex static sites with Pelican using html
instead of Markdown, and having components split into macros and fragments.

The jinja rendering inside the content files is done before the rendering of 
the theme template files.
This means the context and jinja variables are not visible inside articles and pages.

All code that needs those variables (`article`, `category`, etc) should be
put inside the theme's template logic.  As such, the main use of this
plugin is to automatically generate parts of your articles.

## Example

We can use this plugin to create macros and fragments which are 
reusable across pages.
Let's take the following example using the excellent Semantic-UI framework:

File `mypage.md`
```
<h1 class="ui header">Join us</h1>
<div class="ui link cards">
    {% from 'card.html' import card %}
    {{ card(
        "illustration.png", 
        "Lorem ipsum",
        "Lorem ipsum dolor sit amet"  
    ) }}
...
```

Where file `card.html` contains:
```
{% macro card(img_src, title, desc) -%}
<div class="ui card">
    <div class="image">
        <img src="/theme/images/{{img_src}}">
    </div>
    <div class="content">
        <h2 class="header">
            {{title}}
        </h2>
        <p class="description">
            {{desc}}
        </p>
        <div class="extra content">
            <div class="buttons">
                <a href="/" class="ui button">Find out more</a>
            </div>
        </div>
    </div>
</div>
{%- endmacro %}
```

## Configuration

This plugin accepts the setting "JINJA2CONTENT_TEMPLATES" which should be
set to a list of paths relative to 'PATH' (the main content directory).
`jinja2htmlcontent` will look for templates inside these directories, in order.
If they are not found in any, the theme's templates folder is used.
