# -*- coding: utf-8 -*-
"""
Math Render Plugin for Pelican
==============================
This plugin allows your site to render Math. It uses
the MathJax JavaScript engine.

For markdown, the plugin works by creating a Markdown
extension which is used during the markdown compilation
stage.  Math therefore gets treated like a "first class
citizen" in Pelican

For reStructuredText, the plugin instructs the rst engine
to output Mathjax for all math.

The mathjax script is by default automatically inserted
into the HTML.

Typogrify Compatibility
-----------------------
This plugin now plays nicely with Typogrify, but it
requires Typogrify version 2.07 or above.

User Settings
-------------
Users are also able to pass a dictionary of settings
in the settings file which will control how the MathJax
library renders things. This could be very useful for
template builders that want to adjust the look and feel of
the math.  See README for more details.
"""

import collections
import os
import sys

from pelican import signals, generators

try:
    from bs4 import BeautifulSoup
except ImportError as e:
    BeautifulSoup = None

try:
    from . pelican_mathjax_markdown_extension import PelicanMathJaxExtension
except ImportError as e:
    PelicanMathJaxExtension = None

def process_settings(pelicanobj):
    """Sets user specified MathJax settings (see README for more details)"""

    mathjax_settings = {}

    # NOTE TO FUTURE DEVELOPERS: Look at the README and what is happening in
    # this function if any additional changes to the mathjax settings need to
    # be incorporated. Also, please inline comment what the variables
    # will be used for

    # Default settings
    mathjax_settings['auto_insert'] = True  # if set to true, it will insert mathjax script automatically into content without needing to alter the template.
    mathjax_settings['align'] = 'center'  # controls alignment of of displayed equations (values can be: left, right, center)
    mathjax_settings['indent'] = '0em'  # if above is not set to 'center', then this setting acts as an indent
    mathjax_settings['show_menu'] = 'true'  # controls whether to attach mathjax contextual menu
    mathjax_settings['process_escapes'] = 'true'  # controls whether escapes are processed
    mathjax_settings['latex_preview'] = 'TeX'  # controls what user sees while waiting for LaTex to render
    mathjax_settings['color'] = 'inherit'  # controls color math is rendered in
    mathjax_settings['linebreak_automatic'] = 'false'  # Set to false by default for performance reasons (see http://docs.mathjax.org/en/latest/output.html#automatic-line-breaking)
    mathjax_settings['tex_extensions'] = ''  # latex extensions that can be embedded inside mathjax (see http://docs.mathjax.org/en/latest/tex.html#tex-and-latex-extensions)
    mathjax_settings['responsive'] = 'false'  # Tries to make displayed math responsive
    mathjax_settings['responsive_break'] = '768'  # The break point at which it math is responsively aligned (in pixels)
    mathjax_settings['mathjax_font'] = 'default'  # forces mathjax to use the specified font.
    mathjax_settings['process_summary'] = BeautifulSoup is not None  # will fix up summaries if math is cut off. Requires beautiful soup
    mathjax_settings['force_tls'] = 'false'  # will force mathjax to be served by https - if set as False, it will only use https if site is served using https
    mathjax_settings['message_style'] = 'normal'  # This value controls the verbosity of the messages in the lower left-hand corner. Set it to "none" to eliminate all messages
    mathjax_settings['macros'] = '{}'

    # Source for MathJax
    mathjax_settings['source'] = "'//cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML'"

    # Get the user specified settings
    try:
        settings = pelicanobj.settings['MATH_JAX']
    except:
        settings = None

    # If no settings have been specified, then return the defaults
    if not isinstance(settings, dict):
        return mathjax_settings

    # The following mathjax settings can be set via the settings dictionary
    for key, value in ((key, settings[key]) for key in settings):
        # Iterate over dictionary in a way that is compatible with both version 2
        # and 3 of python

        if key == 'align':
            try:
                typeVal = isinstance(value, basestring)
            except NameError:
                typeVal = isinstance(value, str)

            if not typeVal:
                continue

            if value == 'left' or value == 'right' or value == 'center':
                mathjax_settings[key] = value
            else:
                mathjax_settings[key] = 'center'

        if key == 'indent':
            mathjax_settings[key] = value

        if key == 'source':
            mathjax_settings[key] = value

        if key == 'show_menu' and isinstance(value, bool):
            mathjax_settings[key] = 'true' if value else 'false'

        if key == 'message_style':
            mathjax_settings[key] = value if value is not None else 'none'

        if key == 'auto_insert' and isinstance(value, bool):
            mathjax_settings[key] = value

        if key == 'process_escapes' and isinstance(value, bool):
            mathjax_settings[key] = 'true' if value else 'false'

        if key == 'latex_preview':
            try:
                typeVal = isinstance(value, basestring)
            except NameError:
                typeVal = isinstance(value, str)

            if not typeVal:
                continue

            mathjax_settings[key] = value

        if key == 'color':
            try:
                typeVal = isinstance(value, basestring)
            except NameError:
                typeVal = isinstance(value, str)

            if not typeVal:
                continue

            mathjax_settings[key] = value

        if key == 'linebreak_automatic' and isinstance(value, bool):
            mathjax_settings[key] = 'true' if value else 'false'

        if key == 'process_summary' and isinstance(value, bool):
            if value and BeautifulSoup is None:
                print("BeautifulSoup4 is needed for summaries to be processed by render_math\nPlease install it")
                value = False

            mathjax_settings[key] = value

        if key == 'responsive' and isinstance(value, bool):
            mathjax_settings[key] = 'true' if value else 'false'

        if key == 'force_tls' and isinstance(value, bool):
            mathjax_settings[key] = 'true' if value else 'false'       

        if key == 'responsive_break' and isinstance(value, int):
            mathjax_settings[key] = str(value)

        if key == 'tex_extensions' and isinstance(value, list):
            # filter string values, then add '' to them
            try:
                value = filter(lambda string: isinstance(string, basestring), value)
            except NameError:
                value = filter(lambda string: isinstance(string, str), value)

            value = map(lambda string: "'%s'" % string, value)
            mathjax_settings[key] = ',' + ','.join(value)

        if key == 'mathjax_font':
            try:
                typeVal = isinstance(value, basestring)
            except NameError:
                typeVal = isinstance(value, str)

            if not typeVal:
                continue

            value = value.lower()

            if value == 'sanserif':
                value = 'SansSerif'
            elif value == 'fraktur':
                value = 'Fraktur'
            elif value == 'typewriter':
                value = 'Typewriter'
            else:
                value = 'default'

            mathjax_settings[key] = value

        if key == 'macros':
            text_lines = []
            macros = parse_tex_macros(value)
            for macro in macros:
                if 'args' in macro.keys():
                    # number of arguments > 1
                    text_lines.append("{0}: ['{1}', {2}]".format(macro['name'], macro['definition'], macro['args']))
                else:
                    text_lines.append("{0}: '{1}'".format(macro['name'], macro['definition']))
            mathjax_settings[key] = '{' + ", ".join(text_lines) + '}'

    return mathjax_settings

def _load_macro_definitions(*args):
    """Returns list of lines from files, use absolute path.

    Example: [{'filename': '/home/user/defs.text', 'line_num': 1,
     'def': '\newcommand{\circ}{2 \pi R}'}]"""
    output_lines = []
    for arg in args:
        with open(arg, 'rt') as input_file:
            lines = input_file.read().splitlines()
            for index, value in enumerate(lines):
                if value.strip() == '': continue
                line_num = index + 1
                line = {'filename': arg, 'line_num': line_num, 'def': value}
                output_lines.append(line)
    return output_lines

def _filter_duplicates(*macros):
    """Returns a modified copy of the input list of macros by keeping
    only the last definition of each duplicate item. Also, if a macro is
    defined multiple times, a warning is printed to stdout.
    Unique items are left untouched.
    """
    names = []
    for macro in macros:
        names.append(macro['name'])

    seen = set()
    # duplicate_indices contains the index of the first time an element appears
    # more than once in names
    duplicate_indices = [names.index(item)
                         for item, count in collections.Counter(names).items()
                         if count > 1]
    unique_indices = [names.index(item)
                      for item, count in collections.Counter(names).items()
                      if count == 1]
    if len(duplicate_indices) > 0:
        duplicates = []
        for i in duplicate_indices:
            name = macros[i]['name']
            duplicate = {'name': name, 'where':[]}
            for j in macros:
                if j['name'] == name:
                    duplicate['where'].append((j['line'], j['file']))
            duplicates.append(duplicate)
        exception_text = "WARNING: macros where defined more than once, the last definition is used\n"
        for dup in duplicates:
            exception_text += "Macro {} defined in\n".format(dup['name'].strip('\\'))
            for place in dup['where']:
                exception_text += "{}, line {}\n".format(place[1], place[0])
        print(exception_text)
    # I need the last definition for each duplicate definition
    last_duplicated_indices = []
    for i, v in enumerate(duplicate_indices):
        all_indices = []
        for j, name in enumerate(names):
            if name == names[v]:
                all_indices.append(j)
        last =  max(all_indices)
        last_duplicated_indices.append(last)

    filtered = [elem for i, elem in enumerate(macros)
                if i in unique_indices + last_duplicated_indices]
    return filtered

def parse_tex_macros(args):
    # ogni arg è un file
    macros = []
    for arg in args:
        lines = _load_macro_definitions(arg)
        for line in lines:
            macros.append(_parse_macro(line))
    _filter_duplicates(*macros)
    # remove line and file keys from temp_macros
    # (added for debug in case of duplicates)
    return [{k: v for k, v in elem.items()
             if k in ['name', 'definition', 'args']}
            for elem in macros]

def _parse_macro(arg):
    """Returns a macro from input raw text.

     The TeX macro definition is read and translated to a
     dictionary containing the name without backslash and the definition;
     if arguments are present, their number is added too.

     Backslashes in the definition are added in order to ensure the proper
    form in the final html page.

     Example:
    >  {'name': 'pd',
         'definition': '\\\\\\\\frac{\\\\\\\\partial #1}{\\\\\\\\partial #2}',
         'args': 2,
         'file': '/home/user/commands.tex',
         'line': 1}"""
    splitted = arg['def'].split('{')
    name_number = splitted[1].split('}')
    name = name_number[0].strip('\\')
    # for the definition, remove the last character from the last string which is }
    # remember that strings are immutable objects in python
    last_def_token = splitted[-1][:-1]
    splitted_def = splitted[2:-1] + [last_def_token]
    complete_def = '{'.join(splitted_def).replace('\\','\\\\\\\\')
    final_command = {'line': arg['line_num'], 'file': arg['filename'],
                     'name': name,
                     'definition': complete_def}
    if name_number[1]:
        # the number of arguments is defined, therefore name_number[1] is not null string
        args_number = name_number[1].lstrip('[').rstrip(']')
        final_command['args'] = args_number
    return final_command

def process_summary(article):
    """Ensures summaries are not cut off. Also inserts
    mathjax script so that math will be rendered"""

    summary = article._get_summary()
    summary_parsed = BeautifulSoup(summary, 'html.parser')
    math = summary_parsed.find_all(class_='math')

    if len(math) > 0:
        last_math_text = math[-1].get_text()
        if len(last_math_text) > 3 and last_math_text[-3:] == '...':
            content_parsed = BeautifulSoup(article._content, 'html.parser')
            full_text = content_parsed.find_all(class_='math')[len(math)-1].get_text()
            math[-1].string = "%s ..." % full_text
            summary = summary_parsed.decode()

        article._summary = "%s<script type='text/javascript'>%s</script>" % (summary, process_summary.mathjax_script)

def configure_typogrify(pelicanobj, mathjax_settings):
    """Instructs Typogrify to ignore math tags - which allows Typogrify
    to play nicely with math related content"""

    # If Typogrify is not being used, then just exit
    if not pelicanobj.settings.get('TYPOGRIFY', False):
        return

    try:
        import typogrify
        from distutils.version import LooseVersion

        if LooseVersion(typogrify.__version__) < LooseVersion('2.0.7'):
            raise TypeError('Incorrect version of Typogrify')

        from typogrify.filters import typogrify

        # At this point, we are happy to use Typogrify, meaning
        # it is installed and it is a recent enough version
        # that can be used to ignore all math
        # Instantiate markdown extension and append it to the current extensions
        pelicanobj.settings['TYPOGRIFY_IGNORE_TAGS'].extend(['.math', 'script'])  # ignore math class and script

    except (ImportError, TypeError) as e:
        pelicanobj.settings['TYPOGRIFY'] = False  # disable Typogrify

        if isinstance(e, ImportError):
            print("\nTypogrify is not installed, so it is being ignored.\nIf you want to use it, please install via: pip install typogrify\n")

        if isinstance(e, TypeError):
            print("\nA more recent version of Typogrify is needed for the render_math module.\nPlease upgrade Typogrify to the latest version (anything equal or above version 2.0.7 is okay).\nTypogrify will be turned off due to this reason.\n")

def process_mathjax_script(mathjax_settings):
    """Load the mathjax script template from file, and render with the settings"""

    # Read the mathjax javascript template from file
    with open (os.path.dirname(os.path.realpath(__file__))
            + '/mathjax_script_template', 'r') as mathjax_script_template:
        mathjax_template = mathjax_script_template.read()

    return mathjax_template.format(**mathjax_settings)

def mathjax_for_markdown(pelicanobj, mathjax_script, mathjax_settings):
    """Instantiates a customized markdown extension for handling mathjax
    related content"""

    # Create the configuration for the markdown template
    config = {}
    config['mathjax_script'] = mathjax_script
    config['math_tag_class'] = 'math'
    config['auto_insert'] = mathjax_settings['auto_insert']

    # Instantiate markdown extension and append it to the current extensions
    try:
        if isinstance(pelicanobj.settings.get('MD_EXTENSIONS'), list): # pelican 3.6.3 and earlier
           pelicanobj.settings['MD_EXTENSIONS'].append(PelicanMathJaxExtension(config))
        else:
            pelicanobj.settings['MARKDOWN'].setdefault('extensions', []).append(PelicanMathJaxExtension(config))
    except:
        sys.excepthook(*sys.exc_info())
        sys.stderr.write("\nError - the pelican mathjax markdown extension failed to configure. MathJax is non-functional.\n")
        sys.stderr.flush()

def mathjax_for_rst(pelicanobj, mathjax_script):
    """Setup math for RST"""
    docutils_settings = pelicanobj.settings.get('DOCUTILS_SETTINGS', {})
    docutils_settings['math_output'] = 'MathJax'
    pelicanobj.settings['DOCUTILS_SETTINGS'] = docutils_settings
    rst_add_mathjax.mathjax_script = mathjax_script

def pelican_init(pelicanobj):
    """
    Loads the mathjax script according to the settings.
    Instantiate the Python markdown extension, passing in the mathjax
    script as config parameter.
    """

    # Process settings, and set global var
    mathjax_settings = process_settings(pelicanobj)

    # Generate mathjax script
    mathjax_script = process_mathjax_script(mathjax_settings)

    # Configure Typogrify
    configure_typogrify(pelicanobj, mathjax_settings)

    # Configure Mathjax For Markdown
    if PelicanMathJaxExtension:
        mathjax_for_markdown(pelicanobj, mathjax_script, mathjax_settings)

    # Configure Mathjax For RST
    mathjax_for_rst(pelicanobj, mathjax_script)

    # Set process_summary's mathjax_script variable
    process_summary.mathjax_script = None
    if mathjax_settings['process_summary']:
        process_summary.mathjax_script = mathjax_script

def rst_add_mathjax(content):
    """Adds mathjax script for reStructuredText"""

    # .rst is the only valid extension for reStructuredText files
    _, ext = os.path.splitext(os.path.basename(content.source_path))
    if ext != '.rst':
        return

    # If math class is present in text, add the javascript
    # note that RST hardwires mathjax to be class "math"
    if 'class="math"' in content._content:
        content._content += "<script type='text/javascript'>%s</script>" % rst_add_mathjax.mathjax_script

def process_rst_and_summaries(content_generators):
    """
    Ensure mathjax script is applied to RST and summaries are
    corrected if specified in user settings.

    Handles content attached to ArticleGenerator and PageGenerator objects,
    since the plugin doesn't know how to handle other Generator types.

    For reStructuredText content, examine both articles and pages.
    If article or page is reStructuredText and there is math present,
    append the mathjax script.

    Also process summaries if present (only applies to articles)
    and user wants summaries processed (via user settings)
    """

    for generator in content_generators:
        if isinstance(generator, generators.ArticlesGenerator):
            for article in (
                    generator.articles +
                    generator.translations +
                    generator.drafts):
                rst_add_mathjax(article)
                #optionally fix truncated formulae in summaries.
                if process_summary.mathjax_script is not None:
                    process_summary(article)
        elif isinstance(generator, generators.PagesGenerator):
            for page in generator.pages:
                rst_add_mathjax(page)

def register():
    """Plugin registration"""
    signals.initialized.connect(pelican_init)
    # repeated
    signals.all_generators_finalized.connect(process_rst_and_summaries)
