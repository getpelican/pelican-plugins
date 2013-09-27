# -*- coding: utf-8 -*-
"""
ical plugin for Pelican
=======================

This plugin looks for and parses an .ics file if it is defined in a given
page's :calendar: metadata. One calendar can be defined per page.

"""

from icalendar import Calendar, Event
from pelican import signals , utils
import pytz
import datetime
import os.path

def init_cal(generator):
    # initialisation of the calendar dictionary
    # you can add one calendar per page
    calDict = {}
    generator.context['events'] = calDict

def add_ical(generator, metadata):
    # check if a calendar is here
    if 'calendar' in metadata.keys():
        summ = []
        path = metadata['calendar']
        if not os.path.isabs(path):
            path = os.path.abspath(metadata['calendar'])
        cal = Calendar.from_ical(open(path,'rb').read())
        for element in cal.walk():
            eventdict = {}
            if element.name == "VEVENT":
                if element.get('summary') != None:
                    eventdict['summary'] = element.get('summary')
                if element.get('description') != None:
                    eventdict['description'] = element.get('description')
                if element.get('url') != None:
                    eventdict['url'] = element.get('url')
                if element.get('dtstart') != None:
                    eventdict['dtstart'] = element.get('dtstart').dt
                if element.get('dtend') != None:
                    eventdict['dtend'] = element.get('dtend').dt
                summ.append(eventdict)
        # the id of the calendar is the slugified name of the page
        calId = utils.slugify(metadata['title'])
        generator.context['events'][calId] = summ


def register():
    signals.page_generator_init.connect(init_cal)
    signals.page_generator_context.connect(add_ical)
