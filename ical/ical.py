# -*- coding: utf-8 -*-
"""
iCal plugin for Pelican
===========================

descritpion
"""

from icalendar import Calendar, Event
from pelican import signals
import pytz
import datetime

def add_ical(generator, metadata):
	"""Provides events list to templates
	"""
	
	if 'calendar' in metadata.keys():
		summ = []
		path = metadata['calendar']
		cal = Calendar.from_ical(open(path,'rb').read())
		for element in cal.walk():
			eventdict = {}
			if element.name == "VEVENT":
				eventdict['summary'] = element.get('summary')
				eventdict['description'] = element.get('description').replace('\n\n', '<br>')
				eventdict['dtstart'] = element.get('dtstart').dt
				eventdict['dtend'] = element.get('dtend').dt
				summ.append(eventdict)
		generator.context['events'] = summ
		
def register():
    signals.pages_generate_context.connect(add_ical)
