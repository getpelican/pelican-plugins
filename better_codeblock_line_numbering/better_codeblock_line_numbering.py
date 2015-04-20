"""
Better Code-Block Line Numbering Plugin
--------------------------

Authored by Jacob Levernier, 2014
Released under the BSD 2-Clause License (http://opensource.org/licenses/BSD-2-Clause)

For more information on this plugin, please see the attached Readme.md file.
"""

from pelican import signals # For making this plugin work with Pelican.

import os.path # For checking whether files are present in the filesystem.

import re # For using regular expressions.

def add_line_wrappers(data_passed_from_pelican):
    """A function to read through each page and post as it comes through from Pelican, find all instances of triple-backtick (```...```) code blocks, and add an HTML wrapper to each line of each of those code blocks"""

    if data_passed_from_pelican._content: # If the item passed from Pelican has a "content" attribute (i.e., if it's not an image file or something else like that). NOTE: data_passed_from_pelican.content (without an underscore in front of 'content') seems to be read-only, whereas data_passed_from_pelican._content is able to be overwritten. This is somewhat explained in an IRC log from 2013-02-03 from user alexis to user webdesignhero_ at https://botbot.me/freenode/pelican/2013-02-01/?tz=America/Los_Angeles.
        full_content_of_page_or_post = data_passed_from_pelican._content
    else:
        return # Exit the function, essentially passing over the (non-text) file.

    all_instances_of_pre_elements = re.findall('<pre>.*?</pre>', full_content_of_page_or_post, re.DOTALL) # Use a regular expression to find every instance of '<pre>' followed by anything up to the first matching '</pre>'. re.DOTALL puts python's regular expression engine ('re') into a mode where a dot ('.') matches absolutely anything, including newline characters.
    
    if(len(all_instances_of_pre_elements) > 0): # If the article/page HAS any <pre>...</pre> elements, go on. Otherwise, don't (to do so would inadvertantly wipe out the output content for that article/page).
        updated_full_content_of_page_or_post = full_content_of_page_or_post # This just gives this an initial value before going into the loop below.

        # Go through each <pre> element instance that we found above, and parse it:
        for pre_element_to_parse in all_instances_of_pre_elements:

            # Wrap each line of the <pre>...</pre> section with <span class=code-line>...</span>, following http://bililite.com/blog/2012/08/05/line-numbering-in-pre-elements/. We'll use these to add line numbers using CSS later.
            # Note that below, '^' is the beginning of a string, '$' is the end of a string, and '\n' is a newline.
            replacement_text_with_beginning_of_each_line_wrapped_in_span = re.sub(r'(<pre.*?>|\n(?!</pre>))','\\1<span class="code-line">',pre_element_to_parse) # The (?!...) here is a Negative Lookahead (cf. http://www.regular-expressions.info/lookaround.html). This full regular expression says "Give me all code snippets that start with <pre ****> or start with a newline (\n), but NOT if the newline is followed immediately with '</pre>'. Take whatever you find, and replace it with what you found (\1) followed immediately by '<span class="code-lines">'.
            # http://stackoverflow.com/a/14625628 explains why we need to escape the backslash in the capture group reference (the '\1'). In short, python will recognize it as "\x01" if it's not escaped.
            replacement_text_with_full_line_wrapped_in_span = re.sub(r'((?<!</pre>)$|(?<!</pre>)\n)','</span>\\1',replacement_text_with_beginning_of_each_line_wrapped_in_span) # This regular expression says "Give me all code snippets that are the end of a string or a newline (but not preceeded by "</pre>" (this is a 'negative lookahead,' '(?<)'), and replace whatever you found with '</span'> followed by whatever you found (\1).
            
            updated_full_content_of_page_or_post = updated_full_content_of_page_or_post.replace(pre_element_to_parse,replacement_text_with_full_line_wrapped_in_span)

        # Replace the content of the page or post with our now-updated content (having gone through all instances of <pre> elements and updated them all, exiting the loop above.
        data_passed_from_pelican._content = updated_full_content_of_page_or_post


# Make Pelican work (see http://docs.getpelican.com/en/3.3.0/plugins.html#how-to-create-plugins):
def register():
    signals.content_object_init.connect(add_line_wrappers)
