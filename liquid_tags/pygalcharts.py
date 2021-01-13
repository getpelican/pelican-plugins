"""
pygal Tag
---------
This implements a Liquid-style pygal tag for Pelican. JSON is used for the data,
and you can pass a bunch of pygal's 'config' items through as-is

[1] http://www.pygal.org/

Syntax
------
{% pygal
    {
        <graph data>
    }
%}

Examples
--------
{%
	pygal {
		"type": "bar",
		"title": "Test Chart",
		"x-labels" : {"from": 2002, "to": 2013},
		"data" : [
		{"title": "Firefox",
		 "values": [null, null, 0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1]},
		 {"title": "Chrome",
		 "values": [null, null, null, null, null, null,    0,  3.9, 10.8, 23.8, 35.3]},
		 {"title": "IE",
		 "values": [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1]},
		 {"title": "Others",
		 "values": [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5]}
		]
	}
%}

{%
	pygal {
		"type": "pie",
		"half_pie": true,
		"title": "Browser usage in February 2012 (in %)",
		"data" : [
		{"title": "IE",
		 "values": 19.5},
		 {"title": "Firefox",
		 "values": 36.6},
		 {"title": "Chrome",
		 "values": 36.3},
		 {"title": "Safari",
		 "values": 4.5},
		 {"title": "Opera",
		 "values": 2.3}
		]
	}
%}

{%
	pygal {
		"type": "pie",
			"config": {
			"show_legend": false,
			"print_values": true,
			"show_y_labels": true
		},
		"title": "Browser usage in February 2012 (in %)",
		"data" : [
		{"title": "IE",
		 "values": 19.5},
		 {"title": "Firefox",
		 "values": 36.6},
		 {"title": "Chrome",
		 "values": 36.3},
		 {"title": "Safari",
		 "values": 4.5},
		 {"title": "Opera",
		 "values": 2.3}
		]
	}
%}



...


Output
------
<<div class="pygal" style="text-align: center;"><embed type="image/svg+xml" src=SVG_MARKUP_EMBEDDED style="max-width:1000px"/></div>

"""

import base64
import re
from json import loads
from .mdx_liquid_tags import LiquidTags

SYNTAX = '{% pygal (data) %}'
DOT_BLOCK_RE = re.compile(r'^\s*\{\s*(?P<code>.*\})\s*\}$', re.MULTILINE | re.DOTALL)


def run_pygal(data, options=[], format='svg'):
    """ Runs pygal programs and returns image data
    """
    import pygal

    chart_title = data.get('title', None)
    chart_type = data.get('type', '').lower()
    # Config options are pretty much proxied straight through from the JSON dict into the object
    config = pygal.Config()
    config_dict = data.get('config', {})
    for key in config_dict.keys():
        setattr(config, key, config_dict[key])

    if chart_type == 'bar':
        chart = pygal.HorizontalBar(config) if data.get('horizontal', False) else pygal.Bar(config)
    elif chart_type == 'line':
        chart = pygal.Line(config)
    elif chart_type == 'pie':
        ir=data.get('inner_radius', 0.0)
        hp=data.get('half_pie', False)
        chart = pygal.Pie(config, inner_radius=ir, half_pie=hp)
    else:
        print('undefined or unknown chart type')

    if chart is not None:
        chart.title = data.get('title', None)
        # Do labels (if present)
        label_data = data.get('x-labels', None)
        if isinstance(label_data, list):
            # use list
            chart.x_labels = label_data
        elif isinstance(label_data, dict):
            # use a range
            range_from = label_data.get('from', 0)
            range_to = label_data.get('to', 0)
            chart.x_labels = map(str, range(range_from, range_to))
        # insert data
        for data_set in data.get('data', []):
            title = data_set.get('title', None)
            values = data_set.get('values', None)
            chart.add(title, values)
        # now render
        result = chart.render_data_uri()
    else:
        result = None
    return result

@LiquidTags.register('pygal')
def pygal_parser(preprocessor, tag, markup):
    """ Simple pygal parser """
    # Find JSON payload
    data = loads(markup)
    if tag == 'pygal' and data is not None:
        # Run generation of chart
        output = run_pygal(data)
        # Return embedded SVG image
        return '<div class="pygal" style="text-align: center;"><embed type="image/svg+xml" src=%s style="max-width:1000px"/></div>' % output

    else:
        raise ValueError('Error processing input. \nExpected syntax: {0}'.format(SYNTAX))

#----------------------------------------------------------------------
# This import allows image tag to be a Pelican plugin
from .liquid_tags import register
