HTML Entities for reStructuredText
##################################

This plugin allows you to enter HTML entities such as &copy;, &lt;, &#149; inline in a RST document, as opposed
to the tedious method of creating substitution definitions.

Roles
=====

Adds one inline role:

::

    :html_entity:

Usage
=====

::

    :html_entity:`copy` 2013 :html_entity:`lt` Pelican :html_entity:`gt` Industries :html_entity:`149` All Rights Reserved

produces:

|copy| 2013 |lt| Pelican |gt| Industries |bullet| All Rights Reserved

.. |copy|   unicode:: U+000A9 .. COPYRIGHT SIGN
.. |lt|     unicode:: U+003C  .. LESS THAN
.. |gt|     unicode:: U+003E  .. GREATER THAN
.. |bullet| unicode:: U+2022  .. BULLET
