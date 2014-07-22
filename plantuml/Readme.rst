PlantUML plugin for Pelican rst documents
=========================================

This plugin allows you to define UML diagrams directly into rst documents using the great
PlantUML_ tool.

This plugin gets the content of ``uml`` directive, passes it to the external
program PlantUML_ and then links the generated image to the document.

Installation
------------

You need to install PlantUML_ (see the site for details) and Graphviz_ 2.26.3 or later.
The plugin expects a program ``plantuml`` in the classpath. If not installed by your package
manager, you can create a shell script and place it somewhere in the classpath. For example,
save te following into ``/usr/local/bin/plantuml`` (supposing PlantUML_ installed into
``/opt/plantuml``):

.. code-block:: bash

    #!/bin/bash
    java -jar /opt/plantuml/plantuml.jar ${@}

For Gentoo_ there is an ebuild at http://gpo.zugaina.org/dev-util/plantuml/RDep: you can download
the ebuild and the ``files`` subfolder or you can add the ``zugaina`` repository with _layman
(raccomended).

Usage
-----

Add ``plantuml`` to plugin list in ``pelicanconf.py``. For example:

.. code-block:: ptyhon

    PLUGINS = [ "sitemap", "plantuml" ]

Use the ``uml`` directive to start UML diagram description. It is not necessary to enclose
diagram body between ``@startuml`` and ``@enduml`` directives: they are added automatically 
before calling ``plantuml``.

In addition to ``class`` and
``alt`` options common to all images, you can use the ``format`` option to select what kind
of image must be produced. At the moment only ``png`` and ``svg`` are supported; the default
is ``png``.

Please note that the ``format`` option in not recognized by the ``plantuml`` extension of
``rst2pdf`` utility (call it with ``-e plantuml.py``) so if you use it you can get errors from
that program.
  
Examples
--------

Sequence diagram (from PlantUML_ site):

.. code-block:: rst

  .. uml::

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



.. _PlantUML: http://plantuml.sourceforge.net
.. _Sabayon: http://www.sabayon.org
.. _Gentoo: http://www.gentoo.org
.. _layman: http://wiki.gentoo.org/wiki/Layman
.. _Graphviz: http://www.graphviz.org
