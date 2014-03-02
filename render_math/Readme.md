Math Render Plugin For Pelican
==============================
This plugin gives pelican the ability to render mathematics. It accomplishes
this by using the [MathJax](http://www.mathjax.org/) javascript engine. Both
[LaTex](http://en.wikipedia.org/wiki/LaTeX) and [MathML](http://en.wikipedia.org/wiki/MathML) 
can be rendered within the content.

The plugin also ensures that pelican and recognized math "play" nicely together, by
ensuring [Typogrify](https://github.com/mintchaos/typogrify) does not alter math content
and summaries that get cut off are repaired.

Recognized math in the context of this plugin is either LaTex or MathML as described below.

### LaTex
Anything between `$`...`$` (inline math) and `$$`..`$$` (displayed math) will be recognized as
LaTex. In addition, anything the `\begin` and `\end` LaTex macros will also be 
recognized as LaTex. For example, `\begin{equation}`...`\end{equation}` would be used to 
render math equations with numbering.

Within recognized LaTex as described above, any supported LaTex macro can be used.

### MathML
Anything between `<math>` and `</math>` tags will be recognized as MathML

Installation
------------
To enable, ensure that `render_math` plugin is accessible.
Then add the following to settings.py:

    PLUGINS = ["render_math"]

Your site is now capable of rendering math math using the mathjax JavaScript
engine. No alterations to the template is needed, just use and enjoy!

### Typogrify
In the past, using [Typgogrify](https://github.com/mintchaos/typogrify) would alter the math contents resulting
in math that could not be rendered by MathJax. The only option was to ensure
that Typogrify was disabled in the settings.

The problem has been recitified in this plugin, but it requires [Typogrify version 2.04](https://pypi.python.org/pypi/typogrify)
(or higher). If this version of Typogrify is not present, the plugin will inform that an incorrect
version of Typogrify is not present and disable Typogrify for the entire site

Usage
-----
### Backward Compatibility
This plugin is backward compatible in the sense that it
will render previous setups correctly. This is because those
settings and metadata information is ignored by this version. Therefore
you can remove them to neaten up your site

### Templates
No alteration is needed to a template for this plugin to work. Just install
the plugin and start writing your Math. 

If on the other hand, you are template designer and want total control
over the MathJax JavaScript, you can set the `auto_insert` setting to 
`False` which will cause no MathJax JavaScript to be added to the content.

If you choose this option, you should really know what you are doing. Therefore
only do this if you are designing your template. There is no real advantage to
to letting template logic handle the insertion of the MathJax JavaScript other
than it being slightly neater.

By setting `auto_insert` to `False`, metadata with `key` value of `mathjax`
will be present in all pages and articles where MathJax should be present.
The template designer can detect this and then use the `MATHJAXSCRIPT` setting
which will contain the user specified MathJax script to insert into the content.

For example, this code could be used:
```
{% if not MATH['auto_insert'] %}
    {% if page and page.mathjax or article and article.mathjax %}
        {{ MATHJAXSCRIPT }}
    {% endif %}
{% endif %}
```

### Settings
Certain MathJax rendering options can be set. These options 
are in a dictionary variable called `MATH` in the pelican
settings file.

The dictionary can be set with the following keys:

 * `auto_insert`: controls whether plugin should automatically insert
MathJax JavaScript in content that has Math. It is only recommended
to set this to False if you are a template designer and you want
extra control over where the MathJax JavaScript is renderd. **Default Value**:
True
 * `wrap_latex`: controls the tags that LaTex math is wrapped with inside the resulting
html. For example, setting `wrap_latex` to `mathjax` would wrap all LaTex math inside
`<mathjax>...</mathjax>` tags. If typogrify is set to True, then math needs
to be wrapped in tags and `wrap_latex` will therefore default to `mathjax` if not
set. `wrap_latex` cannot be set to `'math'` because this tag is reserved for 
mathml notation. **Default Value**: None unless Typogrify is enabled in which case, 
it defaults to `mathjax`
 * `align`: controls how displayed math will be aligned. Can be set to either
`left`, `right` or `center`. **Default Value**: `center`.
 * `indent`: if `align` not set to `center`, then this controls the indent
level. **Default Value**: `0em`.
 * `show_menu`: a boolean value that controls whether the mathjax contextual 
menu is shown. **Default Value**: True
 * `process_escapes`: a boolean value that controls whether mathjax processes escape 
sequences. **Default Value**: True
 * `latex_preview`: controls the preview message users are seen while mathjax is
rendering LaTex. If set to `Tex`, then the TeX code is used as the preview 
(which will be visible until it is processed by MathJax). **Default Value**: `Tex`
 * `color`: controls the color of the mathjax rendered font. **Default Value**: `black`
 * `ssl`: specifies if ssl should be used to load MathJax engine. Can be set to one
of three things
  * `auto`: **Default Value** will automatically determine what protodol to use 
based on current protocol of the site. 
  * `force`: will force ssl to be used.
  * `off`: will ensure that ssl is not used

For example, in settings.py, the following would make math render in blue and
displaymath align to the left:

    MATH = {'color':'blue','align':left}

LaTex Examples
--------------
###Inline
LaTex between `$`..`$`, for example, `$`x^2`$`, will be rendered inline
with respect to the current html block.

###Displayed Math
LaTex between `$$`..`$$`, for example, `$$`x^2`$$`, will be rendered centered in a
new paragraph.

###Equations
LaTex between `\begin` and `\end`, for example, `begin{equation}` x^2 `\end{equation}`,
will be rendered centered in a new paragraph with a right justified equation number
at the top of the paragraph. This equation number can be referenced in the document.
To do this, use a `label` inside of the equation format and then refer to that label
using `ref`. For example: `begin{equation}` `\label{eq}` X^2 `\end{equation}`. Now
refer to that equation number by `$`\ref{eq}`$`.

MathML Examples
---------------
The following will render the Quadratic formula:
```
<math xmlns="http://www.w3.org/1998/Math/MathML" display="block"> 
  <mrow>
    <mi>x</mi>
    <mo>=</mo>
    <mfrac>
      <mrow>
        <mo>&#x2212;</mo>
        <mi>b</mi>
        <mo>&#xB1;</mo>
        <msqrt>
          <mrow>
            <msup>
              <mi>b</mi>
              <mn>2</mn>
            </msup>
            <mo>&#x2212;</mo>
            <mn>4</mn>
            <mi>a</mi>
            <mi>c</mi>
          </mrow>
        </msqrt>
      </mrow>
      <mrow>
        <mn>2</mn>
        <mi>a</mi>
      </mrow>
    </mfrac>
  </mrow>
</math>
```
