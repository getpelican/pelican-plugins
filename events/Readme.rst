events
----

This plugin scans blog posts for an events.
It also generates an ``.ical`` calendar file.

Dependencies
------------

This plugin depends on the ``icalendar`` package, which can be installed
using APT or RPM or, if you are unlucky, via pip::

    pip install icalendar

Usage
-----

Add the following to pelicanconf.py::
    PLUGIN_EVENTS = {
        'ics_fname': 'calendar.ics',
    }

Create articles and usual and add the "event-start" metadata to turn them into
events. The event start is independent of the article "date".
"event-start" is in "YYYY-MM-DD hh:mm" format.
Also add "event-end", in the same format, or "event-duration" as a number
followed by a dimension:

w: weeks
d: days
h: hours
m: minutes
s: seconds

You can also specify an optional "location"

Example in ReST format::

    :event-start: 2015-01-21 10:30
    :event-duration: 2h
    :location: somewhere


To generate an sorted event list in a dedicated page copy the events_list.html
template under the templates directory in your theme, then create a page:

content/pages/events_list.rst::

 Events list
 ###########
 :slug: events-list
 :summary:
 :template: events_list
