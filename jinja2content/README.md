# Jinja2 Content

This plugin allows the use of Jinja2 directives inside your pelican
articles and pages.  This template rendering is done before the final html
is generated, i.e. before your theme's `article.html` is applied.  This
means the context and jinja variables usually visible to your article
template **ARE NOT** available at this time.

All code that needs those variables (`article`, `category`, etc) should be
put inside the theme's template logic.  As such, the main use of this
plugin is to automatically generate parts of your articles.


## Example

One usage is to embed repetitive html code into Markdown articles.  Since
Markdown doesn't care for layout, if anything more sophisticated than just
displaying an image is necessary, one is forced to embed html in Markdown
articles (at the very least, hardcode `<div>` tags and then select them
from the theme's CSS).  However, with `jinja2content`, one can do the
following.

File `my-cool-article.md`
```
# My cool title

My cool content.

{% from 'img_desc.html' import img_desc %}
{{ img_desc("/images/my-cool-image.png",
    "This is a cool tooltip",
    "This is a very cool image.") }}
```

Where file `img_desc.html` contains:
```
{% macro img_desc(src, title='', desc='') -%}
<div class="img-desc">
  <p><img src="{{ src }}" title="{{ title }}"></p>
  {% if desc %}
  <p><em>{{ desc }}</em></p>
  {% endif %}
</div>
{%- endmacro %}
```

The result will be:
```
# My cool title

My cool content.

<div class="img-desc">
  <p><img src="/images/my-cool-image.png" title="This is a cool tooltip"></p>
  <p><em>This is a very cool image.</em></p>
</div>
```

After this, the Markdown will be rendered into html and only then the
theme's templates will be applied.

In this way, Markdown articles have more control over the content that is
passed to the theme's `article.html` template, without the need to pollute
the Markdown with html.  Another added benefit is that now `img_desc` is
reusable across articles.

Note that templates rendered with `jinja2content` can contain Markdown as
well as html, since they are added before the Markdown content is converted
to html.


## Configuration

This plugin accepts the setting "JINJA2CONTENT_TEMPLATES" which should be
set to a list of paths relative to 'PATH' (the main content directory).
`jinja2content` will look for templates inside these directories, in order.
If they are not found in any, the theme's templates folder is used.


## Notes

+ Only Markdown supported at this moment.  Adding .rst support shouldn't be
  too hard, and you can ask for it by opening an issue.
+ This plugin is intended to replace
  [pelican-jinj2content](https://github.com/joachimneu/pelican-jinja2content/tree/f73ef9b1ef1ee1f56c80757b4190b53f8cd607d1)
  which hasn't been developed in a while and generated empty `<p>` tags in
  the final html output.
