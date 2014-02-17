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
__WRAP_TAG__ = None #  the tag to wrap mathjax in (needed to play nicely with typogrify or for template designers)
__LATEX_REGEX__ = re.compile(r'(\$\$|\$|\\begin\{(.+?)\}).*?\1|\\end\{\2\}', re.DOTALL | re.IGNORECASE) #  used to detect latex

def mathjaxscript():
    # Reference about dynamic loading of MathJax can be found at http://docs.mathjax.org/en/latest/dynamic.html
    # The https cdn address can be found at http://www.mathjax.org/resources/faqs/#problem-https

    # Note: The script will be processed by the browser once, no matter how
    # many times it is declared because it checks for the existence of an id
    # before processing

    return """
<script type= "text/javascript">
    if (!document.getElementById('mathjaxscript_pelican')) {
        var s = document.createElement('script');
        s.id = 'mathjaxscript_pelican';
        s.type = 'text/javascript'; s.src = 'https:' == document.location.protocol ? 'https://c328740.ssl.cf1.rackcdn.com/mathjax/latest/MathJax.js' : 'http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML';
        s[(window.opera ? "innerHTML" : "text")] =
            "MathJax.Hub.Config({" +
            "    config: ['MMLorHTML.js']," +
            "    TeX: { extensions: ['AMSmath.js','AMSsymbols.js','noErrors.js','noUndefined.js'], equationNumbers: { autoNumber: 'AMS' } }," +
            "    jax: ['input/TeX','input/MathML','output/HTML-CSS']," +
            "    extensions: ['tex2jax.js','mml2jax.js','MathMenu.js','MathZoom.js']," +
            "    displayAlign: '"""+mathjaxscript.displayalign+"""'," +
            "    displayIndent: '"""+mathjaxscript.displayindent+"""'," +
            "    showMathMenu: """+mathjaxscript.showmathmenu+"""," +
            "    tex2jax: { " +
            "        inlineMath: [ [\'$\',\'$\'] ], " +
            "        displayMath: [ [\'$$\',\'$$\'] ]," +
            "        processEscapes: """+mathjaxscript.processescapes+"""," +
            "        preview: '"""+mathjaxscript.preview+"""'," +
            "    }, " +
            "    'HTML-CSS': { " +
            "        styles: { '.MathJax_Display, .MathJax .mo, .MathJax .mi, .MathJax .mn': {color: '""" +mathjaxscript.color+ """ ! important'}} " +
            "    } " +
            "}); ";
        (document.body || document.getElementsByTagName('head')[0]).appendChild(s);
    }
</script>
"""


# Python standard library for binary search, namely bisect
# is cool but I need specific business logic to evaluate
# my search predicate, so I am using my own version
def binarysearch(matchtuple, ignorelist):
    """
        Determines if t is within tupleList. Using
        the fact that tupleList is ordered, binary
        search can be performed which is O(logn)
    """

    ignore = False
    if ignorelist == []:
        return False

    lo = 0
    hi = len(ignorelist)-1

    # Find first value in array where predicate is False
    # predicate function: tupleList[mid][0] < t[index]
    while lo < hi:
        mid = lo + (hi-lo+1)/2
        if ignorelist[mid][0] < matchtuple[0]:
            lo = mid
        else:
            hi = mid-1

    if lo >= 0 and lo <= len(ignorelist)-1:
        ignore = (ignorelist[lo][0] <= matchtuple[0] and ignorelist[lo][1] >= matchtuple[1])

    return ignore


def ignorecontent(content):
    """
        Creates a list of match span tuples
        for which content should be ignored
        e.g. <pre> and <code> tags
    """
    ignorelist = []

    # used to detect all <pre> and <code> tags
    ignoreregex = re.compile(r'<(pre|code).*?>.*?</(\1)>', re.DOTALL | re.IGNORECASE)

    # Ignore tags that are within <code> and <pre> blocks
    for match in ignoreregex.finditer(content):
        ignorelist.append(match.span())

    return ignorelist


def wraplatex(content, ignorelist):
    """
        Wraps latex in user specified tags. This is needed for typogrify to
        play nicely with latex but it can also be styled by templated providers
    """
    wraplatex.foundlatex = False

    def mathtagwrap(match):
        """function for use in re.sub"""
        # determine if the tags are within <pre> and <code> blocks
        ignore = binarysearch(match.span(1), ignorelist) and binarysearch(match.span(2), ignorelist)

        if ignore:
            return match.group(0)
        else:
            wraplatex.foundlatex = True
            return '<%s>%s</%s>' % (__WRAP_TAG__, match.group(0), __WRAP_TAG__)

    return (__LATEX_REGEX__.sub(mathtagwrap, content), wraplatex.foundlatex)


def processsummary(instance, ignorelist):
    """
        Summaries need special care. If Latex is cut off, it must be restored.
        Also, the mathjax script must be included if necessary
    """

    processsummary.alteredsummary = False
    insertmathjaxscript = False
    endtag = '</%s>' % __WRAP_TAG__ if __WRAP_TAG__ != None else ''

    # use content's _get_summary method to obtain summary
    summary = instance._get_summary()

    # Determine if there is any math in the summary which are not within the
    # ignorelist tags
    mathitem = None
    for mathitem in processsummary.latexregex.finditer(summary):
        if binarysearch(mathitem.span(), ignorelist):
            mathitem = None # In <code> or <pre> tags, so ignore
        else:
            insertmathjaxscript = True

    # Repair the latex if it was cut off mathitem will be the final latex
    # code  matched that is not within <pre> or <code> tags
    if mathitem and mathitem.group(4) == ' ...':
        end = r'\end{%s}' % mathitem.group(3) if mathitem.group(3) is not None else mathitem.group(2)
        latexmatch = re.search('%s.*?%s' % (re.escape(mathitem.group(1)), re.escape(end)), instance._content, re.DOTALL | re.IGNORECASE)
        newsummary = summary.replace(mathitem.group(0), latexmatch.group(0)+'%s ...' % endtag)

        if newsummary != summary:
            return newsummary+mathjaxscript()

    def partialregex(match):
        """function for use in re.sub"""
        if binarysearch(match.span(), ignorelist):
            return match.group(0)

        processsummary.alteredsummary = True
        return match.group(1) + match.group(4)

    # check for partial latex tags at end. These must be removed
    summary = processsummary.latexpartialregex.sub(partialregex, summary)

    if processsummary.alteredsummary:
        return summary+mathjaxscript() if insertmathjaxscript else summary

    return summary+mathjaxscript() if insertmathjaxscript else None


def processsettings(settings):
    """
        Set user specified MathJax settings (see README for more details)
    """

    # NOTE TO FUTURE DEVELOPERS: Look at the README and what is happening in
    # this function if any additional changes to the mathjax settings need to
    # be incorporated. Also, please inline comment what the variables
    # will be used for

    # Global Variables Used To Set The Mathjax Script
    mathjaxscript.displayalign = 'center'  # controls alignment of of displayed equations (values can be: left, right, center)
    mathjaxscript.displayindent = '0em'  # if above is not set to 'center', then this setting acts as an indent
    mathjaxscript.showmathmenu = 'true'  # controls whether to attach mathjax contextual menu
    mathjaxscript.processescapes = 'true'  # controls whether escapes are processed
    mathjaxscript.preview = 'TeX'  # controls what user sees as preview
    mathjaxscript.color = 'black'  # controls color math is rendered in

    if not isinstance(settings, dict):
        return

    # The following mathjax settings can be set via the settings dictionary
    # Iterate over dictionary in a way that is compatible with both version 2
    # and 3 of python
    for key, value in ((key, settings[key]) for key in settings):
        if key == 'align' and isinstance(value, str):
            if value == 'left':
                 mathjaxscript.displayalign = 'left'
            elif value == 'right':
                 mathjaxscript.displayalign = 'right'
            else:
                 mathjaxscript.displayalign = 'center'

        if key == 'indent':
            mathjaxscript.displayindent = value

        if key == 'show_menu' and isinstance(value, bool):
            mathjaxscript.showmathmenu = 'true' if value else 'false'

        if key == 'process_escapes' and isinstance(value, bool):
            mathjaxscript.processescapes = 'true' if value else 'false'

        if key == 'preview' and isinstance(value, str):
            mathjaxscript.preview = value

        if key == 'color' and isinstance(value, str):
            mathjaxscript.color = value



def processcontent(instance):
    """
        Processes content, with logic to ensure that typogrify does not clash
        with latex. Also, mathjax script is inserted at the end of the content thereby
        making it independent of the template
    """

    if not instance._content:
        return

    ignorelist = ignorecontent(instance._content)

    if __WRAP_TAG__:
        instance._content, latex = wraplatex(instance._content, ignorelist)
    else:
        latex = True if __LATEX_REGEX__.search(instance._content) else False

    # The user initially set typogrify to be True, but since it would clash
    # with latex, we set it to False. This means that the default reader will
    # not call typogrify, so it is called here, where we are able to control
    # logic for it ignore latex if necessary
    if processcontent.typogrify:
        # Tell typogrify to ignore the tags that latex has been wrapped in
        ignoretags = [__WRAP_TAG__] if __WRAP_TAG__ else None

        # Exact copy of the logic as found in the default reader
        from typogrify.filters import typogrify
        instance._content = typogrify(instance._content, ignoretags)
        instance.metadata['title'] = typogrify(instance.metadata['title'], ignoretags)

    if latex:
        # Mathjax script added to the end of article. Now it does not need to
        # be explicitly added to the template
        instance._content += mathjaxscript()

        # The summary needs special care because latex math cannot just be cut
        # off
        summary = processsummary(instance, ignorelist)
        if summary != None:
            instance._summary = summary


def pelicaninit(pelicanobj):
    """
        Intialializes certain global variables and sets typogogrify setting to
        False should it be set to True.
    """

    global __WRAP_TAG__

    try:
        settings = pelicanobj.settings['LATEX']
    except:
        settings = None

    processsettings(settings)

    # Allows mathjax script to be accessed from template should it be needed
    pelicanobj.settings['MATHJAXSCRIPT'] = mathjaxscript()

    # If typogrify set to True, then we need to handle it manually so it does
    # not conflict with Latex
    try:
        if pelicanobj.settings['TYPOGRIFY'] == True:
            pelicanobj.settings['TYPOGRIFY'] = False
            __WRAP_TAG__ = 'mathjax' # default to wrap mathjax content inside of
            processcontent.typogrify = True
    except KeyError:
        pass

    # Set __WRAP_TAG__ to the settings tag if defined. The idea behind this is
    # to give template designers control over how math would be rendered
    try:
        if pelicanobj.settings['LATEX']['wrap']:
            __WRAP_TAG__ = pelicanobj.settings['LATEX']['wrap']
    except (KeyError, TypeError):
        pass

    # regular expressions that depend on __WRAP_TAG__ are set here
    tagstart = r'<%s>' % __WRAP_TAG__ if not __WRAP_TAG__ is None else ''
    tagend = r'</%s>' % __WRAP_TAG__ if not __WRAP_TAG__ is None else ''
    latexsummaryregex = r'((\$\$|\$|\\begin\{(.+?)\}).+?)(\2|\\end\{\3\}|\s?\.\.\.)(%s)?' % tagend
    latexpartialregex = r'(.*)(%s)(\\.*?|\$.*?)(\s?\.\.\.)(%s)' % (tagstart, tagend)

    processsummary.latexregex = re.compile(latexsummaryregex, re.DOTALL | re.IGNORECASE)
    processsummary.latexpartialregex = re.compile(latexpartialregex, re.DOTALL | re.IGNORECASE)


def register():
    """
        Plugin registration
    """
    signals.initialized.connect(pelicaninit)
    signals.content_object_init.connect(processcontent)
