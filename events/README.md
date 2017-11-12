Events plugin
=============

This plugin allows you to put events in your content via metadata. An
iCal file is generated containing all events.


Dependencies
------------

This plugin depends on the `icalendar` package, which can be installed
using APT, DNF/YUM or pip:

```sh
pip install icalendar
```


Settings
--------

You can define settings with the `PLUGIN_EVENTS` variable:

```python
PLUGIN_EVENTS = {
    'ics_fname': 'calendar.ics',
}
```

Settings:
- `ics_fname`: Where the iCal file is written


Usage
-----

When you write an article, you can use theses metadatas
- `event-start`: When the event will start in "YYYY-MM-DD hh:mm"
- `event-end`: When the event will stop in "YYYY-MM-DD hh:mm"
- `event-duration`: How many times the event will continue [1]
- `event-location`: Where the event take place

[1] To specify the event duration, use a number followed by a time unit:
- `w`: weeks
- `d`: days
- `h`: hours
- `m`: minutes
- `s`: seconds


Exemples
--------

Example in ReST format:
```ReST
:event-start: 2015-01-21 10:30
:event-duration: 2h
:event-location: somewhere
```

Example in Markdown format:
```markdown
Event-start: 2015-01-21 10:30
Event-duration: 2h
Event-location: somewhere
```


Dedicated page
--------------

To generate an sorted event list in a dedicated page:
- Copy the `events_list.html` template under the templates directory of your theme
- Create a page for this list, for exemple in `content/pages/events_list.rst`
- Write these metadatas in your page:
```ReST
Events list
###########
:slug: events-list
:summary:
:template: events_list
```
