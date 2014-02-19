# -*- coding: utf-8 -*-
"""
Latex Plugin For Pelican
========================

This plugin allows you to write mathematical equations in your articles using Latex.
It uses the MathJax Latex JavaScript library to render latex that is embedded in
between `$..$` for inline math and `$$..$$` for displayed math. It also allows for
writing equations in by using `\begin{equation}`...`\end{equation}`. No
alteration to a template is required for this plugin to work, just install and
use.

Typogrify Compatibility
-----------------------
This plugin now plays nicely with typogrify, but it requires
typogrify version 2.07 or above.

User Settings
-------------
Users are also able to pass a dictionary of settings in the settings file which
will control how the mathjax library renders thing. This could be very useful
for template builders that want to adjust look and feel of the math.
See README for more details.
"""

from pelican import signals
from pelican import contents
import re

# Global Variables
_TYPOGRIFY = False  # used to determine if we should process typogrify
_WRAP_TAG = None  # the tag to wrap mathjax in (needed to play nicely with typogrify or for template designers)
_LATEX_REGEX = re.compile(r'(\$\$|\$|\\begin\{(.+?)\}|<(math).*?>).*?(\1|\\end\{\2\}|</\3>)', re.DOTALL | re.IGNORECASE) #  used to detect latex
_LATEX_SUMMARY_REGEX = None  # used to match latex in summary
_LATEX_PARTIAL_REGEX = None  # used to match latex that has been cut off in summary
_MATHJAX_SETTINGS = {}  # settings that can be specified by the user, used to control mathjax script settings
_MATHJAX_SCRIPT="""
<script type= "text/javascript">
    if (!document.getElementById('mathjaxscript_pelican')) {{
        var s = document.createElement('script');
        s.id = 'mathjaxscript_pelican';
        s.type = 'text/javascript'; s.src = 'https:' == document.location.protocol ? 'https://c328740.ssl.cf1.rackcdn.com/mathjax/latest/MathJax.js' : 'http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML';
        s[(window.opera ? "innerHTML" : "text")] =
            "MathJax.Hub.Config({{" +
            "    config: ['MMLorHTML.js']," +
            "    TeX: {{ extensions: ['AMSmath.js','AMSsymbols.js','noErrors.js','noUndefined.js'], equationNumbers: {{ autoNumber: 'AMS' }} }}," +
            "    jax: ['input/TeX','input/MathML','output/HTML-CSS']," +
            "    extensions: ['tex2jax.js','mml2jax.js','MathMenu.js','MathZoom.js']," +
            "    displayAlign: '{align}'," +
            "    displayIndent: '{indent}'," +
            "    showMathMenu: {show_menu}," +
            "    tex2jax: {{ " +
            "        inlineMath: [ [\'$\',\'$\'] ], " +
            "        displayMath: [ [\'$$\',\'$$\'] ]," +
            "        processEscapes: {process_escapes}," +
            "        preview: '{preview}'," +
            "    }}, " +
            "    'HTML-CSS': {{ " +
            "        styles: {{ '.MathJax_Display, .MathJax .mo, .MathJax .mi, .MathJax .mn': {{color: '{color} ! important'}} }}" +
            "    }} " +
            "}}); ";
        (document.body || document.getElementsByTagName('head')[0]).appendChild(s);
    }}
</script>
"""


# Python standard library for binary search, namely bisect is cool but I need
# specific business logic to evaluate my search predicate, so I am using my
# own version
def binary_search(match_tuple, ignore_within):
    """Determines if t is within tupleList. Using the fact that tupleList is
    ordered, binary search can be performed which is O(logn)
    """

    ignore = False
    if ignore_within == []:
        return False

    lo = 0
    hi = len(ignore_within)-1

    # Find first value in array where predicate is False
    # predicate function: tupleList[mid][0] < t[index]
    while lo < hi:
        mid = lo + (hi-lo+1)/2
        if ignore_within[mid][0] < match_tuple[0]:
            lo = mid
        else:
            hi = mid-1

    if lo >= 0 and lo <= len(ignore_within)-1:
        ignore = (ignore_within[lo][0] <= match_tuple[0] and ignore_within[lo][1] >= match_tuple[1])

    return ignore


def ignore_content(content):
    """Creates a list of match span tuples for which content should be ignored
    e.g. <pre> and <code> tags
    """
    ignore_within = []

    # used to detect all <pre> and <code> tags. NOTE: Alter this regex should
    # additional tags need to be ignored
    ignore_regex = re.compile(r'<(pre|code).*?>.*?</(\1)>', re.DOTALL | re.IGNORECASE)

    for match in ignore_regex.finditer(content):
        ignore_within.append(match.span())

    return ignore_within


def wrap_latex(content, ignore_within):
    """Wraps latex in user specified tags.

    This is needed for typogrify to play nicely with latex but it can also be
    styled by template providers
    """
    wrap_latex.foundlatex = False

    def math_tag_wrap(match):
        """function for use in re.sub"""

        # determine if the tags are within <pre> and <code> blocks
        ignore = binary_search(match.span(1), ignore_within) and binary_search(match.span(2), ignore_within)

        if ignore or match.group(3) == 'math':
            if match.group(3) == 'math':
                # Will detect mml, but not wrap anything around it
                wrap_latex.foundlatex = True

            return match.group(0)
        else:
            wrap_latex.foundlatex = True
            return '<%s>%s</%s>' % (_WRAP_TAG, match.group(0), _WRAP_TAG)

    return (_LATEX_REGEX.sub(math_tag_wrap, content), wrap_latex.foundlatex)


def process_summary(instance, ignore_within):
    """Summaries need special care. If Latex is cut off, it must be restored.

    In addition, the mathjax script must be included if necessary thereby
    making it independent to the template
    """

    process_summary.altered_summary = False
    insert_mathjax_script = False
    end_tag = '</%s>' % _WRAP_TAG if _WRAP_TAG != None else ''

    # use content's _get_summary method to obtain summary
    summary = instance._get_summary()

    # Determine if there is any math in the summary which are not within the
    # ignore_within tags
    mathitem = None
    for mathitem in _LATEX_SUMMARY_REGEX.finditer(summary):
        if binary_search(mathitem.span(), ignore_within):
            mathitem = None # In <code> or <pre> tags, so ignore
        else:
            insert_mathjax_script = True

    # Repair the latex if it was cut off mathitem will be the final latex
    # code  matched that is not within <pre> or <code> tags
    if mathitem and '...' in mathitem.group(6):
        if mathitem.group(3) is not None:
            end = r'\end{%s}' % mathitem.group(3)
        elif mathitem.group(4) is not None:
            end = r'</math>'
        elif mathitem.group(2) is not None:
            end = mathitem.group(2)

        search_regex = r'%s(%s.*?%s)' % (re.escape(instance._content[0:mathitem.start(1)]), re.escape(mathitem.group(1)), re.escape(end))
        latex_match = re.search(search_regex, instance._content, re.DOTALL | re.IGNORECASE)

        if latex_match:
            new_summary = summary.replace(mathitem.group(0), latex_match.group(1)+'%s ...' % end_tag)

            if new_summary != summary:
                return new_summary+_MATHJAX_SCRIPT.format(**_MATHJAX_SETTINGS)

    def partial_regex(match):
        """function for use in re.sub"""
        if binary_search(match.span(3), ignore_within):
            return match.group(0)

        process_summary.altered_summary = True
        return match.group(1) + match.group(4)

    # check for partial latex tags at end. These must be removed

    summary = _LATEX_PARTIAL_REGEX.sub(partial_regex, summary)

    if process_summary.altered_summary:
        return summary+_MATHJAX_SCRIPT.format(**_MATHJAX_SETTINGS) if insert_mathjax_script else summary

    return summary+_MATHJAX_SCRIPT.format(**_MATHJAX_SETTINGS) if insert_mathjax_script else None


def process_settings(settings):
    """Sets user specified MathJax settings (see README for more details)"""

    global _MATHJAX_SETTINGS

    # NOTE TO FUTURE DEVELOPERS: Look at the README and what is happening in
    # this function if any additional changes to the mathjax settings need to
    # be incorporated. Also, please inline comment what the variables
    # will be used for

    # Default settings
    _MATHJAX_SETTINGS['align'] = 'center'  # controls alignment of of displayed equations (values can be: left, right, center)
    _MATHJAX_SETTINGS['indent'] = '0em'  # if above is not set to 'center', then this setting acts as an indent
    _MATHJAX_SETTINGS['show_menu'] = 'true'  # controls whether to attach mathjax contextual menu
    _MATHJAX_SETTINGS['process_escapes'] = 'true'  # controls whether escapes are processed
    _MATHJAX_SETTINGS['preview'] = 'TeX'  # controls what user sees as preview
    _MATHJAX_SETTINGS['color'] = 'black'  # controls color math is rendered in

    if not isinstance(settings, dict):
        return

    # The following mathjax settings can be set via the settings dictionary
    # Iterate over dictionary in a way that is compatible with both version 2
    # and 3 of python
    for key, value in ((key, settings[key]) for key in settings):
        if key == 'align' and isinstance(value, str):
            if value == 'left' or value == 'right' or value == 'center':
                _MATHJAX_SETTINGS[key] = value
            else:
                _MATHJAX_SETTINGS[key] = 'center'

        if key == 'indent':
            _MATHJAX_SETTINGS[key] = value

        if key == 'show_menu' and isinstance(value, bool):
            _MATHJAX_SETTINGS[key] = 'true' if value else 'false'

        if key == 'process_escapes' and isinstance(value, bool):
            _MATHJAX_SETTINGS[key] = 'true' if value else 'false'

        if key == 'preview' and isinstance(value, str):
            _MATHJAX_SETTINGS[key] = value

        if key == 'color' and isinstance(value, str):
            _MATHJAX_SETTINGS[key] = value


def process_content(instance):
    """Processes content, with logic to ensure that typogrify does not clash
    with latex.

    In addition, mathjax script is inserted at the end of the content thereby
    making it independent of the template
    """

    if not instance._content:
        return

    ignore_within = ignore_content(instance._content)

    if _WRAP_TAG:
        instance._content, latex = wrap_latex(instance._content, ignore_within)
    else:
        latex = True if _LATEX_REGEX.search(instance._content) else False

    # The user initially set typogrify to be True, but since it would clash
    # with latex, we set it to False. This means that the default reader will
    # not call typogrify, so it is called here, where we are able to control
    # logic for it ignore latex if necessary
    if _TYPOGRIFY:
        # Tell typogrify to ignore the tags that latex has been wrapped in
        # also, typogrify must always ignore mml (math) tags
        ignore_tags = [_WRAP_TAG,'math'] if _WRAP_TAG else ['math']

        # Exact copy of the logic as found in the default reader
        from typogrify.filters import typogrify
        instance._content = typogrify(instance._content, ignore_tags)
        instance.metadata['title'] = typogrify(instance.metadata['title'], ignore_tags)

    if latex:
        # Mathjax script added to the end of article. Now it does not need to
        # be explicitly added to the template
        instance._content += _MATHJAX_SCRIPT.format(**_MATHJAX_SETTINGS)

        # The summary needs special care because latex math cannot just be cut
        # off
        summary = process_summary(instance, ignore_within)
        if summary != None:
            instance._summary = summary


def pelican_init(pelicanobj):
    """Intialializes certain global variables and sets typogogrify setting to
    False should it be set to True.
    """

    global _TYPOGRIFY
    global _WRAP_TAG
    global _LATEX_SUMMARY_REGEX
    global _LATEX_PARTIAL_REGEX

    try:
        settings = pelicanobj.settings['LATEX']
    except:
        settings = None

    process_settings(settings)

    # Allows mathjax script to be accessed from template should it be needed
    pelicanobj.settings['MATHJAXSCRIPT'] = _MATHJAX_SCRIPT.format(**_MATHJAX_SETTINGS)

    # If typogrify set to True, then we need to handle it manually so it does
    # not conflict with Latex
    try:
        if pelicanobj.settings['TYPOGRIFY'] == True:
            pelicanobj.settings['TYPOGRIFY'] = False
            _WRAP_TAG = 'mathjax' # default to wrap mathjax content inside of
            _TYPOGRIFY = True
    except KeyError:
        pass

    # Set _WRAP_TAG to the settings tag if defined. The idea behind this is
    # to give template designers control over how math would be rendered
    try:
        if pelicanobj.settings['LATEX']['wrap']:
            _WRAP_TAG = pelicanobj.settings['LATEX']['wrap']
    except (KeyError, TypeError):
        pass

    # regular expressions that depend on _WRAP_TAG are set here
    tag_start= r'<%s>' % _WRAP_TAG if not _WRAP_TAG is None else ''
    tag_end = r'</%s>' % _WRAP_TAG if not _WRAP_TAG is None else ''
    latex_summary_regex = r'((\$\$|\$|\\begin\{(.+?)\}|<(math)(\s.*?)?>).+?)(\2|\\end\{\3\}|\s?\.\.\.)(%s|</\4>)?' % tag_end

    # NOTE: The logic in _get_summary will handle <math> correctly because it
    # is perceived as an html tag. Therefore we are only interested in handling non mml
    latex_partial_regex = r'(.*)(%s)(\\\S*?|\$)\s*?(\s?\.\.\.)(%s)?$' % (tag_start, tag_end)

    _LATEX_SUMMARY_REGEX = re.compile(latex_summary_regex, re.DOTALL | re.IGNORECASE)
    _LATEX_PARTIAL_REGEX = re.compile(latex_partial_regex, re.DOTALL | re.IGNORECASE)


def register():
    """Plugin registration"""

    signals.initialized.connect(pelican_init)
    signals.content_object_init.connect(process_content)
