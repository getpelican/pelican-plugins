# -*- coding: utf-8 -*-
from pelican import signals

def initialize_content_object_set(app):
    app.settings['content_objects'] = set()

def collect_content_objects(co):
    context = co._context['content_objects'].add(co)

def register():
    signals.initialized.connect(initialize_content_object_set)
    signals.content_object_init.connect(collect_content_objects)
