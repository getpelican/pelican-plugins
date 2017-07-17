-----------------------------
Implementing language buttons
-----------------------------

Each article with translations has translations links, but that's the
only way to switch between language subsites.

For this reason it is convenient to add language buttons to the top
menu bar to make it simple to switch between the language subsites on
all pages.

Example designs
---------------

Language buttons showing other available languages
..................................................

The ``extra_siteurls`` dictionary is a mapping of all other (not the
``DEFAULT_LANG`` of the current (sub-)site) languages to the
``SITEURL`` of the respective (sub-)sites

.. code-block:: jinja

   <!-- SNIP -->
   <nav><ul>
   {% if extra_siteurls %}
   {% for lang, url in extra_siteurls.items() %}
   <li><a href="{{ url }}/">{{ lang }}</a></li>
   {% endfor %}
   <!-- separator -->
   <li style="background-color: white; padding: 5px;">&nbsp</li>
   {% endif %}
   {% for title, link in MENUITEMS %}
   <!-- SNIP -->

Notice the slash ``/`` after ``{{ url }}``, this makes sure it works
with local development when ``SITEURL == ''``.

Language buttons showing all available languages, current is active
...................................................................

The ``extra_siteurls`` dictionary is a mapping of all languages to the
``SITEURL`` of the respective (sub-)sites. This template sets the
language of the current (sub-)site as active.

.. code-block:: jinja

   <!-- SNIP -->
   <nav><ul>
   {% if lang_siteurls %}
   {% for lang, url in lang_siteurls.items() %}
   <li{% if lang == DEFAULT_LANG %} class="active"{% endif %}><a href="{{ url }}/">{{ lang }}</a></li>
   {% endfor %}
   <!-- separator -->
   <li style="background-color: white; padding: 5px;">&nbsp</li>
   {% endif %}
   {% for title, link in MENUITEMS %}
   <!-- SNIP -->


Tips and tricks
---------------

Showing more than language codes
................................

If you want the language buttons to show e.g. the names of the
languages or flags [#flags]_, not just the language codes, you can use
a jinja filter to translate the language codes


.. code-block:: python

   languages_lookup = {
		'en': 'English',
		'cz': 'Čeština',
		}

   def lookup_lang_name(lang_code):
       return languages_lookup[lang_code]

   JINJA_FILTERS = {
		...
		'lookup_lang_name': lookup_lang_name,
		}

And then the link content becomes

.. code-block:: jinja

   <!-- SNIP -->
   {% for lang, siteurl in lang_siteurls.items() %}
   <li{% if lang == DEFAULT_LANG %} class="active"{% endif %}><a href="{{ siteurl }}/">{{ lang | lookup_lang_name }}</a></li>
   {% endfor %}
   <!-- SNIP -->


Changing the order of language buttons
......................................

Because ``lang_siteurls`` and ``extra_siteurls`` are instances of
``OrderedDict`` with ``main_lang`` being always the first key, you can
change the order through a jinja filter.

.. code-block:: python

   def my_ordered_items(ordered_dict):
       items = list(ordered_dict.items())
       # swap first and last using tuple unpacking
       items[0], items[-1] = items[-1], items[0]
       return items

   JINJA_FILTERS = {
		...
		'my_ordered_items': my_ordered_items,
		}

And then the ``for`` loop line in the template becomes

.. code-block:: jinja

   <!-- SNIP -->
   {% for lang, siteurl in lang_siteurls | my_ordered_items %}
   <!-- SNIP -->


.. [#flags] Although it may look nice, `w3 discourages it
            <http://www.w3.org/TR/i18n-html-tech-lang/#ri20040808.173208643>`_.
