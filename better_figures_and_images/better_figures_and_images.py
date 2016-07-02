""" Adds tags to images in article or page text.

Adds either responsive or boostrap repsonsive tags to images in the corpus of the article or page text.
Can use the keywords BETTER_FIGURES_BOOSTRAP or RESPONSIVE_IMAGES.

RESPONSIVE_IMAGES adds max-width: 100%; and height: auto; to the style tag.
BETTER_FIGURES_BOOSTRAP adds img-fluid to the class tag.

This adds two additional features for markdown. You can add additional tag attributes by adding json to the markdown alt tag field.
The module will process this and add the attributes to the to the img tag. Any attribute will be added without validation.
The json contains one magic attribute called type. If type is set to "figure" then the img tag will be wrapped in a figure tag.
After the img tag a figcaption tag will be added. If the img tag has a caption, that will be included as string text in the figcaption.
Otherwise, the alt text will be used.

This update remove the need for pillow as the size of the image is no loger necessare for HTML5.
This allows the plugin to work with plugins that modify the file location such as photos.
"""

from __future__ import unicode_literals

from pelican.generators import ArticlesGenerator
from pelican.generators import PagesGenerator
from pelican import signals

import json
import logging
import pprint
import re


logger = logging.getLogger(__name__)

try:
    from bs4 import BeautifulSoup
except ImportError:
    logger.error('BeautifulSoup not found')
    raise


def initialized(pelican):
    """Initialize the plugin """

    from pelican.settings import DEFAULT_CONFIG
    DEFAULT_CONFIG.setdefault('BETTER_FIGURES_BOOTSTRAP', False)
    DEFAULT_CONFIG.setdefault('RESPONSIVE_IMAGES', False)
    if pelican:
        pelican.settings.setdefault('BETTER_FIGURES_BOOTSTRAP', False)
        pelican.settings.setdefault('RESPONSIVE_IMAGES', False)


def default_fixer(tag_pile, tag_name, default):
    """Helper to add default tags.

    If the dictionary already contains a list, this extends the list.
    Otherwise, this adds the key and the element as a list.
    """
    if tag_name in tag_pile and isinstance(tag_pile[tag_name], list):
        tag_pile[tag_name].extend(default)
    else:
        tag_pile[tag_name] = default

    return tag_pile


def tag_parser(default, alt_tag):
    """Parses any JSON attributes contained within the alt tag.

    If in the alt tag there are JSON elements, this converts them to a dictionary.
    It also deduplicates any redundant tags.
    It also will set the alt key value to an empty string if it ends in:
    gif, jpg, jpeg, tiff, or png

    """

    # Example of pattern this will match: '{"type": "img", "style": ["width: 100%;"], "class":["float-left", "gap-left"]}'
    JSON_PATTERN = r'{.*?}'
    # If we wanted to match exact names a better pattern might be: IMAGE_PATTERN = r'[^/]*?\.(gif|jpg|jpeg|tiff|png)$'
    IMAGE_PATTERN = r'\.(gif|jpg|jpeg|tiff|png)$'

    json_instructions = re.findall(JSON_PATTERN, alt_tag)
    json_instructions = json_instructions[0] if len(json_instructions) == 1 else '{}'
    alt = re.sub(JSON_PATTERN, '', alt_tag).strip()
    logger.debug('The json instructions are: {0}'.format(json_instructions))

    logger.debug('The alt tag is: {0}'.format(alt))
    try:
        json_instructions = json.loads(json_instructions)
    except ValueError as e:
        logger.error('JSON Error:{0}'.format(e))
        raise

    if (re.search(IMAGE_PATTERN, alt)):
        json_instructions['alt'] = ''
    else:
        json_instructions['alt'] = alt

    if default == 'BETTER_FIGURES_BOOTSTRAP':
        json_instructions = default_fixer(json_instructions, 'class', ['img-fluid'])
    else:
        json_instructions = default_fixer(json_instructions, 'style', ['max-width: 100%;', 'height: auto;'])

    for key, value in json_instructions.iteritems():
        if isinstance(value, list):
            logger.debug("The list of multivalues keys are: {0}, {1}".format(key, value))
            # This deduplicates any redundant values in lists contained in keys.
            json_instructions[key] = list(set(value))

    return json_instructions


def better_figures_and_images(instance):
    """Adds appropriate attributes to img and figure tags.

    See README.md for more information.
    """

    if instance._content is not None:
        content = instance._content
        soup = BeautifulSoup(content, 'html.parser')

        if 'BETTER_FIGURES_BOOTSTRAP' in instance.settings and instance.settings['BETTER_FIGURES_BOOTSTRAP']:
            default = 'BETTER_FIGURES_BOOTSTRAP'
            fig_attr = 'class'
            cap_tag_default = ['figure-caption', 'text-center']
            fig_tag_default = ['figure']
            fig_img_default = ['figure-img']
        elif 'RESPONSIVE_IMAGES' in instance.settings and instance.settings['RESPONSIVE_IMAGES']:
            default = 'RESPONSIVE_IMAGES'
            fig_attr = 'style'
            fig_tag_default = ['max-width: 100%;', 'height: auto;']
            fig_img_default = ['max-width: 100%;', 'height: auto;']

        else:
            default = None

        if 'figure' in content:
            for figure in soup('figure'):
                figure.setdefault(fig_attr, []).extend(fig_tag_default)
                figure.img.setdefault(fig_attr, []).extend(fig_img_default)

        if 'img' in content:
            for img in soup('img'):
                logger.debug("Image Source: {0}".format(img['src']))
                attribs = tag_parser(default, img['alt'])
                for key, value in attribs.iteritems():
                    if key != 'type':
                        img[key] = value
                if 'type' in attribs and attribs['type'] == 'figure':
                    if 'caption' in attribs:
                        cap_text = attribs['caption']
                    else:
                        cap_text = attribs['alt']

                    cap_tag = soup.new_tag('figcaption', **{fig_attr: cap_tag_default})
                    logger.debug(cap_text)
                    cap_tag.string = cap_text
                    fig_tag = soup.new_tag('figure', **{fig_attr: fig_tag_default})
                    img[fig_attr].extend(fig_img_default)
                    img.wrap(fig_tag)
                    img.insert_after(cap_tag)

                    logger.debug(pprint.pformat(img.parent))
        instance._content = soup.prettify(formatter="html")


def run_plugin(generators):
    """Runs generator on both pages and articles. """
    for generator in generators:
        if isinstance(generator, ArticlesGenerator):
            for article in generator.articles:
                better_figures_and_images(article)
        elif isinstance(generator, PagesGenerator):
            for page in generator.pages:
                better_figures_and_images(page)


def register():
    """Uses the new style of registration based on GitHub Pelican issue #314. """
    signals.initialized.connect(initialized)
    try:
        signals.all_generators_finalized.connect(run_plugin)
    except AttributeError:
        # NOTE: This results in #314 so shouldn't really be relied on
        # https://github.com/getpelican/pelican-plugins/issues/314
        signals.content_object_init.connect(better_figures_and_images)
