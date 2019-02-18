================================================
PlantUML plugin for Pelican rst and md documents
================================================

This plugin allows you to define UML diagrams directly into rst or md documents using the great PlantUML_ tool.

It gets the content of ``uml`` directive, passes it to the external program PlantUML_ and then links the generated image to the document.

.. contents::

Installation
============

You need to install PlantUML_ (see the site for details) and Graphviz_ 2.26.3 or later. The plugin expects a program ``plantuml`` in the classpath. If not installed by your package manager, you can create a shell script and place it somewhere in the classpath. For example, save te following into ``/usr/local/bin/plantuml`` (supposing PlantUML_ installed into ``/opt/plantuml``):

.. code-block:: bash

    #!/bin/bash
    java -jar /opt/plantuml/plantuml.jar ${@}

For Gentoo_ there is an ebuild at http://gpo.zugaina.org/dev-util/plantuml/RDep: you can download the ebuild and the ``files`` subfolder or you can add the ``zugaina`` repository with _layman (reccomended).

Usage
=====

Add ``plantuml`` to plugin list in ``pelicanconf.py``. For example:

.. code-block:: ptyhon

    PLUGINS = [ "sitemap", "plantuml" ]

One loaded the plugin register also the Pyhton-Markdown_ extension. 

RST usage
---------
Use the ``uml`` directive to start UML diagram description. It is not necessary to enclose diagram body between ``@startuml`` and ``@enduml`` directives: they are added automatically  before calling ``plantuml``.

In addition to ``class`` and ``alt`` options common to all images, you can use the ``format`` option to select what kind of image must be produced. At the moment only ``png`` and ``svg`` are supported; the default is ``png``.

Please note that the ``format`` option in not recognized by the ``plantuml`` extension of ``rst2pdf`` utility (call it with ``-e plantuml.py``) so if you use it you can get errors from that program.

MD usage
--------
For use with the Pyhton-Markdown_ syntax, the UML block must be enclose with ``::uml::``:

.. code-block:: markdown

    ::uml:: [format=...] [classes=...] [alt=...]
       PlantUML script
    ::end-uml::

Please keep a blank line before ``::uml::`` and after ``::end-uml::`` to be sure that the UML code will be correctly recognized. See Examples_ for more details.

With MD syntax options must be specified in the same line as the opening ``:uml::``, with the order ``format``, ``classes`` anmd ``alt``. The general syntax for option is

.. code-block:: text

    option="value"

Option can be enclosed with single or double quotes, as you like. Options defaults are the same as for the rst plugin.

For pandoc_reader plugin users
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The plugin ``pandoc_reader`` sends the Markdown body to the pandoc_ tool which has it's own Markdown parser, written in Haskell_ language: Python_ plugins manipulating Markdown posts (such this) are not used because the entire body id passed to pandoc_ without any iteraction by Pelican_.

For those who are using the ``pandoc_reader`` plugin and wants to include PlantUML_ diagrams, use the ``pandoc-plantuml`` script (only *nix, sorry): it is a wrapper for filtering the code blocks parsed by pandoc_ before
writing out the converted file. It is an adaption of the great work by Kurt Bonne for his `pandoc-plantuml-filter <https://github.com/kbonne/pandoc-plantuml-filter.git>`_.

To use it, copy the ``pandoc-plantuml`` file in a subdirectory of your pelican project (for example `pandoc_extensions`) and make sure it is executable (``chmod +x pandoc-plantuml``).

In the ``pelicanconf.py`` configure the needed plugins:

.. code-block:: python

    PLUGINS = ['pandoc_reader'] // Yes, plantuml plugin non necessary
    PANDOC_ARGS = ['--filter=pandoc_extensions/pandoc-plantuml']

In Markdown posts use the following syntax to include PlantUML_ diagrams:

.. code-block:: markdown

    ```plantuml
    @startuml
      Alice -> Bob: Authentication Request
      Bob --> Alice: Authentication Response

      Alice -> Bob: Another authentication Request
      Alice <-- Bob: another authentication Response
    @enduml
    ```

Rendered images will bu put in the output/images folder.

**NOTE:** ``pandoc-plantuml`` is broken from pandoc 1.16 cause an API change in pandoc ``Image`` function. I'm working on a fix but in the meanwhile use a version of pandoc prior to ``1.16`` .

Debugging
---------
The plugin can produce debugging informations to help to locate errors. To enable debugging execute ``pelican`` in debug mode:

 .. code-block:: console

     make DEBUG=1 html

  
Examples
========

Sequence diagram (from PlantUML_ site):

.. code-block:: rst

  .. uml::
    :alt: Sample sequence diagram

    participant User

    User -> A: DoWork
    activate A #FFBBBB

    A -> A: Internal call
    activate A #DarkSalmon

    A -> B: << createRequest >>
    activate B

    B --> A: RequestCreated
    deactivate B
    deactivate A
    A -> User: Done
    deactivate A

Output:

.. image:: http://plantuml.sourceforge.net/imgp/sequence_022.png
   :alt: Sample sequence diagram


Same diagram with Python-Markdown_ syntax:

.. code-block:: markdown

    ::uml:: format="png" alt="Sample sequence diagram"
      participant User

      User -> A: DoWork
      activate A #FFBBBB

      A -> A: Internal call
      activate A #DarkSalmon

      A -> B: << createRequest >>
      activate B

      B --> A: RequestCreated
      deactivate B
      deactivate A
      A -> User: Done
      deactivate A
    ::end-uml::

Another example from PlantUML_ site (activity diagram):

.. code-block:: rst

  .. uml::

    start
    :ClickServlet.handleRequest();
    :new page;
    if (Page.onSecurityCheck) then (true)
      :Page.onInit();
      if (isForward?) then (no)
	:Process controls;
	if (continue processing?) then (no)
	  stop
	endif
	
	if (isPost?) then (yes)
	  :Page.onPost();
	else (no)
	  :Page.onGet();
	endif
	:Page.onRender();
      endif
    else (false)
    endif

    if (do redirect?) then (yes)
      :redirect process;
    else
      if (do forward?) then (yes)
	:Forward request;
      else (no)
	:Render page template;
      endif
    endif

    stop

Generated image:

.. image:: http://plantuml.sourceforge.net/imgp/activity2_009.png
   :alt: Sample activity diagram



.. _PlantUML: http://plantuml.sourceforge.net
.. _Sabayon: http://www.sabayon.org
.. _Gentoo: http://www.gentoo.org
.. _layman: http://wiki.gentoo.org/wiki/Layman
.. _Graphviz: http://www.graphviz.org
.. _Pyhton-Markdown: http://pythonhosted.org/Markdown
.. _pandoc: http://johnmacfarlane.net/pandoc
.. _Haskell: http://www.haskell.org/haskellwiki/Haskell
.. _Python:: http://www.python.org
.. _Pelican: http://docs.getpelican.com/en
