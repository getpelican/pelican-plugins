Show Source plugin
------------------

The plugin allows you to place a link to the source text of your posts in the
same way that `Sphinx`_ does. It works for both pages and articles.

Plugin Activation
~~~~~~~~~~~~~~~~~

To activate the plugin ensure that you have ``SHOW_SOURCE_ON_SIDEBAR = True`` or
``SHOW_SOURCE_IN_SECTION = True`` your settings file.

Making Source Available for Posts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In order to mark posts so that their source may be seen use the following
metadata values (unless overridden)- for reStructuredText documents:

.. code-block:: reStructuredText

    :show_source: True

or, in Markdown syntax

.. code-block:: Markdown

    Show_source: True

The plugin will render your source document URL to a corresponding
``article.show_source_url`` (or ``page.show_source_url``) attribute which is
then accessible in the site templates.

Show Source in the Templates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To get the show source links on the article or page you will have to modify your
theme, either as a sidebar display or at the foot of an article.

Article or Page Sidebar Display
*******************************

How to get the source link to appear in the sidebar using the
`pelican-bootstrap3`_ theme:

.. code-block:: HTML

    {% if SHOW_SOURCE_ON_SIDEBAR %}
        {% if (article and article.show_source_url) or (page and page.show_source_url) %}
            <li class="list-group-item"><h4><i class="fa fa-tags fa-file-text"></i><span class="icon-label">This Page</span></h4>
                <ul class="list-group">
                    <li class="list-group-item">
                        {% if article %}
                        <a href="{{ SITEURL }}/{{ article.show_source_url }}">Show source</a>
                        {% elif page %}
                        <a href="{{ SITEURL }}/{{ page.show_source_url }}">Show source</a>
                        {% endif %}
                    </li>
                </ul>
            </li>
        {% endif %}
    {% endif %}

Article Footer Display
**********************

Here's some code (yes, `pelican-bootstrap3`_ again) to enable a souce link at
the bottom of an article:

.. code-block:: HTML

    {% if SHOW_SOURCE_IN_SECTION %}
        {% if article and article.show_source_url %}
        <section class="well" id="show-source">
            <h4>This Page</h4>
            <ul>
                <a href="{{ SITEURL }}/{{ article.show_source_url }}">Show source</a>
            </ul>
        </section>
        {% endif %}
    {% endif %}


Overriding Default Plugin Behaviour
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The default behaviour of the plugin is that revealing source is enabled on a
case by case basis. This can be changed by the use of
:py:`SHOW_SOURCE_ALL_POSTS = True` in the settings file. This does mean that the
plugin will publish all source documents no matter whether ``show_source`` is
set in the metadata or not.

Unless overridden, each document is saved as the article or page slug attribute
with a ``.txt`` extension.

So for example, if your configuration had ``ARTICLE_SAVE_AS`` configured like
so:

.. code-block:: python

    ARTICLE_SAVE_AS = 'posts/{date:%Y}/{date:%m}/{slug}/index.html'

Your static HTML post and source text document will be like the following:

.. code-block:: Text

    posts/2016/10/welcome-to-my article/index.html
    posts/2016/10/welcome-to-my article/welcome-to-my article.txt

You can add the ``SHOW_SOURCE_FILENAME`` variable in your settings file to
override the source file name, so you could set the following:

.. code-block:: python

    SHOW_SOURCE_FILENAME = 'my_source_file.txt'

So with the ``ARTICLE_SAVE_AS`` configured as above, the files would be saved
thus:

.. code-block:: Text

    posts/2016/10/welcome-to-my article/index.html
    posts/2016/10/welcome-to-my article/my_source_file.txt

This is the same behaviour for pages also.

.. _`Sphinx`: http://www.sphinx-doc.org/
.. _`pelican-bootstrap3`: https://github.com/getpelican/pelican-themes/tree/master/pelican-bootstrap3
