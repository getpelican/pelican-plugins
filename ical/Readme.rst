ical
--------

This plugin read the calendar in the page metadata :calendar:

    {% if page.calendar %}
		{% for machin in iCal %}
			{{ machin}}<br/>
		{% endfor %}
    {% endif %}
