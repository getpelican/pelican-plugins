ical
----

This plugin looks for and parses an ``.ics`` file if it is defined in a given
page's ``calendar`` metadata. One calendar can be defined per page.

Dependencies
------------

This plugin depends on the ``icalendar`` package, which can be installed via
pip::

	pip install icalendar

Usage
-----

For a reST-formatted page, include the following line in the metadata::

    :calendar: /path/to/your/ics/file

For Markdown, include the following line in the page metadata::

    Calendar: /path/to/your/ics/file

Following is some example code that can be added to your theme's ``page.html``
template in order to display the calendar::

    {% if page.calendar %}
    <dl>
        {% for vevent in events[page.slug] %}
            <dt>{{ vevent.summary }}</dt>
            <dd>{{ vevent.description|replace('\n\n', '<br>') }}</dd>
            <dd>{{ vevent.dtstart }}</dd>
            <dd>{{ vevent.dtend }}</dd>
            <dd class="footer"><a href="{{ vevent.url }}">See more</a></dd>
        {% endfor %}
    </dl>
    {% endif %}
