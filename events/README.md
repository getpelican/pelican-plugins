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

You can use the following metadata in your content:
- `event-start`: When the event will start in "YYYY-MM-DD hh:mm"
- `event-end`: When the event will stop in "YYYY-MM-DD hh:mm"
- `event-duration`: The duration of the event [1]
- `event-location`: Where the event takes place

[1] To specify the event duration, use a number followed by a time unit:
- `w`: weeks
- `d`: days
- `h`: hours
- `m`: minutes
- `s`: seconds


Examples
--------

Example in reST format:
```reST
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

To generate a sorted event list in its own dedicated page:
- Copy the `events_list.html` template under the templates directory of your theme
- Create a page for this list, for example in `content/pages/events_list.rst`
- Include the following metadata in your content:
```reST
Events list
###########
:slug: events-list
:summary:
:template: events_list
```
