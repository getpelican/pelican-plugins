ical
--------

This plugin read the calendar defined in the page metadata :calendar:

with

:calendar: /path/to/your/ics/file

Example of code that can be added in page template ::


	{% if page.calendar %}
	<dl>
		{% for vevent in  events[page.slug] %}
			<dt>{{ vevent.summary }}</dt>
			<dd>{{ vevent.description }}</dd>
			<dd>{{ vevent.dtstart }}</dd>
			<dd>{{ vevent.dtend }}</dd>
		{% endfor %}
    </dl>
    {% endif %}
    
this plugins needed icalendar module installed and works only for pages

