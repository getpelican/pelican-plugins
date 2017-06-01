# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Bootstrap RST
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
from docutils import nodes
from docutils.parsers.rst.directives.body import BasePseudoSection
from docutils.parsers.rst import Directive, directives, states, roles
from docutils.parsers.rst.roles import set_classes
from docutils.nodes import fully_normalize_name, whitespace_normalize_name
from docutils.parsers.rst.directives.tables import Table
from docutils.parsers.rst.roles import set_classes
from docutils.transforms import misc


class button(nodes.Inline, nodes.Element): pass
class progress(nodes.Inline, nodes.Element): pass
class alert(nodes.General, nodes.Element): pass
class callout(nodes.General, nodes.Element): pass



class Alert(Directive):
    required_arguments, optional_arguments = 0,0
    has_content = True
    option_spec = {'type': directives.unchanged,
                   'dismissable': directives.flag,
                   'class': directives.class_option }

    def run(self):
        # Raise an error if the directive does not have contents.
        self.assert_has_content()
        text = '\n'.join(self.content)

        # Create the node, to be populated by `nested_parse`.
        node = alert(text, **self.options)
        node['classes'] = ['alert']
        node['classes'] += self.options.get('class', [])
        if 'type' in self.options:
            node['classes'] += ['alert-%s' % node['type']]
        node.dismissable = False
        if 'dismissable' in self.options:
            node['classes'] += ['alert-dismissable']
            node.dismissable = True

        # Parse the directive contents.
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


class Callout(Directive):
    required_arguments, optional_arguments = 0,1
    has_content = True

    def run(self):
        # Raise an error if the directive does not have contents.
        self.assert_has_content()
        text = '\n'.join(self.content)

        # Create the node, to be populated by `nested_parse`.
        node = callout(self.block_text, **self.options)
        node['classes'] = ['bs-callout']
        if len(self.arguments):
            type = 'bs-callout-' + self.arguments[0]
        else:
            type = 'bs-callout-info'
        node['classes'] += [type]

        # Parse the directive contents.
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]



class Container(Directive):
    optional_arguments = 1
    final_argument_whitespace = True
    option_spec = {'name': directives.unchanged}
    has_content = True
    default_class = None

    def run(self):
        self.assert_has_content()
        text = '\n'.join(self.content)
        try:
            if self.arguments:
                classes = directives.class_option(self.arguments[0])
            else:
                classes = self.default_class
        except ValueError:
            raise self.error(
                'Invalid class attribute value for "%s" directive: "%s".'
                % (self.name, self.arguments[0]))
        node = nodes.container(text)
        node['classes'].extend(classes)
        self.add_name(node)
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]

class Thumbnail(Container):
    default_class = ['thumbnail']

class Caption(Container):
    default_class = ['caption']

class Jumbotron(Container):
    default_class = ['jumbotron']

class PageHeader(Container):
    default_class = ['page-header']



class Lead(Directive):
    required_arguments, optional_arguments = 0,0
    has_content = True
    option_spec = {'class':  directives.class_option }
    def run(self):
        self.assert_has_content()
        text = '\n'.join(self.content)
        node = nodes.container(text, **self.options)
        node['classes'] = ['lead']
        node['classes'] += self.options.get('class', [])
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


class Paragraph(Directive):
    required_arguments, optional_arguments = 0,0
    has_content = True
    option_spec = {'class':  directives.class_option }

    def run(self):
        # Raise an error if the directive does not have contents.
        self.assert_has_content()
        text = '\n'.join(self.content)

        # Create the node, to be populated by `nested_parse`.
        node = nodes.paragraph(text, **self.options)
        node['classes'] += self.options.get('class', [])

        # Parse the directive contents.
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


class PageRow(Directive):

    """
    Directive to declare a container that is column-aware.
    """

    required_arguments, optional_arguments = 0,1
    final_argument_whitespace = True
    has_content = True
    option_spec = {'class':  directives.class_option }
    def run(self):
        self.assert_has_content()
        node = nodes.container(self.content)
        node['classes'] = ['row']
        if self.arguments:
            node['classes'] += [self.arguments[0]]
        node['classes'] += self.options.get('class', [])

        self.add_name(node)
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]



class PageColumn(Directive):

    """
    Directive to declare column with width and offset.
    """

    required_arguments, optional_arguments = 0,0
    final_argument_whitespace = True
    has_content = True
    option_spec = {'width':  directives.positive_int,
                   'offset': directives.positive_int,
                   'push':   directives.positive_int,
                   'pull':   directives.positive_int,
                   'size':   lambda x: directives.choice(x, ('xs', 'sm', 'md', 'lg')),
                   'class':  directives.class_option }
    def run(self):
        self.assert_has_content()
        text = '\n'.join(self.content)
        node = nodes.container(text)
        width = self.options.get('width', 1)
        size = self.options.get('size', 'md')
        node['classes'] += ["col-%s-%d" % (size, width)]

        offset = self.options.get('offset', 0)
        if offset > 0:
            node['classes'] += ["col-%s-offset-%d" % (size, offset)]

        push = self.options.get('push', 0)
        if push > 0:
            node['classes'] += ["col-%s-push-%d" % (size, push)]

        pull = self.options.get('pull', 0)
        if pull > 0:
            node['classes'] += ["col-%s-pull-%d" % (size, pull)]

        node['classes'] += self.options.get('class', [])

        self.add_name(node)
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]



class Button(Directive):

    """
    Directive to declare a button
    """

    required_arguments, optional_arguments = 0,0
    final_argument_whitespace = True
    has_content = True
    option_spec = {'class'   : directives.class_option,
                   'target'  : directives.unchanged_required }
    def run(self):
        self.assert_has_content()
        node = button()
        node['target'] = self.options.get('target', None)
        node['classes'] = self.options.get('class', [])
        self.state.nested_parse(self.content, self.content_offset, node)
        self.add_name(node)
        return [node]



class Progress(Directive):

    """
    Directive to declare a progress bar.
    """

    required_arguments, optional_arguments = 0,1
    final_argument_whitespace = True
    has_content = False
    option_spec = { 'class'   : directives.class_option,
                    'label'   : directives.unchanged,
                    'value'   : directives.unchanged_required,
                    'min'     : directives.unchanged_required,
                    'max'     : directives.unchanged_required }
    def run(self):
        node = progress()
        node['classes']   = self.options.get('class', '')
        node['value_min'] = self.options.get('min_value', '0')
        node['value_max'] = self.options.get('max_value', '100')
        node['value']     = self.options.get('value', '50')
        node['label']     = self.options.get('label', '')
        if self.arguments:
            node['value'] = self.arguments[0].rstrip(' %')
            #if 'label' not in self.options:
            #    node['label'] = self.arguments[0]
        return [node]



class Header(Directive):

    """Contents of document header."""

    required_arguments, optional_arguments = 0,1
    has_content = True
    option_spec = {'class':  directives.class_option }

    def run(self):
        self.assert_has_content()
        header = self.state_machine.document.get_decoration().get_header()
        header['classes'] += self.options.get('class', [])
        if self.arguments:
            header['classes'] += [self.arguments[0]]
        self.state.nested_parse(self.content, self.content_offset, header)
        return []


class Footer(Directive):

    """Contents of document footer."""

    required_arguments, optional_arguments = 0,1
    has_content = True
    option_spec = {'class':  directives.class_option }

    def run(self):
        self.assert_has_content()
        footer = self.state_machine.document.get_decoration().get_footer()
        footer['classes'] += self.options.get('class', [])
        if self.arguments:
            footer['classes'] += [self.arguments[0]]
        self.state.nested_parse(self.content, self.content_offset, footer)
        return []







# List item class
# -----------------------------------------------------------------------------
class ItemClass(Directive):

    """
    Set a "list-class" attribute on the directive content or the next element.
    When applied to the next element, a "pending" element is inserted, and a
    transform does the work later.
    """

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = False

    def run(self):
        try:
            class_value = directives.class_option(self.arguments[0])
        except ValueError:
            raise self.error(
                'Invalid class attribute value for "%s" directive: "%s".'
                % (self.name, self.arguments[0]))

        parent = self.state.parent
        if isinstance(parent,nodes.list_item):
            parent['classes'].extend(class_value)
        return []


# PATCH: Make a row inherit from the class attribute
# --------------------------------------------------------------
class ListTable(Table):

    """
    Implement tables whose data is encoded as a uniform two-level bullet list.
    For further ideas, see
    http://docutils.sf.net/docs/dev/rst/alternatives.html#list-driven-tables
    """

    option_spec = {'header-rows': directives.nonnegative_int,
                   'stub-columns': directives.nonnegative_int,
                   'widths': directives.positive_int_list,
                   'class': directives.class_option,
                   'name': directives.unchanged}

    def run(self):
        if not self.content:
            error = self.state_machine.reporter.error(
                'The "%s" directive is empty; content required.' % self.name,
                nodes.literal_block(self.block_text, self.block_text),
                line=self.lineno)
            return [error]
        title, messages = self.make_title()
        node = nodes.Element()          # anonymous container for parsing
        self.state.nested_parse(self.content, self.content_offset, node)
        try:
            num_cols, col_widths = self.check_list_content(node)
            table_data = [[item.children for item in row_list[0]]
                          for row_list in node[0]]
            header_rows = self.options.get('header-rows', 0)
            stub_columns = self.options.get('stub-columns', 0)
            self.check_table_dimensions(table_data, header_rows, stub_columns)
        except SystemMessagePropagation as detail:
            return [detail.args[0]]
        #table_node = self.build_table_from_list(table_data, col_widths,
        #                                        header_rows, stub_columns)
        table_node = self.build_table_from_list(node[0], col_widths,
                                                header_rows, stub_columns)
        table_node['classes'] += self.options.get('class', [])
        self.add_name(table_node)
        if title:
            table_node.insert(0, title)
        return [table_node] + messages

    def check_list_content(self, node):
        if len(node) != 1 or not isinstance(node[0], nodes.bullet_list):
            error = self.state_machine.reporter.error(
                'Error parsing content block for the "%s" directive: '
                'exactly one bullet list expected.' % self.name,
                nodes.literal_block(self.block_text, self.block_text),
                line=self.lineno)
            raise SystemMessagePropagation(error)
        list_node = node[0]
        # Check for a uniform two-level bullet list:
        for item_index in range(len(list_node)):
            item = list_node[item_index]
            if len(item) != 1 or not isinstance(item[0], nodes.bullet_list):
                error = self.state_machine.reporter.error(
                    'Error parsing content block for the "%s" directive: '
                    'two-level bullet list expected, but row %s does not '
                    'contain a second-level bullet list.'
                    % (self.name, item_index + 1), nodes.literal_block(
                    self.block_text, self.block_text), line=self.lineno)
                raise SystemMessagePropagation(error)
            elif item_index:
                # ATTN pychecker users: num_cols is guaranteed to be set in the
                # "else" clause below for item_index==0, before this branch is
                # triggered.
                if len(item[0]) != num_cols:
                    error = self.state_machine.reporter.error(
                        'Error parsing content block for the "%s" directive: '
                        'uniform two-level bullet list expected, but row %s '
                        'does not contain the same number of items as row 1 '
                        '(%s vs %s).'
                        % (self.name, item_index + 1, len(item[0]), num_cols),
                        nodes.literal_block(self.block_text, self.block_text),
                        line=self.lineno)
                    raise SystemMessagePropagation(error)
            else:
                num_cols = len(item[0])
        col_widths = self.get_column_widths(num_cols)
        return num_cols, col_widths

    def build_table_from_list(Self, table_data, col_widths, header_rows, stub_columns):
        table = nodes.table()
        tgroup = nodes.tgroup(cols=len(col_widths))
        table += tgroup
        for col_width in col_widths:
            colspec = nodes.colspec(colwidth=col_width)
            if stub_columns:
                colspec.attributes['stub'] = 1
                stub_columns -= 1
            tgroup += colspec
        rows = []
        for row in table_data:
            row_node = nodes.row()
            row_node['classes'] = row[0]['classes']
            for cell in row[0]:
                cell = cell.children
                entry = nodes.entry()
                entry += cell
                row_node += entry
            rows.append(row_node)
        if header_rows:
            thead = nodes.thead()
            thead.extend(rows[:header_rows])
            tgroup += thead
        tbody = nodes.tbody()
        tbody.extend(rows[header_rows:])
        tgroup += tbody
        return table



directives.register_directive('item-class', ItemClass)
directives.register_directive('list-table', ListTable)
directives.register_directive('thumbnail', Thumbnail)
directives.register_directive('caption', Caption)
directives.register_directive('jumbotron', Jumbotron)
directives.register_directive('page-header', PageHeader)
directives.register_directive('lead', Lead)
directives.register_directive('progress', Progress)
directives.register_directive('alert', Alert)
directives.register_directive('callout', Callout)
directives.register_directive('row', PageRow)
directives.register_directive('column', PageColumn)
directives.register_directive('button', Button)
directives.register_directive('footer', Footer)
directives.register_directive('header', Header)
