HTML Entities for reStructuredText
##################################

This plugin allows you to enter HTML entities such as &copy;, &lt;, &#149; in a RST document.

Roles
=====

Adds one inline role:

::
    :html_entity:

Usage
=====

::
    :html_entity:`copy` 2013 :html_entity:`lt`Pelican:html_entity:`gt` Industries :html_entity:`149` All Rights Reserved

produces

.. raw:: html

    &copy; 2013 &lt;Pelican&gt; Industries &#149; All Rights Reserved

