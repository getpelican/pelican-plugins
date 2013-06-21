#!/usr/bin/env python
import pelican
from jinja2.utils import generate_lorem_ipsum

# Copy into 'test_data' directory and run
blog_relative_path = '.'
config_file_path = blog_relative_path + '/pelican.conf.py'
output_dir_path = blog_relative_path + '/output'
plugin_file_path = '..'

def get_settings(config_file_path, output_dir_path, plugin_file_path, blog_relative_path):

	# Read settings
	_DEFAULT_CONFIG = pelican.settings._DEFAULT_CONFIG
	settings = pelican.settings.get_settings_from_file(config_file_path, default_settings=_DEFAULT_CONFIG)
	settings = pelican.settings.configure_settings(settings)

	# Fix the output path
	settings['OUTPUT_PATH'] = output_dir_path

	# Add feed summary settings
	settings['PLUGIN_PATH'] = plugin_file_path
	settings['PLUGINS'] = ['feed_summary','summary']
	settings['FEED_USE_SUMMARY'] = True
	settings['FEED_SUMMARY_LENGTH'] = 150

	# "Contents" file is missing from path, pelican doesn't run in any context without fixing this
	settings['FILES_TO_COPY'] = ((blog_relative_path+'/content/extra/robots.txt', 'robots.txt'),)
	settings['TEMPLATE_PAGES'] = {blog_relative_path+'/content/pages/jinja2_template.html': 'jinja2_template.html'}

	return settings

def write_long_content(blog_relative_path):
	# Generate two blog posts that are long enough to test the word limit in the feeds
	text1 = generate_lorem_ipsum(n=5, html=False, min=20, max=100)
	text2 = generate_lorem_ipsum(n=2, html=False, min=20, max=100)
	text3 = generate_lorem_ipsum(n=3, html=False, min=20, max=100)

	header1 = r"""Title: Hello, Part Deux
Date: 2012-12-16 15:19
Author: modernscientist
Slug: long_post1"""
	
	header2 = r"""Title: Hello, Again
Date: 2012-12-18 15:19
Author: modernscientist
Slug: long_post2"""
	
	# Test the 'FEED_SUMMARY_LENGTH' setting
	fh1 = open(blog_relative_path+'/content/long_post1.md','w')
	fh1.write(header1+'\n\n'+text1)
	fh1.close()

	# Test the summary plugin setting
	fh2 = open(blog_relative_path+'/content/long_post2.md','w')
	fh2.write(header2+'\n\n'+text2+'\n<!-- PELICAN_END_SUMMARY -->\n'+text3)
	fh2.close()

	return

if __name__ == "__main__":
	write_long_content(blog_relative_path)
	settings = get_settings(config_file_path, output_dir_path, plugin_file_path, blog_relative_path)
	Pelican = pelican.Pelican(settings)
	Pelican.run()