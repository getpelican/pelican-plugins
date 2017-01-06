# Glossary

Builds a glossary page containing definition lists found in articles.


## Example

If you have an article (Markdown or ReST) that generates the following:

file `defns.html` titled "My definitions"
```
<dl>
  <dt>My Term</dt>
  <dd>This is definition for My Term.</dd>
  <dt>Another Term</dt>
  <dd>And another definition.</dd>
</dl>
```

This plugin will do two things. First, it will add an anchor to the
beginning of the <dl> tag, like so:

file `defns.html` titled "My definitions"
```
<a name="another-term"></a>
<a name="my-term"></a>
<dl>
  <dt>My Term</dt>
  <dd>This is definition for My Term.</dd>
  <dt>Another Term</dt>
  <dd>And another definition.</dd>
</dl>
```

Second, it will extract all such definitions and put them inside the
`definitions` variable in the pelican context. It will be seen by all page
templates.

The `definitions` variable will have the following attributes:
+ `title`, the definition title, inside <dt> tags,
+ `definition`, the definition, inside <dd> tags,
+ `anchor`, the text inside the `name` attribute for the anchor link,
+ `source`, the article or page that contains this definition list,
+ `see_also`, containing a list of objects just like this one, made from
  other definitions in the same list.

For example, for the above html code, the `definitions` variable would look
like the following:

```
definitions = [obj1, obj2]
obj1.title = "My Term"
obj1.definition = "This is definition for My Term."
obj1.anchor = 'my-term'
obj1.source = <Content object pointing to "My definitions" file>
obj1.see_also = [obj2]

obj2.title = "Another Term"
obj2.definition = "And another definition."
obj2.link = 'another-term'
obj2.source = <Content object pointing to "My definitions" file>
obj2.see_also = [obj1]
```


## Usage

Next is an example usage of the `definitions` variable.

glossary.html
```
{% for def in definitions | sort(attribute='title') %}
<dl>
  <a name="{{ def.anchor }}"></a>
  <dt><h4>{{ def.title }}</h4></dt>
  <dd>
    <p>{{ def.definition }}</p>
    <p><i>
      <span>Defined in: <a href="{{ def.source.url }}#{{ def.anchor }}">{{ def.source.title }}</a>.</span>
      {% if def.see_also %}
      <span> See also: </span>
      {% for also in def.see_also %}
      <span><a href="{{ output_file }}#{{ also.anchor }}">{{ also.title }}</a>{% if not loop.last %}, {% else %}.{% endif %}</span>
      {% endfor%}
      {% endif %}
    </i></p>
  </dd>
</dl>
```

This example generates new anchors in the glossary page, so that navigation
through the `see also` links is done inside the same page, as well as link
to the source page (with the correct anchor too).
>>>>>>> Stashed changes

## Notes

+ The `glossary` plugin supports the use of a `GLOSSARY_EXCLUDE` setting,
  which can be set to an arbitrary list in your `pelicanconf.py`. By
  default, it's equal to the empty list. `glossary` will add to
  `definitions` all definitions **EXCEPT** those whose title is found
  inside `GLOSSARY_EXCLUDE`.
