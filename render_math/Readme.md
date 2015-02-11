Math Render Plugin For Pelican
==============================
This plugin gives pelican the ability to render mathematics. It accomplishes
this by using the [MathJax](http://www.mathjax.org/) javascript engine.

The plugin also ensures that Typogrify and recognized math "play" nicely together, by
ensuring [Typogrify](https://github.com/mintchaos/typogrify) does not alter math content.
It requires at a minimum Pelican version *3.5* and Typogrify version *2.0.7* to work.
If these versions are not available, Typogrify will be disabled for the entire site.

Both Markdown and reStructuredText is supported.

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

The problem has been recitified in this plugin, but it requires [Typogrify version 2.0.7](https://pypi.python.org/pypi/typogrify)
(or higher) and Pelican version 3.5 or higher. If these versions are not present, the plugin will disable
Typogrify for the entire site

Usage
-----
### Templates
No alteration is needed to a template for this plugin to work. Just install
the plugin and start writing your Math. 

### Settings
Certain MathJax rendering options can be set. These options 
are in a dictionary variable called `MATH_JAX` in the pelican
settings file.

The dictionary can be set with the following keys:

 * `align`: [string] controls how displayed math will be aligned. Can be set to either
`'left'`, `'right'` or `'center'`. **Default Value**: `'center'`.
 * `indent`: [string] if `align` not set to `'center'`, then this controls the indent
level. **Default Value**: `'0em'`.
 * `show_menu`: [boolean] controls whether the mathjax contextual menu is shown.
**Default Value**: `True`
 * `process_escapes`: [boolean] controls whether mathjax processes escape sequences.
**Default Value**: `True`
 * `latex_preview`: [string] controls the preview message users are shown while mathjax is
rendering LaTex. If set to `'Tex'`, then the TeX code is used as the preview 
(which will be visible until it is processed by MathJax). **Default Value**: `'Tex'`
 * `color`: [string] controls the color of the mathjax rendered font. **Default Value**: `'inherit'`
 * `linebreak_automatic`: [boolean] If set, Mathjax will try to *intelligently* break up displayed math
(Note: It will not work for inline math). This is very useful for a responsive site. It
is turned off by default due to it potentially being CPU expensive. **Default Value**: `False`
 * `tex_extensions`: [list] a list of [latex extensions](http://docs.mathjax.org/en/latest/tex.html#tex-and-latex-extensions)
accepted by mathjax. **Default Value**: `[]` (empty list)
 * `responsive`: [boolean] tries to make displayed math render responsively. It does by determining if the width
is less than `responsive_break` (see below) and if so, sets `align` to `left`, `indent` to `0em` and `linebreak_automatic` to `True`.
**Default Value**: `False` (defaults to `False` for backward compatibility)
 * `responsive_break`: [integer] a number (in pixels) representing the width breakpoint that is used
when setting `responsive_align` to `True`. **Default Value**: 768

#### Settings Examples
Make math render in blue and displaymath align to the left:

    MATH_JAX = {'color':'blue','align':left}

Use the [color](http://docs.mathjax.org/en/latest/tex.html#color) and
[mhchem](http://docs.mathjax.org/en/latest/tex.html#mhchem) extensions:
    
    MATH_JAX = {'tex_extensions': ['color.js','mhchem.js']}

#### Resulting HTML
Inlined math is wrapped in `span` tags, while displayed math is wrapped in `div` tags.
These tags will have a class attribute that is set to `math` which 
can be used by template designers to alter the display of the math.

Markdown
--------
This plugin implements a custom extension for markdown resulting in math
being a "first class citizen" for Pelican. 

###Inlined Math
Math between `$`..`$`, for example, `$`x^2`$`, will be rendered inline
with respect to the current html block. Note: To use inline math, there
must *not* be any whitespace before the ending `$`. So for example:

 * **Relevant inline math**: `$e=mc^2$`
 * **Will not render as inline math**: `$40 vs $50`

###Displayed Math
Math between `$$`..`$$`, for example, `$$`x^2`$$`, will be rendered centered in a
new paragraph.

###Latex Macros
Latex macros are supported, and are automatically treated like displayed math 
(i.e. it is wrapped in `div` tag). For example, `begin{equation}` x^2 `\end{equation}`,
will be rendered in its own block with a right justified equation number
at the top of the block. This equation number can be referenced in the document.
To do this, use a `label` inside of the equation format and then refer to that label
using `ref`. For example: `begin{equation}` `\label{eq}` X^2 `\end{equation}`. Now
refer to that equation number by `$`\ref{eq}`$`.

reStructuredText
----------------
If there is math detected in reStructuredText document, the plugin will automatically
set the [math_output](http://docutils.sourceforge.net/docs/user/config.html#math-output) configuration setting to `MathJax`.

###Inlined Math
Inlined math needs to use the [math role](http://docutils.sourceforge.net/docs/ref/rst/roles.html#math):

```
The area of a circle is :math:`A_\text{c} = (\pi/4) d^2`.
```

###Displayed Math
Displayed math uses the [math block](http://docutils.sourceforge.net/docs/ref/rst/directives.html#math):

```
.. math::

  α_t(i) = P(O_1, O_2, … O_t, q_t = S_i λ)
```
