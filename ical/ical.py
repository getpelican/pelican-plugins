# -*- coding: utf-8 -*-
"""
ical plugin for Pelican
===========================

This plugin read the calendar defined in the page metadata :calendar:


"""

from icalendar import Calendar, Event
from pelican import signals
from pelican import utils
import pytz
import datetime

def init_cal(generator):
	calDict = {}
	generator.context['events'] = calDict

def add_ical(generator, metadata):
	if 'calendar' in metadata.keys():
		summ = []
		path = metadata['calendar']
		cal = Calendar.from_ical(open(path,'rb').read())
		for element in cal.walk():
			eventdict = {}
			if element.name == "VEVENT":
				eventdict['summary'] = element.get('summary')
				if element.get('description') != None :
					eventdict['description'] = element.get('description').replace('\n\n', '<br>')
				eventdict['dtstart'] = element.get('dtstart').dt
				eventdict['dtend'] = element.get('dtend').dt
				summ.append(eventdict)
		calId = utils.slugify(metadata['title'])
		generator.context['events'][calId] = summ

		
def register():
    signals.pages_generator_init.connect(init_cal)
    signals.pages_generate_context.connect(add_ical)
