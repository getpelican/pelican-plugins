"""
Video Privacy Enhancer
--------------------------

Authored by Jacob Levernier, 2014
Released under the GNU AGPLv3

For more information on this plugin, please see the attached Readme.md file.

"""

"""
LIBRARIES FOR PYTHON TO USE
"""

from pelican import signals # For making this plugin work with Pelican.

import os.path # For checking whether files are present in the filesystem.

import re # For using regular expressions.

import logging
logger = logging.getLogger(__name__) # For using logger.debug() to log errors or other notes.

import six
# import urllib.request
import six.moves.urllib.request 

from . import video_service_thumbnail_url_generating_functions as video_thumbnail_functions # These are functions defined in 'video_service_thumbnail_url_generating_functions.py', which is located in the same directory as this file. 

"""
END OF LIBRARIES
"""

"""
SETTINGS
"""

# Do not use a leading or trailing slash below (e.g., use "images/video-thumbnails"):
output_directory_for_thumbnails = "images/video-thumbnails"

# See the note in the Readme file re: adding support for other video services to this list.
supported_video_services = {
	"youtube": {
		"shortcode_not_including_exclamation_point": "youtube",
		"function_for_generating_thumbnail_url": video_thumbnail_functions.generate_thumbnail_download_link_youtube,
	},
	"vimeo": {
		"shortcode_not_including_exclamation_point": "vimeo",
		"function_for_generating_thumbnail_url": video_thumbnail_functions.generate_thumbnail_download_link_vimeo,
	},
}

""" 
In order for this plugin to work optimally, you need to do just a few things:

1. Enable the plugn in pelicanconf.py (see http://docs.getpelican.com/en/3.3.0/plugins.html for documentation):  
	PLUGIN_PATH = "/pelican-plugins"  
	PLUGINS = ["video_privacy_enhancer"]

2a. If necessary, install jQuery on your site (See https://stackoverflow.com/questions/1458349/installing-jquery -- the jQuery base file should go into your Pelican theme's 'static' directory)

2b. Copy the jQuery file in this folder into, for example, your_theme_folder/static/video_privacy_enhancer_jQuery.js, and add a line like this to the <head></head> element of your website's base.html (or equivalent) template:
	`<script src="{{ SITEURL }}/theme/video_privacy_enhancer_jquery.js"></script> <!--Load jQuery functions for the Video Privacy Enhancer Pelican plugin -->`

3. Choose a default video embed size and add corresponding CSS to your theme's CSS file:

Youtube allows the following sizes in its embed GUI (as of this writing, in March 2014). I recommend choosing one, and then having the iframe for the actual video embed match it (so that it's a seamless transition). This can be handled with CSS in both cases, so I haven't hard-coded it here:
	1280 W x 720 H
	853 W x 480 H
	640 W x 360 H
	560 W x 315 H

Here's an example to add to your CSS file:

```
/* For use with the video-privacy-enhancer Pelican plugin */
img.video-embed-dummy-image,
iframe.embedded_privacy_video {
	width: 853px;
	max-height: 480px;

	/* Center the element on the screen */
	display: block;
	margin-top: 2em;
	margin-bottom: 2em;
	margin-left: auto;
	margin-right: auto;
}
iframe.embedded_privacy_video {
	width: 843px;
	height: 480px;
}
```

"""

"""
END SETTINGS
"""

# A function to check whtether output_directory_for_thumbnails (a variable set above in the SETTINGS section) exists. If it doesn't exist, we'll create it.
def check_for_thumbnail_directory(pelican_output_path):
	# Per http://stackoverflow.com/a/84173, check if a file exists. isfile() works on files, and exists() works on files and directories.
	try:
		if not os.path.exists(pelican_output_path + "/" + output_directory_for_thumbnails): # If the directory doesn't exist already...
			os.makedirs(pelican_output_path + "/" + output_directory_for_thumbnails) # Create the directory to hold the video thumbnails.
			return True
	except Exception as e:
		logger.error("Video Privacy Enhancer Plugin: Error in checking if thumbnail folder exists and making the directory if it doesn't: %s", e) # In case something goes wrong.
		return False


def download_thumbnail(video_id_from_shortcode, video_thumbnail_url, video_service_name, pelican_output_path):
	# Check if the thumbnail directory exists already:
	check_for_thumbnail_directory(pelican_output_path)
	
	# Check if the thumbnail for this video exists already (if it's been previously downloaded). If it doesn't, download it:
	if not os.path.exists(pelican_output_path + "/" + output_directory_for_thumbnails + "/" + video_service_name + "_" + video_id_from_shortcode + ".jpg"): # If the thumbnail doesn't already exist...
		logger.debug("Video Privacy Enhancer Plugin: Downloading thumbnail from the following url: " + video_thumbnail_url)
		six.moves.urllib.request.urlretrieve(video_thumbnail_url, pelican_output_path + "/" + output_directory_for_thumbnails + "/" + video_service_name + "_" + video_id_from_shortcode + ".jpg") # Download the thumbnail. This follows the instructions at http://www.reelseo.com/youtube-thumbnail-image/ for downloading YouTube thumbnail images.


# A function to read through each page and post as it comes through from Pelican, find all instances of a shortcode (e.g., `!youtube(...)`) and change it into an HTML <img> element with the video thumbnail.
# 'dictionary_of_services' below should be the dictionary defined in the settings above, which includes the service's name as the dictionary key, and, for each service, has a dictionary containing 'shortcode_to_search_for_not_including_exclamation_point' and 'function_for_generating_thumbnail_url'
def process_shortcodes(data_passed_from_pelican):
	dictionary_of_services = supported_video_services # This should be defined in the settings section above.
	
	if not data_passed_from_pelican._content: # If the item passed from Pelican has a "content" attribute (i.e., if it's not an image file or something else like that). NOTE: data_passed_from_pelican.content (without an underscore in front of 'content') seems to be read-only, whereas data_passed_from_pelican._content is able to be overwritten. This is somewhat explained in an IRC log from 2013-02-03 from user alexis to user webdesignhero_ at https://botbot.me/freenode/pelican/2013-02-01/?tz=America/Los_Angeles.
		return # Exit the function, essentially passing over the (non-text) file.
	
	# Loop through services (e.g., youtube, vimeo), processing the output for each:
	for video_service_name, video_service_information in six.iteritems(dictionary_of_services):
		
		# Good for debugging:
		logger.debug("Video Privacy Enhancer Plugin: The name of the current service being processed is '" + video_service_name + "'")
		
		shortcode_to_search_for_not_including_exclamation_point = video_service_information['shortcode_not_including_exclamation_point']
		logger.debug("Video Privacy Enhancer Plugin: Currently looking for the shortcode '" + shortcode_to_search_for_not_including_exclamation_point + "'")
		
		function_for_generating_thumbnail_url = video_service_information['function_for_generating_thumbnail_url']
		
		all_instances_of_the_shortcode = re.findall(r'(?<!\\\)\!' + shortcode_to_search_for_not_including_exclamation_point + r'.*?\)', data_passed_from_pelican._content) # Use a regular expression to find every instance of, e.g., '!youtube' followed by anything up to the first matching ')'.
		
		if(len(all_instances_of_the_shortcode) > 0): # If the article/page HAS any shortcodes, go on. Otherwise, don't (to do so would inadvertantly wipe out the output content for that article/page).
			replace_shortcode_in_text = "" # This just gives this an initial value before going into the loop below.

			# Go through each shortcode instance that we found above, and parse it:
			for shortcode_to_parse in all_instances_of_the_shortcode:

				video_id_from_shortcode = re.findall('(?<=' + shortcode_to_search_for_not_including_exclamation_point + r'\().*?(?=\))', shortcode_to_parse)[0] # Get what's inside of the parentheses in, e.g., '!youtube(...).'
				
				# print "Video ID is " + video_id_from_shortcode # Good for debugging purposes.
				
				# Use the Pelican pelicanconf.py settings:
				pelican_output_path = data_passed_from_pelican.settings['OUTPUT_PATH']
				pelican_site_url = data_passed_from_pelican.settings['SITEURL']
				
				# Download the video thumbnail if it's not already on the filesystem:
				video_thumbnail_url = function_for_generating_thumbnail_url(video_id_from_shortcode)
				
				download_thumbnail(video_id_from_shortcode, video_thumbnail_url, video_service_name, pelican_output_path)
				
				# Replace the shortcode (e.g., '!youtube(...)') with '<img>...</img>'. Note that the <img> is given a class that the jQuery file mentioned at the top of this file will watch over. Any time an image with that class is clicked, the jQuery function will trigger and turn it into the full video embed.
				replace_shortcode_in_text = re.sub(r'\!' + shortcode_to_search_for_not_including_exclamation_point + r'\(' + video_id_from_shortcode + r'\)', r'<img class="video-embed-dummy-image" id="' + video_id_from_shortcode + '" src="' +  pelican_site_url + '/' + output_directory_for_thumbnails + '/' + video_service_name + '_' + video_id_from_shortcode + '.jpg" alt="Embedded Video - Click to view" title="Embedded Video - Click to view" embed-service="' + video_service_name + '"></img>', data_passed_from_pelican._content)
				
				# Replace the content of the page or post with our now-updated content (having gone through all instances of the shortcode and updated them all, exiting the loop above.
				data_passed_from_pelican._content = replace_shortcode_in_text


# Make Pelican work (see http://docs.getpelican.com/en/3.3.0/plugins.html#how-to-create-plugins):
def register():
	signals.content_object_init.connect(process_shortcodes)
