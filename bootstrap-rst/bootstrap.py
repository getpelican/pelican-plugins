#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Bootstrap RST
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import sys, os, re
from docutils import nodes, utils
from docutils.parsers.rst.directives import images
from docutils.transforms import TransformError, Transform, parts
from docutils.parsers.rst import Directive, directives, states, roles
from docutils.nodes import fully_normalize_name, whitespace_normalize_name
from docutils.parsers.rst.roles import set_classes

from docutils.io import StringOutput
from docutils.core import Publisher

from pelican import signals
from pelican.readers import RstReader, PelicanHTMLTranslator

from .roles import *
from .directives import *


class HTMLTranslator(PelicanHTMLTranslator):
    """
    This is a translator class for the docutils system.
    """

    def visit_h1(self, node):
        self.body.append('<h1>%s</h1>' % node.children[0])
        raise nodes.SkipNode

    def visit_h2(self, node):
        self.body.append('<h2>%s</h2>' % node.children[0])
        raise nodes.SkipNode

    def visit_h3(self, node):
        self.body.append('<h3>%s</h3>' % node.children[0])
        raise nodes.SkipNode

    def visit_h4(self, node):
        self.body.append('<h4>%s</h4>' % node.children[0])
        raise nodes.SkipNode

    def visit_h5(self, node):
        self.body.append('<h5>%s</h5>' % node.children[0])
        raise nodes.SkipNode

    def visit_h6(self, node):
        self.body.append('<h6>%s</h6>' % node.children[0])
        raise nodes.SkipNode

    def visit_label_default(self, node):
        self.body.append(
            '<span class="label label-default">%s</span>' % node.children[0])
        raise nodes.SkipNode

    def visit_label_primary(self, node):
        self.body.append(
            '<span class="label label-primary">%s</span>' % node.children[0])
        raise nodes.SkipNode

    def visit_label_success(self, node):
        self.body.append(
            '<span class="label label-success">%s</span>' % node.children[0])
        raise nodes.SkipNode

    def visit_label_info(self, node):
        self.body.append(
            '<span class="label label-info">%s</span>' % node.children[0])
        raise nodes.SkipNode

    def visit_label_warning(self, node):
        self.body.append(
            '<span class="label label-warning">%s</span>' % node.children[0])
        raise nodes.SkipNode

    def visit_label_danger(self, node):
        self.body.append(
            '<span class="label label-danger">%s</span>' % node.children[0])
        raise nodes.SkipNode

    def visit_page_row(self, node):
        self.body.append(self.starttag(node,'div'))

    def depart_page_row(self, node):
        self.body.append('</div>\n')

    def visit_page_column(self, node):
        self.body.append(self.starttag(node,'div'))

    def depart_page_column(self, node):
        self.body.append('</div>\n')


    def visit_button(self, node):
        btn_classes = { 'primary' : 'btn-primary', 'success' : 'btn-success',
                        'info'    : 'btn-info',    'warning' : 'btn-warning',
                        'danger'  : 'btn-danger',  'link'    : 'btn-link',
                        'outline' : 'btn-outline', 'tiny'    : 'btn-xs',
                        'small'   : 'btn-sm',      'large'   : 'btn-lg',
                        'block'   : 'btn-block',   'active'  : 'btn-active' }

        classes = 'btn '
        flag = False
        for node_class in node['classes']:
            if node_class in ['primary', 'success', 'warning'
                              'info', 'link', 'danger', 'outline']:
                flag = True
            btn_class = btn_classes.get(node_class, None)
            if btn_class:
                classes += btn_class + ' '
        if flag == False:
            classes += 'btn-default'

        target = node['target']
        properties = ''

        # Disabled
        if 'disabled' in node['classes']:
            if target:
                properties += ' disabled="disabled"'
            else:
                classes += ' disabled'

        # Data toggle
        if 'toggle' in node['classes']:
            classes += ' dropdown-toggle '
            properties += ' data-toggle="dropdown"'
        if target:
            properties += ' role="button"'
            anchor = '<a href="%s" class="%s" %s>' % (target,classes,properties)
            self.body.append(anchor)
        else:
            properties += ' type="button"'
            button = '<button class="%s" %s>' % (classes,properties)
            self.body.append(button)

    def depart_button(self, node):
        if node['target']:
            self.body.append('</a>\n')
        else:
            self.body.append('</button>\n')


    def visit_progress(self, node):
        prg_classes = { 'success' : 'progress-bar-success',
                        'info'    : 'progress-bar-info',
                        'warning' : 'progress-bar-warning',
                        'danger'  : 'progress-bar-danger' }

        label = node['label']
        classes = 'progress-bar'
        flag = False
        for nodeclass in node['classes']:
            flag = True
            classes += ' ' + prg_classes.get(nodeclass, '')
        if flag == False:
            classes += ' progress-bar-default'
        properties = 'role="progress-bar"'
        properties += ' aria-valuenow="%d"' % int(node['value'])
        properties += ' aria-valuemin="%d"' % int(node['value_min'])
        properties += ' aria-valuemax="%d"' % int(node['value_max'])
        properties += ' style="width: %d%%";' % int(node['value'])
        if 'active' in node['classes']:
            self.body.append('<div class="progress progress-striped active">')
        elif 'striped' in node['classes']:
            self.body.append('<div class="progress progress-striped">')
        else:
            self.body.append('<div class="progress">')
        self.body.append(
            '<div class="%s" %s>%s</div>' % (classes,properties,label))
        self.body.append('</div>')
        raise nodes.SkipNode

    def visit_alert(self, node):
        self.body.append(self.starttag(node, 'div', CLASS='alert'))
        if node.dismissable:
            self.body.append(
                u"""<button type="button" class="close" data-dismiss="alert" """
                u"""aria-hidden="true">×</button>""")

    def depart_alert(self, node):
        self.body.append('</div>\n')

    def visit_callout(self, node):
        self.body.append(self.starttag(node, 'div', CLASS='bs-callout'))

    def depart_callout(self, node):
        self.body.append('</div>\n')



    # overwritten
    def visit_definition_list(self, node):
        list_class = node.parent.get('list-class', [])
        list_class.append('docutils')
        list_class = ' '.join(list_class)
        self.body.append(self.starttag(node, 'dl', CLASS=list_class))

    # overwritten
    def visit_sidebar(self, node):
        self.body.append(self.starttag(node, 'div', CLASS='col-md-3 col-md-push-9'))
        self.body.append(self.starttag(node, 'div', CLASS='bs-docs-sidebar hidden-print affix-top'))
        self.body.append(self.starttag(node, 'div', CLASS='sidebar'))
        self.set_first_last(node)
        self.in_sidebar = True

    # overwritten
    def depart_sidebar(self, node):
        self.body.append('</div>\n')
        self.body.append('</div>\n')
        self.body.append('</div>\n')
        #  Opening tag for body
        self.body.append(self.starttag(node, 'div', CLASS='col-md-9 col-md-pull-3'))
        self.in_sidebar = False

    # overwritten : removed compact paragraph
    # def visit_paragraph(self, node):
    #     if self.should_be_compact_paragraph(node):
    #         self.context.append('')
    #     else:
    #         self.body.append(self.starttag(node, 'p', ''))
    #     self.context.append('</p>\n')

    # overwritten: remove border=1, replace docutils/table class
    def visit_table(self, node):
        self.context.append(self.compact_p)
        self.compact_p = True
        #classes = ' '.join(['docutils', self.settings.table_style]).strip()
        classes = ' '.join(['table', self.settings.table_style]).strip()
        self.body.append(self.starttag(node, 'table', CLASS=classes))

    # overwritten : removed 'container' class
    def visit_container(self, node):
        self.body.append(self.starttag(node, 'div', CLASS=''))

    # overwritten: get rid of <hr> tag
    def depart_header(self, node):
        start = self.context.pop()
        header = [self.starttag(node, 'div', CLASS='header')]
        header.extend(self.body[start:])
        header.append('\n</div>\n')
        self.body_prefix.extend(header)
        self.header.extend(header)
        del self.body[start:]

    # overwritten: get rid of <hr> tag
    def depart_footer(self, node):
        start = self.context.pop()
        footer = [self.starttag(node, 'div', CLASS='footer')]
        footer.extend(self.body[start:])
        footer.append('\n</div>\n')
        self.footer.extend(footer)
        self.body_suffix[:0] = footer
        del self.body[start:]

    # overwritten
    def depart_document(self, node):
        self.head_prefix.extend([self.doctype,
                                 self.head_prefix_template %
                                 {'lang': self.settings.language_code}])
        self.html_prolog.append(self.doctype)
        self.meta.insert(0, self.content_type % self.settings.output_encoding)
        self.head.insert(0, self.content_type % self.settings.output_encoding)
        if self.math_header:
            self.head.append(self.math_header)
        # skip content-type meta tag with interpolated charset value:
        self.html_head.extend(self.head[1:])
        # self.body_prefix.append(self.starttag(node, 'div', CLASS='document'))
        self.body_prefix.append(self.starttag(node, 'div', CLASS='container'))
        # self.body_suffix.insert(0, '</div>\n')
        self.fragment.extend(self.body) # self.fragment is the "naked" body
        self.html_body.extend(self.body_prefix[1:] + self.body_pre_docinfo
                              + self.docinfo + self.body
                              + self.body_suffix[:-1])
        assert not self.context, 'len(context) = %s' % len(self.context)


# -----------------------------------------------------------------------------
class RSTReader(RstReader):
    """
        A custom RST reader that behaves exactly like its parent class RstReader
        with the difference that it uses our HTMLTranslator
    """

    def _get_publisher(self, source_path):
        extra_params = {'initial_header_level': '2',
                        'syntax_highlight': 'short',
                        'input_encoding': 'utf-8'}
        user_params = self.settings.get('DOCUTILS_SETTINGS')
        if user_params:
            extra_params.update(user_params)

        pub = Publisher(destination_class=StringOutput)
        pub.set_components('standalone', 'restructuredtext', 'html')
        pub.writer.translator_class = HTMLTranslator
        pub.process_programmatic_settings(None, extra_params, None)
        pub.set_source(source_path=source_path)
        pub.publish()
        return pub


def add_reader(readers):
    readers.reader_classes['rst'] = RSTReader

def register():
    signals.readers_init.connect(add_reader)
