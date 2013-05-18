ical
--------

This plugin read the calendar defined in the page metadata :calendar:

Example of code that can be added in page template ::

	{% if page.calendar %}
	<dl>
		{% for vevent in iCal %}
			<dt>{{ vevent.summary }}</dt>
			<dd>{{ vevent.description }}</dd>
		{% endfor %}
    </dl>
    {% endif %}

