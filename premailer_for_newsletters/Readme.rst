===========================
 Premailer for Newsletters
===========================

``premailer_for_newsletters`` let you automate the processing of html generated
files from pelican thought premailer which turns CSS blocks into style
attributes.

Requirements
============

``premailer_for_newsletters`` requires premailer which can be installed with pip:

.. code-block:: sh

   pip install premailer


Usage
=====

``premailer_for_newsletters`` connects to the finalized signal which is invoked after
all the generators are executed and just before pelican exits useful for custom
post processing actions, such as: - minifying js/css assets. - notify/ping
search engines with an updated sitemap.

It pass the whole page to ``premailer`` and overwrite the result on the original
output file.


In order to use it, you need to define your ``PLUGIN_PATH`` and add
``premailer_for_newsletters`` to the ``PLUGINS`` list : 

.. code-block:: python

  PLUGIN_PATHS = ['./pelican-plugins']
  PLUGINS = ['premailer_for_newsletters', 'image_process']

