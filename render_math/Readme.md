Math Render Plugin For Pelican
==============================

**NOTE: [This plugin has been moved to its own repository](https://github.com/pelican-plugins/render-math). Please file any issues/PRs there. Once all plugins have been migrated to the [new Pelican Plugins organization](https://github.com/pelican-plugins), this monolithic repository will be archived.**

This plugin gives pelican the ability to render mathematics. It accomplishes
this by using the [MathJax](http://www.mathjax.org/) javascript engine.

The plugin also ensures that Typogrify and recognized math "play" nicely together, by
ensuring [Typogrify](https://github.com/mintchaos/typogrify) does not alter math content.

Both Markdown and reStructuredText is supported.

Requirements
------------

  * Pelican version *3.6* or above is required.
  * Typogrify version *2.0.7* or higher is needed for Typogrify to play
    "nicely" with this plugin. If this version is not available, Typogrify
    will be disabled for the entire site.
  * BeautifulSoup4 is required to correct summaries. If BeautifulSoup4 is
    not installed, summary processing will be ignored, even if specified
    in user settings.

Installation
------------
To enable, ensure that `render_math` plugin is accessible.
Then add the following to settings.py:

    PLUGINS = ["render_math"]

Your site is now capable of rendering math math using the mathjax JavaScript
engine. No alterations to the template is needed, just use and enjoy!

However, if you wish, you can set the `auto_insert` setting to `False` which
will disable the mathjax script from being automatically inserted into the
content. You would only want to do this if you had control over the template
and wanted to insert the script manually.

### Typogrify
In the past, using [Typgogrify](https://github.com/mintchaos/typogrify) would
alter the math contents resulting in math that could not be rendered by MathJax.
The only option was to ensure that Typogrify was disabled in the settings.

The problem has been rectified in this plugin, but it requires at a minimum
[Typogrify version 2.0.7](https://pypi.python.org/pypi/typogrify) (or higher).
If this version is not present, the plugin will disable Typogrify for the entire
site.

### BeautifulSoup4
Pelican creates summaries by truncating the contents to a specified user length.
The truncation process is oblivious to any math and can therefore destroy
the math output in the summary.

To restore math, [BeautifulSoup4](https://pypi.python.org/pypi/beautifulsoup4/4.4.0)
is used. If it is not installed, no summary processing will happen.

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
 * `auto_insert`: [boolean] will insert the mathjax script into content that it is
detected to have math in it. Setting it to false is not recommended.
**Default Value**: `True`
 * `indent`: [string] if `align` not set to `'center'`, then this controls the indent
level. **Default Value**: `'0em'`.
 * `show_menu`: [boolean] controls whether the mathjax contextual menu is shown.
**Default Value**: `True`
 * `process_escapes`: [boolean] controls whether mathjax processes escape sequences.
**Default Value**: `True`
 * `mathjax_font`: [string] will force mathjax to use the chosen font. Current choices
for the font is `sanserif`, `typewriter` or `fraktur`. If this is not set, it will
use the default font settings. **Default Value**: `default`
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
 * `process_summary`: [boolean] ensures math will render in summaries and fixes math in that were cut off.
Requires [BeautifulSoup4](http://www.crummy.com/software/BeautifulSoup/bs4/doc/) be installed. **Default Value**: `True`
 * `message_style`: [string] This value controls the verbosity of the messages in the lower left-hand corner. Set it to `None` to eliminate all messages.
**Default Value**: normal

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

### Inlined Math
Math between `$`..`$`, for example, `$`x^2`$`, will be rendered inline
with respect to the current html block. Note: To use inline math, there
must *not* be any whitespace before the ending `$`. So for example:

 * **Relevant inline math**: `$e=mc^2$`
 * **Will not render as inline math**: `$40 vs $50`

### Displayed Math
Math between `$$`..`$$` will be rendered "block style", for example, `$$`x^2`$$`, will be rendered centered in a
new paragraph.

#### Other Latex  Display Math commands
The other LaTeX commands which usually invoke display math mode from text mode
are supported,
and are automatically treated like `$$`-style displayed math 
in that they are rendered "block" style on their own lines.
For example, `\begin{equation}` x^2 `\end{equation}`,
will be rendered in its own block with a right justified equation number
at the top of the block. This equation number can be referenced in the document.
To do this, use a `label` inside of the equation format and then refer to that label
using `ref`. For example: `\begin{equation}` `\label{eq}` X^2 `\end{equation}`. 
Now refer to that equation number by `$`\ref{eq}`$`.

reStructuredText
----------------
If there is math detected in reStructuredText document, the plugin will automatically
set the [math_output](http://docutils.sourceforge.net/docs/user/config.html#math-output) configuration setting to `MathJax`.

### Inlined Math
Inlined math needs to use the [math role](http://docutils.sourceforge.net/docs/ref/rst/roles.html#math):

```
The area of a circle is :math:`A_\text{c} = (\pi/4) d^2`.
```

### Displayed Math
Displayed math uses the [math block](http://docutils.sourceforge.net/docs/ref/rst/directives.html#math):

```
.. math::

  α_t(i) = P(O_1, O_2, … O_t, q_t = S_i λ)
```
