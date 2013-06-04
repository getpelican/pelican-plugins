ical
--------

This plugin read the calendar defined in the page metadata : calendar :

with::

    :calendar: /path/to/your/ics/file

Example of code that can be added in page template ::


    {% if page.calendar %}
    <dl>
        {% for vevent in  events[page.slug] %}
            <dt>{{ vevent.summary }}</dt>
            <dd>{{ vevent.description|replace('\n\n', '<br>') }}</dd>
            <dd>{{ vevent.dtstart }}</dd>
            <dd>{{ vevent.dtend }}</dd>
            <dd class="footer"><a href="{{ vevent.url }}" target="_blank">See more</a></dd>
        {% endfor %}
    </dl>
    {% endif %}
    
this plugins needs icalendar module installed::

	pip install icalendar

