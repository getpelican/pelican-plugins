# -*- coding: utf-8 -*-
"""
Math Render Plugin for Pelican
==============================
This plugin allows your site to render Math. It supports both LaTeX and MathML
using the MathJax JavaScript engine.

Typogrify Compatibility
-----------------------
This plugin now plays nicely with Typogrify, but it requires
Typogrify version 2.04 or above.

User Settings
-------------
Users are also able to pass a dictionary of settings in the settings file which
will control how the MathJax library renders things. This could be very useful
for template builders that want to adjust the look and feel of the math.
See README for more details.
"""

import os
import re

from pelican import signals
from pelican import contents


# Global Variables
_TYPOGRIFY = None  # if Typogrify is enabled, this is set to the typogrify.filter function
_WRAP_LATEX = None  # the tag to wrap LaTeX math in (needed to play nicely with Typogrify or for template designers)
_MATH_REGEX = re.compile(r'(\$\$|\$|\\begin\{(.+?)\}|<(math)(?:\s.*?)?>).*?(\1|\\end\{\2\}|</\3>)', re.DOTALL | re.IGNORECASE)  # used to detect math
_MATH_SUMMARY_REGEX = None  # used to match math in summary
_MATH_INCOMPLETE_TAG_REGEX = None  # used to match math that has been cut off in summary
_MATHJAX_SETTINGS = {}  # settings that can be specified by the user, used to control mathjax script settings
with open (os.path.dirname(os.path.realpath(__file__))+'/mathjax_script.txt', 'r') as mathjax_script:  # Read the mathjax javascript from file
    _MATHJAX_SCRIPT=mathjax_script.read()


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
        mid = lo + (hi-lo+1)//2
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
    ignore_regex = re.compile(r'<(pre|code)(?:\s.*?)?>.*?</(\1)>', re.DOTALL | re.IGNORECASE)

    for match in ignore_regex.finditer(content):
        ignore_within.append(match.span())

    return ignore_within


def wrap_math(content, ignore_within):
    """Wraps math in user specified tags.

    This is needed for Typogrify to play nicely with math but it can also be
    styled by template providers
    """

    wrap_math.found_math = False

    def math_tag_wrap(match):
        """function for use in re.sub"""

        # determine if the tags are within <pre> and <code> blocks
        ignore = binary_search(match.span(1), ignore_within) or binary_search(match.span(4), ignore_within)

        if ignore or match.group(3) == 'math':
            if match.group(3) == 'math':
                # Will detect mml, but not wrap anything around it
                wrap_math.found_math = True

            return match.group(0)
        else:
            wrap_math.found_math = True
            return '<%s>%s</%s>' % (_WRAP_LATEX, match.group(0), _WRAP_LATEX)

    return (_MATH_REGEX.sub(math_tag_wrap, content), wrap_math.found_math)


def process_summary(instance, ignore_within):
    """Summaries need special care. If Latex is cut off, it must be restored.

    In addition, the mathjax script must be included if necessary thereby
    making it independent to the template
    """

    process_summary.altered_summary = False
    insert_mathjax = False
    end_tag = '</%s>' % _WRAP_LATEX if _WRAP_LATEX is not None else ''

    # use content's _get_summary method to obtain summary
    summary = instance._get_summary()

    # Determine if there is any math in the summary which are not within the
    # ignore_within tags
    math_item = None
    for math_item in _MATH_SUMMARY_REGEX.finditer(summary):
        ignore = binary_search(math_item.span(2), ignore_within)
        if '...' not in math_item.group(5):
            ignore = ignore or binary_search(math_item.span(5), ignore_within)
        else:
            ignore = ignore or binary_search(math_item.span(6), ignore_within)

        if ignore:
            math_item = None # In <code> or <pre> tags, so ignore
        else:
            insert_mathjax = True

    # Repair the math if it was cut off math_item will be the final math
    # code  matched that is not within <pre> or <code> tags
    if math_item and '...' in math_item.group(5):
        if math_item.group(3) is not None:
            end = r'\end{%s}' % math_item.group(3)
        elif math_item.group(4) is not None:
            end = r'</math>'
        elif math_item.group(2) is not None:
            end = math_item.group(2)

        search_regex = r'%s(%s.*?%s)' % (re.escape(instance._content[0:math_item.start(1)]), re.escape(math_item.group(1)), re.escape(end))
        math_match = re.search(search_regex, instance._content, re.DOTALL | re.IGNORECASE)

        if math_match:
            new_summary = summary.replace(math_item.group(0), math_match.group(1)+'%s ...' % end_tag)

            if new_summary != summary:
                if _MATHJAX_SETTINGS['auto_insert']:
                    return new_summary+_MATHJAX_SCRIPT.format(**_MATHJAX_SETTINGS)
                else:
                    instance.mathjax = True
                    return new_summary

    def incomplete_end_latex_tag(match):
        """function for use in re.sub"""
        if binary_search(match.span(3), ignore_within):
            return match.group(0)

        process_summary.altered_summary = True
        return match.group(1) + match.group(4)

    # check for partial math tags at end. These must be removed
    summary = _MATH_INCOMPLETE_TAG_REGEX.sub(incomplete_end_latex_tag, summary)

    if process_summary.altered_summary or insert_mathjax:
        if insert_mathjax:
            if _MATHJAX_SETTINGS['auto_insert']:
                summary+= _MATHJAX_SCRIPT.format(**_MATHJAX_SETTINGS)
            else:
                instance.mathjax = True

        return summary

    return None  # Making it explicit that summary was not altered


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
    _MATHJAX_SETTINGS['latex_preview'] = 'TeX'  # controls what user sees while waiting for LaTex to render
    _MATHJAX_SETTINGS['color'] = 'black'  # controls color math is rendered in

    # Source for MathJax: default (below) is to automatically determine what protocol to use
    _MATHJAX_SETTINGS['source'] = """'https:' == document.location.protocol
                ? 'https://c328740.ssl.cf1.rackcdn.com/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML'
                : 'http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML'"""

    # This next setting controls whether the mathjax script should be automatically
    # inserted into the content. The mathjax script will not be inserted into
    # the content if no math is detected. For summaries that are present in the
    # index listings, mathjax script will also be automatically inserted.
    # Setting this value to false means the template must be altered if this
    # plugin is to work, and so it is only recommended for the template
    # designer who wants maximum control.
    _MATHJAX_SETTINGS['auto_insert'] = True  # controls whether mathjax script is automatically inserted into the content

    if not isinstance(settings, dict):
        return

    # The following mathjax settings can be set via the settings dictionary
    # Iterate over dictionary in a way that is compatible with both version 2
    # and 3 of python
    for key, value in ((key, settings[key]) for key in settings):
        if key == 'auto_insert' and isinstance(value, bool):
            _MATHJAX_SETTINGS[key] = value

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

        if key == 'latex_preview' and isinstance(value, str):
            _MATHJAX_SETTINGS[key] = value

        if key == 'color' and isinstance(value, str):
            _MATHJAX_SETTINGS[key] = value

        if key == 'ssl' and isinstance(value, str):
            if value == 'off':
                _MATHJAX_SETTINGS['source'] = "'http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML'"

            if value == 'force':
                _MATHJAX_SETTINGS['source'] = "'https://c328740.ssl.cf1.rackcdn.com/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML'"


def process_content(instance):
    """Processes content, with logic to ensure that Typogrify does not clash
    with math.

    In addition, mathjax script is inserted at the end of the content thereby
    making it independent of the template
    """

    if not instance._content:
        return

    ignore_within = ignore_content(instance._content)

    if _WRAP_LATEX:
        instance._content, math = wrap_math(instance._content, ignore_within)
    else:
        math = True if _MATH_REGEX.search(instance._content) else False

    # The user initially set Typogrify to be True, but since it would clash
    # with math, we set it to False. This means that the default reader will
    # not call Typogrify, so it is called here, where we are able to control
    # logic for it ignore math if necessary
    if _TYPOGRIFY:
        # Tell Typogrify to ignore the tags that math has been wrapped in
        # also, Typogrify must always ignore mml (math) tags
        ignore_tags = [_WRAP_LATEX,'math'] if _WRAP_LATEX else ['math']

        # Exact copy of the logic as found in the default reader
        instance._content = _TYPOGRIFY(instance._content, ignore_tags)
        instance.metadata['title'] = _TYPOGRIFY(instance.metadata['title'], ignore_tags)

    if math:
        if _MATHJAX_SETTINGS['auto_insert']:
            # Mathjax script added to content automatically. Now it
            # does not need to be explicitly added to the template
            instance._content += _MATHJAX_SCRIPT.format(**_MATHJAX_SETTINGS)
        else:
            # Place the burden on ensuring mathjax script is available to
            # browser on the template designer (see README for more details)
            instance.mathjax = True

        # The summary needs special care because math math cannot just be cut
        # off
        summary = process_summary(instance, ignore_within)
        if summary is not None:
            instance._summary = summary


def pelican_init(pelicanobj):
    """Intialializes certain global variables and sets typogogrify setting to
    False should it be set to True.
    """

    global _TYPOGRIFY
    global _WRAP_LATEX
    global _MATH_SUMMARY_REGEX
    global _MATH_INCOMPLETE_TAG_REGEX

    try:
        settings = pelicanobj.settings['MATH']
    except:
        settings = None

    process_settings(settings)

    # Allows MathJax script to be accessed from template should it be needed
    pelicanobj.settings['MATHJAXSCRIPT'] = _MATHJAX_SCRIPT.format(**_MATHJAX_SETTINGS)

    # If Typogrify set to True, then we need to handle it manually so it does
    # not conflict with LaTeX
    try:
        if pelicanobj.settings['TYPOGRIFY'] is True:
            pelicanobj.settings['TYPOGRIFY'] = False
            try:
                from typogrify.filters import typogrify

                # Determine if this is the correct version of Typogrify to use
                import inspect
                typogrify_args = inspect.getargspec(typogrify).args
                if len(typogrify_args) < 2 or 'ignore_tags' not in typogrify_args:
                    raise TypeError('Incorrect version of Typogrify')

                # At this point, we are happy to use Typogrify, meaning
                # it is installed and it is a recent enough version
                # that can be used to ignore all math
                _TYPOGRIFY = typogrify
                _WRAP_LATEX = 'mathjax' # default to wrap mathjax content inside of
            except ImportError:
                print("\nTypogrify is not installed, so it is being ignored.\nIf you want to use it, please install via: pip install typogrify\n")
            except TypeError:
                print("\nA more recent version of Typogrify is needed for the render_math module.\nPlease upgrade Typogrify to the latest version (anything above version 2.04 is okay).\nTypogrify will be turned off due to this reason.\n")
    except KeyError:
        pass

    # Set _WRAP_LATEX to the settings tag if defined. The idea behind this is
    # to give template designers control over how math would be rendered
    try:
        if pelicanobj.settings['MATH']['wrap_latex']:
            _WRAP_LATEX = pelicanobj.settings['MATH']['wrap_latex']
    except (KeyError, TypeError):
        pass

    # regular expressions that depend on _WRAP_LATEX are set here
    tag_start= r'<%s>' % _WRAP_LATEX if not _WRAP_LATEX is None else ''
    tag_end = r'</%s>' % _WRAP_LATEX if not _WRAP_LATEX is None else ''
    math_summary_regex = r'((\$\$|\$|\\begin\{(.+?)\}|<(math)(?:\s.*?)?>).+?)(\2|\\end\{\3\}|</\4>|\s?\.\.\.)(%s|</\4>)?' % tag_end

    # NOTE: The logic in _get_summary will handle <math> correctly because it
    # is perceived as an html tag. Therefore we are only interested in handling
    # non mml (i.e. LaTex)
    incomplete_end_latex_tag = r'(.*)(%s)(\\\S*?|\$)\s*?(\s?\.\.\.)(%s)?$' % (tag_start, tag_end)

    _MATH_SUMMARY_REGEX = re.compile(math_summary_regex, re.DOTALL | re.IGNORECASE)
    _MATH_INCOMPLETE_TAG_REGEX = re.compile(incomplete_end_latex_tag, re.DOTALL | re.IGNORECASE)


def register():
    """Plugin registration"""

    signals.initialized.connect(pelican_init)
    signals.content_object_init.connect(process_content)
