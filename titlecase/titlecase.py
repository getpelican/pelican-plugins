# -*- coding: utf-8 -*-
"""
Original Perl version by: John Gruber http://daringfireball.net/ 10 May 2008
Python version by Stuart Colville http://muffinresearch.co.uk
Ported to Pelican by Jean-Ray Arseneau (http://theinterstitial.net)
License: http://www.opensource.org/licenses/mit-license.php

"""

import re

from pelican import signals

def content_to_titlecase(text):
	SMALL = 'a|an|and|as|at|but|by|en|for|if|in|of|on|or|the|to|v\.?|via|vs\.?'
	PUNCT = r"""!"#$%&'‘()*+,\-./:;?@[\\\]_`{|}~"""

	SMALL_WORDS = re.compile(r'^(%s)$' % SMALL, re.I)
	INLINE_PERIOD = re.compile(r'[a-z][.][a-z]', re.I)
	UC_ELSEWHERE = re.compile(r'[%s]*?[a-zA-Z]+[A-Z]+?' % PUNCT)
	CAPFIRST = re.compile(r"^[%s]*?([A-Za-z])" % PUNCT)
	SMALL_FIRST = re.compile(r'^([%s]*)(%s)\b' % (PUNCT, SMALL), re.I)
	SMALL_LAST = re.compile(r'\b(%s)[%s]?$' % (SMALL, PUNCT), re.I)
	SUBPHRASE = re.compile(r'([:.;?!][ ])(%s)' % SMALL)
	APOS_SECOND = re.compile(r"^[dol]{1}['‘]{1}[a-z]+$", re.I)
	ALL_CAPS = re.compile(r'^[A-Z\s%s]+$' % PUNCT)
	UC_INITIALS = re.compile(r"^(?:[A-Z]{1}\.{1}|[A-Z]{1}\.{1}[A-Z]{1})+$")
	MAC_MC = re.compile(r"^([Mm]a?c)(\w+)")
    
	lines = re.split('[\r\n]+', text)
	processed = []
	for line in lines:
	   all_caps = ALL_CAPS.match(line)
	   words = re.split('[\t ]', line)
	   tc_line = []
	   for word in words:
		  if all_caps:
			 if UC_INITIALS.match(word):
				tc_line.append(word)
				continue
			 else:
				word = word.lower()
	  
		  if APOS_SECOND.match(word):
			 word = word.replace(word[0], word[0].upper())
			 word = word.replace(word[2], word[2].upper())
			 tc_line.append(word)
			 continue
		  if INLINE_PERIOD.search(word) or UC_ELSEWHERE.match(word):
			 tc_line.append(word)
			 continue
		  if SMALL_WORDS.match(word):
			 tc_line.append(word.lower())
			 continue

		  match = MAC_MC.match(word)
		  if match:
			 tc_line.append("%s%s" % (match.group(1).capitalize(),
							   match.group(2).capitalize()))
			 continue
	  
		  hyphenated = []
		  for item in word.split('-'):
			 hyphenated.append(CAPFIRST.sub(lambda m: m.group(0).upper(), item))
		  tc_line.append("-".join(hyphenated))
	

	   result = " ".join(tc_line)

	   result = SMALL_FIRST.sub(lambda m: '%s%s' % (
		  m.group(1),
		  m.group(2).capitalize()
	   ), result)

	   result = SMALL_LAST.sub(lambda m: m.group(0).capitalize(), result)

	   result = SUBPHRASE.sub(lambda m: '%s%s' % (
		  m.group(1),
		  m.group(2).capitalize()
	   ), result)
	
	   processed.append(result)

	return "\n".join(processed)

class TitleCase(object):
	"""
	TileCase class to initialize the Title Case jinja filter.
	"""
    
	def __call__(self, text):
		text = content_to_titlecase(text)
		return text


def initialize(generator):
	generator.env.filters.update({'titlecase': TitleCase()})

def register():
    signals.generator_init.connect(initialize)
