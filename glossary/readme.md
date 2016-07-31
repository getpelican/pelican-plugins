# Glossary

Builds a glossary page containing definition lists found in articles and
pages.


## Example

If you have an article or page that generates the following:

file `defns.html` titled "My definitions"
```
<dl>
  <dt><a href="some-link.html">My Term</a></dt>
  <dd>This is definition for My Term.</dd>
  <dt>Another Term</dt>
  <dd>And another definition.</dd>
</dl>
```

This plugin will extract all such definitions and put them inside the
`definitions` variable in the pelican context. It will be seen by all page
templates.

The `definitions` variable will have the following attributes:
+ `title`, the definition title, inside <dt> tags,
+ `definition`, the definition, inside <dd> tags,
+ `link`, if the <dt> tags enclose a <a> tag, it will be stored here, or
  None,
+ `source`, the article or page that contains this definition list,
+ `see_also`, containing a list of dicts just like this, made from other
  definitions in the same list.

For example, for the above html code, the `definitions` variable would look
like the following:

```
definitions = [dict1, dict2]
dict1.title = "My Term"
dict1.definition = "This is definition for My Term."
dict1.link = 'some-link.html'
dict1.source = <content Object referring to "My definitions">
dict1.see_also = [dict2]

dict2.title = "Another Term"
dict2.definition = "And another definition."
dict2.link = None
dict2.source = <content Object referring to "My definitions">
dict2.see_also = [dict1]
```

Note the `link` attribute does not necessarily point to `source.url`.


## Usage

Next is an example usage of the `definitions` variable.

```
{% for def in definitions | sort(attribute='title') %}
<dl>
  <dt>{{ def.title }}</dt>
  <dd>
    <p>{{ def.definition }}</p>
    <p>
    Defined in:
    {% if def.link %}<a href="{{ def.link }}">{% endif %}
    {{ def.source.title }}
    {% if def.link %}</a>{% endif %}.

    {% if def.see_also %}
    See also:
    {% for also in def.see_also %}
    <a href="{{ also.link }}">{{ also.title }}</a>
    {% endfor%}
    {% endif %}
    </p>
  </dd>
</dl>
{% endfor %}
```

## Notes

+ The `glossary` plugin supports the use of a `GLOSSARY_EXCLUDE` setting,
  which can be set to an arbitrary list in your `pelicanconf.py`. By
  default, it's equal to the empty list. `glossary` will add to
  `definitions` all definitions **EXCEPT** those whose title is found
  inside `GLOSSARY_EXCLUDE`.
