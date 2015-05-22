# -*- coding: utf-8 -*-
"""
Table embedding plugin for Pelican
=================================

This plugin allows you to create easily table.

"""
from __future__ import unicode_literals
import re

ai_regex = re.compile(r"ai ?\= ?\" ?(1) ?\"")
th_regex = re.compile(r"th ?\= ?\" ?(0) ?\"")
cap_regex = re.compile("caption ?\= ?\"(.+?)\"")
main_regex = re.compile(r"(\[jtable(.*?)\]([\s\S]*?)\[\/jtable\])")

table_template = """
<div class="justtable">
    <table>
        {% if caption %}
        <caption> {{ caption }} </caption>
        {% endif %}
        {% if th != 0 %}
        <thead>
        <tr>
            {% if ai == 1 %}
            <th> No. </th>
            {% endif %}
            {% for head in heads %}
            <th>{{ head }}</th>
            {% endfor %}
        </tr>
        </thead>
        {% endif %}
        <tbody>
            {% for body in bodies %}
            <tr>
                {% if ai == 1 %}
                <td> {{ loop.index }} </td>
                {% endif %}
                {% for entry in body %}
                <td>{{ entry }}</td>
                {% endfor %}
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
"""


def generate_table(generator):
    """Replace table tag in the article content."""
    from jinja2 import Template

    template = Template(table_template)

    for article in generator.articles:
        for match in main_regex.findall(article._content):
            param = {"ai": 0, "th": 1, "caption": ""}
            if ai_regex.search(match[1]):
                param['ai'] = 1
            if cap_regex.search(match[1]):
                param['caption'] = cap_regex.findall(match[1])[0]
            if th_regex.search(match[1]):
                param["th"] = 0
            data = match[2].strip().split('\n')
            if len(data) > 2 or len(data) == 1 and param['th'] == 0:
                if param['th'] != 0:
                    heads = data[0].split(',')
                    begin = 1
                else:
                    heads = None
                    begin = 0

                bodies = [n.split(',') for n in data[begin:]]

                # Create a context to render with
                context = generator.context.copy()
                context.update({
                    'heads': heads,
                    'bodies': bodies,
                })
                context.update(param)

                # Render the template
                replacement = template.render(context)
                article._content = article._content.replace(''.join(match[0]), replacement)


def register():
    """Plugin registration."""
    from pelican import signals

    signals.article_generator_finalized.connect(generate_table)
