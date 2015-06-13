#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Twitter Bootstrap RST directives Plugin For Pelican
===================================================

This plugin defines rst directives for different CSS and Javascript components from
the twitter bootstrap framework.

"""

from uuid import uuid1

from cgi import escape
from docutils import nodes, utils
import docutils
from docutils.parsers import rst
from docutils.parsers.rst import directives, roles, Directive
from pelican import signals
from pelican.readers import RstReader, PelicanHTMLTranslator



class CleanHTMLTranslator(PelicanHTMLTranslator):

    """
        A custom HTML translator based on the Pelican HTML translator.
        Used to clean up some components html classes that could conflict 
        with the bootstrap CSS classes.
        Also defines new tags that are not handleed by the current implementation of 
        docutils.

        The most obvious example is the Container component
    """

    def visit_literal(self, node):
        classes = node.get('classes', node.get('class', []))
        if 'code' in classes:
            self.body.append(self.starttag(node, 'code'))
        elif 'kbd' in classes:
            self.body.append(self.starttag(node, 'kbd'))
        else:
            self.body.append(self.starttag(node, 'pre'))

    def depart_literal(self, node):
        classes = node.get('classes', node.get('class', []))
        if 'code' in classes:
            self.body.append('</code>\n')
        elif 'kbd' in classes:
            self.body.append('</kbd>\n')
        else:
            self.body.append('</pre>\n')

    def visit_container(self, node):
        self.body.append(self.starttag(node, 'div'))


class CleanRSTReader(RstReader):

    """
        A custom RST reader that behaves exactly like its parent class RstReader with
        the difference that it uses the CleanHTMLTranslator
    """

    def _get_publisher(self, source_path):
        extra_params = {'initial_header_level': '2',
                        'syntax_highlight': 'short',
                        'input_encoding': 'utf-8'}
        user_params = self.settings.get('DOCUTILS_SETTINGS')
        if user_params:
            extra_params.update(user_params)

        pub = docutils.core.Publisher(
            destination_class=docutils.io.StringOutput)
        pub.set_components('standalone', 'restructuredtext', 'html')
        pub.writer.translator_class = CleanHTMLTranslator
        pub.process_programmatic_settings(None, extra_params, None)
        pub.set_source(source_path=source_path)
        pub.publish()
        return pub


def keyboard_role(name, rawtext, text, lineno, inliner,
                  options={}, content=[]):
    """
        This function creates an inline console input block as defined in the twitter bootstrap documentation
        overrides the default behaviour of the kbd role

        *usage:*
            :kbd:`<your code>`

        *Example:*

            :kbd:`<section>`

        This code is not highlighted
    """
    new_element = nodes.literal(rawtext, text)
    new_element.set_class('kbd')

    return [new_element], []


def code_role(name, rawtext, text, lineno, inliner,
              options={}, content=[]):
    """
        This function creates an inline code block as defined in the twitter bootstrap documentation
        overrides the default behaviour of the code role

        *usage:*
            :code:`<your code>`

        *Example:*

            :code:`<section>`

        This code is not highlighted
    """
    new_element = nodes.literal(rawtext, text)
    new_element.set_class('code')

    return [new_element], []


def glyph_role(name, rawtext, text, lineno, inliner,
               options={}, content=[]):
    """
        This function defines a glyph inline role that show a glyph icon from the 
        twitter bootstrap framework

        *Usage:*

            :glyph:`<glyph_name>`

        *Example:*

            Love this music :glyph:`music` :)

        Can be subclassed to include a target

        *Example:*

            .. role:: story_time_glyph(glyph)
                :target: http://www.youtube.com/watch?v=5g8ykQLYnX0
                :class: small text-info

            Love this music :story_time_glyph:`music` :)

    """

    target = options.get('target', None)
    glyph_name = 'glyphicon-{}'.format(text)

    if target:
        target = utils.unescape(target)
        new_element = nodes.reference(rawtext, ' ', refuri=target)
    else:
        new_element = nodes.container()
    classes = options.setdefault('class', [])
    classes += ['glyphicon', glyph_name]
    for custom_class in classes:
        new_element.set_class(custom_class)
    return [new_element], []

glyph_role.options = {
    'target': rst.directives.unchanged,
}
glyph_role.content = False


class Label(rst.Directive):

    '''
        generic Label directive class definition.
        This class define a directive that shows 
        bootstrap Labels around its content

        *usage:*

            .. label-<label-type>::

                <Label content>

        *example:*

            .. label-default::

                This is a default label content

    '''

    has_content = True
    custom_class = ''

    def run(self):
        # First argument is the name of the glyph
        label_name = 'label-{}'.format(self.custom_class)
        # get the label content
        text = '\n'.join(self.content)
        # Create a new container element (div)
        new_element = nodes.container(text)
        # Update its content
        self.state.nested_parse(self.content, self.content_offset,
                                new_element)
        # Set its custom bootstrap classes
        new_element['classes'] += ['label ', label_name]
        # Return one single element
        return [new_element]


class DefaultLabel(Label):

    custom_class = 'default'


class PrimaryLabel(Label):

    custom_class = 'primary'


class SuccessLabel(Label):

    custom_class = 'success'


class InfoLabel(Label):

    custom_class = 'info'


class WarningLabel(Label):

    custom_class = 'warning'


class DangerLabel(Label):

    custom_class = 'danger'


class Panel(rst.Directive):

    """
        generic Panel directive class definition.
        This class define a directive that shows 
        bootstrap Labels around its content

        *usage:*

            .. panel-<panel-type>:: 
                :title: <title>

                <Panel content>

        *example:*

            .. panel-default:: 
                :title: panel title

                This is a default panel content

    """

    has_content = True
    option_spec = {
        'title': rst.directives.unchanged,
    }
    custom_class = ''

    def run(self):
        # First argument is the name of the glyph
        panel_name = 'panel-{}'.format(self.custom_class)
        # get the label title
        title_text = self.options.get('title', self.custom_class.title())
        # get the label content
        text = '\n'.join(self.content)
        # Create the panel element
        panel_element = nodes.container()
        panel_element['classes'] += ['panel', panel_name]
        # Create the panel headings
        heading_element = nodes.container(title_text)
        title_nodes, messages = self.state.inline_text(title_text,
                                                       self.lineno)
        title = nodes.paragraph(title_text, '', *title_nodes)
        heading_element.append(title)
        heading_element['classes'] += ['panel-heading']
        # Create a new container element (div)
        body_element = nodes.container(text)
        # Update its content
        self.state.nested_parse(self.content, self.content_offset,
                                body_element)
        # Set its custom bootstrap classes
        body_element['classes'] += ['panel-body']
        # add the heading and body to the panel
        panel_element.append(heading_element)
        panel_element.append(body_element)
        # Return the panel element
        return [panel_element]


class DefaultPanel(Panel):

    custom_class = 'default'


class PrimaryPanel(Panel):

    custom_class = 'primary'


class SuccessPanel(Panel):

    custom_class = 'success'


class InfoPanel(Panel):

    custom_class = 'info'


class WarningPanel(Panel):

    custom_class = 'warning'


class DangerPanel(Panel):

    custom_class = 'danger'


class Alert(rst.Directive):

    """
        generic Alert directive class definition.
        This class define a directive that shows 
        bootstrap Labels around its content

        *usage:*

            .. alert-<alert-type>::

                <alert content>

        *example:*

            .. alert-default::

                This is a default alert content

    """
    has_content = True
    custom_class = ''

    def run(self):
        # First argument is the name of the glyph
        alert_name = 'alert-{}'.format(self.custom_class)
        # get the label content
        text = '\n'.join(self.content)
        # Create a new container element (div)
        new_element = nodes.compound(text)
        # Update its content
        self.state.nested_parse(self.content, self.content_offset,
                                new_element)
        # Recurse inside its children and change the hyperlinks classes
        for child in new_element.traverse(include_self=False):
            if isinstance(child, nodes.reference):
                child.set_class('alert-link')
        # Set its custom bootstrap classes
        new_element['classes'] += ['alert ', alert_name]
        # Return one single element
        return [new_element]


class SuccessAlert(Alert):

    custom_class = 'success'


class InfoAlert(Alert):

    custom_class = 'info'


class WarningAlert(Alert):

    custom_class = 'warning'


class DangerAlert(Alert):

    custom_class = 'danger'


class Media(rst.Directive):

    '''
        generic Media directive class definition.
        This class define a directive that shows 
        bootstrap media image with text according
        to the media component on bootstrap

        *usage*:
            .. media:: <image_uri>
                :position: <position>
                :alt: <alt>
                :height: <height>
                :width: <width>
                :scale: <scale>
                :target: <target>

                <text content>

        *example*:
            .. media:: http://stuffkit.com/wp-content/uploads/2012/11/Worlds-Most-Beautiful-Lady-Camilla-Belle-HD-Photos-4.jpg
                :height: 750
                :width: 1000
                :scale: 20
                :target: www.google.com
                :alt: Camilla Belle
                :position: left

                This image is not mine. Credit goes to http://stuffkit.com



    '''

    has_content = True
    required_arguments = 1

    option_spec = {
        'position': str,
        'alt': rst.directives.unchanged,
        'height': rst.directives.length_or_unitless,
        'width': rst.directives.length_or_percentage_or_unitless,
        'scale': rst.directives.percentage,
        'target': rst.directives.unchanged_required,
    }

    def get_image_element(self):
        # Get the image url
        image_url = self.arguments[0]
        image_reference = rst.directives.uri(image_url)
        self.options['uri'] = image_reference

        reference_node = None
        messages = []
        if 'target' in self.options:
            block = rst.states.escape2null(
                self.options['target']).splitlines()
            block = [line for line in block]
            target_type, data = self.state.parse_target(
                block, self.block_text, self.lineno)
            if target_type == 'refuri':
                container_node = nodes.reference(refuri=data)
            elif target_type == 'refname':
                container_node = nodes.reference(
                    refname=fully_normalize_name(data),
                    name=whitespace_normalize_name(data))
                container_node.indirect_reference_name = data
                self.state.document.note_refname(container_node)
            else:                           # malformed target
                messages.append(data)       # data is a system message
            del self.options['target']
        else:
            container_node = nodes.container()

        # get image position
        position = self.options.get('position', 'left')
        position_class = 'pull-{}'.format(position)

        container_node.set_class(position_class)

        image_node = nodes.image(self.block_text, **self.options)
        image_node['classes'] += ['media-object']

        container_node.append(image_node)
        return container_node

    def run(self):
        # now we get the content
        text = '\n'.join(self.content)

        # get image alternative text
        alternative_text = self.options.get('alternative-text', '')

        # get container element
        container_element = nodes.container()
        container_element['classes'] += ['media']

        # get image element
        image_element = self.get_image_element()

        # get body element
        body_element = nodes.container(text)
        body_element['classes'] += ['media-body']
        self.state.nested_parse(self.content, self.content_offset,
                                body_element)

        container_element.append(image_element)
        container_element.append(body_element)
        return [container_element, ]


def register_directives():
    rst.directives.register_directive('label-default', DefaultLabel)
    rst.directives.register_directive('label-primary', PrimaryLabel)
    rst.directives.register_directive('label-success', SuccessLabel)
    rst.directives.register_directive('label-info', InfoLabel)
    rst.directives.register_directive('label-warning', WarningLabel)
    rst.directives.register_directive('label-danger', DangerLabel)

    rst.directives.register_directive('panel-default', DefaultPanel)
    rst.directives.register_directive('panel-primary', PrimaryPanel)
    rst.directives.register_directive('panel-success', SuccessPanel)
    rst.directives.register_directive('panel-info', InfoPanel)
    rst.directives.register_directive('panel-warning', WarningPanel)
    rst.directives.register_directive('panel-danger', DangerPanel)

    rst.directives.register_directive('alert-success', SuccessAlert)
    rst.directives.register_directive('alert-info', InfoAlert)
    rst.directives.register_directive('alert-warning', WarningAlert)
    rst.directives.register_directive('alert-danger', DangerAlert)

    rst.directives.register_directive( 'media', Media )


def register_roles():
    rst.roles.register_local_role('glyph', glyph_role)
    rst.roles.register_local_role('code', code_role)
    rst.roles.register_local_role('kbd', keyboard_role)


def add_reader(readers):
    readers.reader_classes['rst'] = CleanRSTReader


def register():
    register_directives()
    register_roles()
    signals.readers_init.connect(add_reader)
