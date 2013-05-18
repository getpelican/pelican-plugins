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
	
	if 'calendar' in metadata.keys():
		summ = []
		path = metadata['calendar']
		cal = Calendar.from_ical(open(path,'rb').read())
		for element in cal.walk():
			if element.name == "VEVENT":
				summ.append(element.get('summary'))
		generator.context['iCal'] = summ
		
def register():
    signals.pages_generate_context.connect(add_ical)
