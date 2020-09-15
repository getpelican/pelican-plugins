===================
Pelican Unity WebGL
===================

Compatibility
=============

Unity >= 5.6 (Tested on 5.6)

Usage
=====

Basic directive
---------------

.. code-block:: rst

	.. unitywebgl GAME_ID

**GAME_ID** is the required parameter. This is name of the directory, that contains your webgl build. This directory should be place in path, specified in config.py file, or with :gameroot: parameter.

Optional parameters
-------------------

.. code-block:: rst

	.. unitywebgl GAME_ID
		:gameroot: /games/new/
		:template: /games/templates/newtemplate
		:width: 640
		:height: 480

+-------------------+------------------+---------------------------------------------------------+
| Parameter         | default value    |                                                         |
+===================+==================+=========================================================+
| gameroot          | /games           | path to directory with games                            |
+-------------------+------------------+---------------------------------------------------------+
| templatepath      | /games/utemplate | path to template                                        |
+-------------------+------------------+---------------------------------------------------------+
| width             |                                                                            |
+-------------------+ Player resolution                                                          |
| height            |                                                                            |
+-------------------+------------------+---------------------------------------------------------+

.. note::
	Test pelican project can be found in *pelican_demo.zip* archive `here <https://github.com/mrpeidz/Unity-WebGL-RST-directive>`_

Configuration
=============

You can change default root directory, template path and player resolution in the *config.py* file.

Modifying html output template
------------------------------

You can modify the *template.txt* file to change html output.

Template parameters explanation:

+-------------------+-------------------------------+
| Parameter         | default value                 |
+===================+===============================+
| 0                 | game directory name           |
+-------------------+-------------------------------+
| 1                 | directory, where games placed |
+-------------------+-------------------------------+
| 2                 | template directory            |
+-------------------+-------------------------------+
| 3                 | width                         |
+-------------------+-------------------------------+
| 4                 | height                        |
+-------------------+-------------------------------+

About
=======

License: `MIT <https://opensource.org/licenses/MIT>`_

`Unity WebGL RST Directive github page <https://github.com/mrpeidz/Unity-WebGL-RST-directive>`_

**Mr.Page (c) 2017**