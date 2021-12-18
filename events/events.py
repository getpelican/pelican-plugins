# -*- coding: utf-8 -*-
"""
events plugin for Pelican
=========================

This plugin looks for and parses an "events" directory and generates
blog posts with a user-defined event date. (typically in the future)
It also generates an ICalendar v2.0 calendar file.
https://en.wikipedia.org/wiki/ICalendar


Author: Federico Ceratto <federico.ceratto@gmail.com>
Released under AGPLv3+ license, see LICENSE
"""

from datetime import datetime, timedelta
from pelican import signals, utils, contents
from collections import namedtuple, defaultdict
import icalendar
import logging
import os.path
import pytz

log = logging.getLogger(__name__)

TIME_MULTIPLIERS = {
    'w': 'weeks',
    'd': 'days',
    'h': 'hours',
    'm': 'minutes',
    's': 'seconds'
}

events = []
localized_events = defaultdict(list)


def parse_tstamp(metadata, field_name):
    """Parse a timestamp string in format "YYYY-MM-DD HH:MM"

    :returns: datetime
    """
    try:
        return datetime.strptime(metadata[field_name], '%Y-%m-%d %H:%M')
    except Exception as e:
        log.error("Unable to parse the '%s' field in the event named '%s': %s" \
            % (field_name, metadata['title'], e))
        raise


def parse_timedelta(metadata):
    """Parse a timedelta string in format [<num><multiplier> ]*
    e.g. 2h 30m

    :returns: timedelta
    """

    chunks = metadata['event-duration'].split()
    tdargs = {}
    for c in chunks:
        try:
            m = TIME_MULTIPLIERS[c[-1]]
            val = int(c[:-1])
            tdargs[m] = val
        except KeyError:
            log.error("""Unknown time multiplier '%s' value in the \
'event-duration' field in the '%s' event. Supported multipliers \
are: '%s'.""" % (c, metadata['title'], ' '.join(TIME_MULTIPLIERS)))
            raise RuntimeError("Unknown time multiplier '%s'" % c)
        except ValueError:
            log.error("""Unable to parse '%s' value in the 'event-duration' \
field in the '%s' event.""" % (c, metadata['title']))
            raise ValueError("Unable to parse '%s'" % c)


    return timedelta(**tdargs)


def basic_isoformat(datetime_value):
    return datetime_value.strftime("%Y%m%dT%H%M%S")


def parse_article(content):
    """Collect articles metadata to be used for building the event calendar

    :returns: None
    """
    if not isinstance(content, contents.Article):
        return

    if 'event-start' not in content.metadata:
        return

    dtstart = parse_tstamp(content.metadata, 'event-start')

    if 'event-end' in content.metadata:
        dtend = parse_tstamp(content.metadata, 'event-end')

    elif 'event-duration' in content.metadata:
        dtdelta = parse_timedelta(content.metadata)
        dtend = dtstart + dtdelta

    else:
        msg = "Either 'event-end' or 'event-duration' must be" + \
            " speciefied in the event named '%s'" % content.metadata['title']
        log.error(msg)
        raise ValueError(msg)

    content.event_plugin_data = {"dtstart": dtstart, "dtend": dtend}

    events.append(content)


def generate_ical_file(generator):
    """Generate an iCalendar file
    """
    global events
    ics_fname = generator.settings['PLUGIN_EVENTS']['ics_fname']
    if not ics_fname:
        return

    ics_fname = os.path.join(generator.settings['OUTPUT_PATH'], ics_fname)
    log.debug("Generating calendar at %s with %d events" % (ics_fname, len(events)))

    tz = generator.settings.get('TIMEZONE', 'UTC')
    tz = pytz.timezone(tz)

    ical = icalendar.Calendar()
    ical.add('prodid', '-//My calendar product//mxm.dk//')
    ical.add('version', '2.0')

    DEFAULT_LANG = generator.settings['DEFAULT_LANG']
    curr_events = events if not localized_events else localized_events[DEFAULT_LANG]

    for e in curr_events:
        ie = icalendar.Event(
            summary=e.metadata['summary'],
            dtstart=basic_isoformat(e.event_plugin_data["dtstart"]),
            dtend=basic_isoformat(e.event_plugin_data["dtend"]),
            dtstamp=basic_isoformat(e.metadata['date']),
            priority=5,
            uid=e.metadata['title'] + e.metadata['summary'],
        )
        if 'event-location' in e.metadata:
            ie.add('location', e.metadata['event-location'])

        ical.add_component(ie)

    with open(ics_fname, 'wb') as f:
        f.write(ical.to_ical())


def generate_localized_events(generator):
    """ Generates localized events dict if i18n_subsites plugin is active """

    if "i18n_subsites" in generator.settings["PLUGINS"]:
        if not os.path.exists(generator.settings['OUTPUT_PATH']):
            os.makedirs(generator.settings['OUTPUT_PATH'])

        for e in events:
            if "lang" in e.metadata:
                localized_events[e.metadata["lang"]].append(e)
            else:
                log.debug("event %s contains no lang attribute" % (e.metadata["title"],))


def generate_events_list(generator):
    """Populate the event_list variable to be used in jinja templates"""

    if not localized_events:
        generator.context['events_list'] = sorted(events, reverse = True,
                                                  key=lambda ev: (ev.event_plugin_data["dtstart"], ev.event_plugin_data["dtend"]))
    else:
        generator.context['events_list'] = {k: sorted(v, reverse = True,
                                                      key=lambda ev: (ev.event_plugin_data["dtstart"], ev.event_plugin_data["dtend"]))
                                            for k, v in localized_events.items()}

def initialize_events(article_generator):
    """
    Clears the events list before generating articles to properly support plugins with
    multiple generation passes like i18n_subsites
    """

    del events[:]
    localized_events.clear()

def register():
    signals.article_generator_init.connect(initialize_events)
    signals.content_object_init.connect(parse_article)
    signals.article_generator_finalized.connect(generate_localized_events)
    signals.article_generator_finalized.connect(generate_ical_file)
    signals.article_generator_finalized.connect(generate_events_list)


