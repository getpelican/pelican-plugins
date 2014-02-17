Latex Plugin For Pelican
========================

This plugin allows you to write mathematical equations in your articles using Latex.
It uses the MathJax Latex JavaScript library to render latex that is embedded in
between `$..$` for inline math and `$$..$$` for displayed math. It also allows for
writing equations in by using `\begin{equation}`...`\end{equation}`.

Installation
------------
To enable, ensure that `latex.py` is put somewhere that is accessible.
Then use as follows by adding the following to your settings.py:

    PLUGINS = ["latex"]

Your site is now capable of rendering latex math using the mathjax JavaScript
library. No alterations to the template file is needed.

### Typogrify
Typogrify will now play nicely with Latex (i.e. typogrify can be enabled
and Latex will be rendered correctly). In order for this to happen,
version 2.07 (or above) of typogrify is required. In fact, this plugin expects
that at least version 2.07 is present and will fail without it.

Usage
-----
### Bakcward Compatibility
This plugin is backward compatible in the sense that it
accompishes what previous versions did without needing any setup in the
metadata or settings files.

### Settings File
Extra options regarding how mathjax renders latex can be set in the settings
file. These options are in a dictionary variable called `LATEX` in the pelican
settings file.

The dictionary can be set with the following keys:

 * `wrap`: controls the tags that math is wrapped with inside the resulting
html. For example, setting `wrap` to `'mathjax'` would wrap all math inside
`<mathjax>...</mathjax>` tags. If typogrify is set to True, then math needs
to be wrapped in tags and `wrap` will therefore default to `mathjax` if not
set.
 * `align`: controls how displayed math will be aligned. Can be set to either
`left`, `right` or `center` (default is `center`).
 * `indent`: if `align` not set to `center`, then this controls the indent
level (default is `0em`).
 * `show_menu`: controls whether the mathjax contextual menu is shown.
 * `process_escapes`: controls whether mathjax processes escape sequences.
 * `preview`: controls the preview message users are seen while mathjax is
loading.
 * `color`: controls the color of the mathjax rendered font.

For example, in settings.py, the following would make latex render in blue and
displaymath align to the left:

    LATEX = {'color':'blue','align':left}

Latex Examples
--------------
###Inline
Latex between `$`..`$`, for example, `$`x^2`$`, will be rendered inline
with respect to the current html block.

###Displayed Math
Latex between `$$`..`$$`, for example, `$$`x^2`$$`, will be rendered centered in a
new paragraph.

###Equations
Latex between `\begin` and `\end`, for example, `begin{equation}` x^2 `\end{equation}`,
will be rendered centered in a new paragraph with a right justified equation number
at the top of the paragraph. This equation number can be referenced in the document.
To do this, use a `label` inside of the equation format and then refer to that label
using `ref`. For example: `begin{equation}` `\label{eq}` X^2 `\end{equation}`. Now
refer to that equation number by `$`\ref{eq}`$`.
