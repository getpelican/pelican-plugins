"""
Video Privacy Enhancer
--------------------------

Authored by Jacob Levernier, 2014
Released under the GNU AGPLv3

For more information on this plugin, please see the attached Readme.md file.

"""

"""
SETTINGS
"""

# Do not use a leading or trailing slash below (e.g., use "images/video-thumbnails"):
output_directory_for_thumbnails = "images/video-thumbnails"

""" 
In order for this plugin to work optimally, you need to do just a few things:

1. Enable the plugn in pelicanconf.py (see http://docs.getpelican.com/en/3.3.0/plugins.html for documentation):  
    PLUGIN_PATH = "/pelican-plugins"  
    PLUGINS = ["video_privacy_enhancer"]

2a. If necessary, install jQuery on your site (See https://stackoverflow.com/questions/1458349/installing-jquery -- the jQuery base file should go into your Pelican themes 'static' directory)

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
img.video-embed-dummy-image.
iframe.embedded_youtube_video {
    width: 843px;
    max-height: 480px;

    /* Center the element on the screen */
    display: block;
    margin-top: 2em;
    margin-bottom: 2em;
    margin-left: auto;
    margin-right: auto;
}
iframe.embedded_youtube_video {
    width: 843px;
    height: 480px;
}
```

"""


"""
END SETTINGS
"""


from pelican import signals # For making this plugin work with Pelican.

import os.path # For checking whether files are present in the filesystem.

import re # For using regular expressions.
import urllib # For downloading the video thumbnails.

import logging
logger = logging.getLogger(__name__) # For using logger.debug() to log errors or other notes.


# A function to check whtether output_directory_for_thumbnails (a variable set above in the SETTINGS section) exists. If it doesn't exist, we'll create it.
def check_for_thumbnail_directory(pelican_output_path):
    # Per http://stackoverflow.com/a/84173, check if a file exists. isfile() works on files, and exists() works on files and directories.
    try:
        if not os.path.exists(pelican_output_path + "/" + output_directory_for_thumbnails): # If the directory doesn't exist already...
            os.makedirs(pelican_output_path + "/" + output_directory_for_thumbnails) # Create the directory to hold the video thumbnails.
            return True
    except:
        print logger.debug("Error in checking if thumbnail folder exists and making the directory if it doesn't.") # In case something goes wrong.
        return False


# A function to download the video thumbnail from YouTube (currently the only supported video platform):
def download_thumbnail(video_id_from_shortcode, pelican_output_path):
    # Check if the thumbnail directory exists already:
    check_for_thumbnail_directory(pelican_output_path)
    
    # Check if the thumbnail for this video exists already (if it's been previously downloaded). If it doesn't, download it:
    if not os.path.exists(pelican_output_path + "/" + output_directory_for_thumbnails + "/" + video_id_from_shortcode + ".jpg"): # If the thumbnail doesn't already exist...
        urllib.urlretrieve("https://img.youtube.com/vi/" + video_id_from_shortcode + "/0.jpg", pelican_output_path + "/" + output_directory_for_thumbnails + "/" + video_id_from_shortcode + ".jpg") # Download the thumbnail. This follows the instructions at http://www.reelseo.com/youtube-thumbnail-image/ for downloading YouTube thumbnail images.


# A function to read through each page and post as it comes through from Pelican, find all instances of `!youtube(...)`, and change it into an HTML <img> element with the video thumbnail.
def process_youtube_shortcodes(data_passed_from_pelican):
    if data_passed_from_pelican._content: # If the item passed from Pelican has a "content" attribute (i.e., if it's not an image file or something else like that). NOTE: data_passed_from_pelican.content (without an underscore in front of 'content') seems to be read-only, whereas data_passed_from_pelican._content is able to be overwritten. This is somewhat explained in an IRC log from 2013-02-03 from user alexis to user webdesignhero_ at https://botbot.me/freenode/pelican/2013-02-01/?tz=America/Los_Angeles.
        full_content_of_page_or_post = data_passed_from_pelican._content
    else:
        return # Exit the function, essentially passing over the (non-text) file.

    all_instances_of_the_youtube_shortcode = re.findall('\!youtube.*?\)', full_content_of_page_or_post) # Use a regular expression to find every instance of '!youtube' followed by anything up to the first matching ')'.

    if(len(all_instances_of_the_youtube_shortcode) > 0): # If the article/page HAS any shortcodes, go on. Otherwise, don't (to do so would inadvertantly wipe out the output content for that article/page).
        replace_shortcode_in_text = "" # This just gives this an initial value before going into the loop below.

        # Go through each shortcode instance that we found above, and parse it:
        for youtube_shortcode_to_parse in all_instances_of_the_youtube_shortcode:

            video_id_from_shortcode = re.findall('(?<=youtube\().*?(?=\))', youtube_shortcode_to_parse)[0] # Get what's inside of the parentheses in '!youtube(...).'
            
            # print "Video ID is " + video_id_from_shortcode # Good for debugging purposes.
            
            # Use the Pelican pelicanconf.py settings:
            pelican_output_path = data_passed_from_pelican.settings['OUTPUT_PATH']
            pelican_site_url = data_passed_from_pelican.settings['SITEURL']

            # Download the video thumbnail if it's not already on the filesystem:            
            download_thumbnail(video_id_from_shortcode, pelican_output_path)

            # Replace '!youtube(...)' with '<img>...</img>'. Note that the <img> is given a class that the jQuery file mentioned at the top of this file will watch over. Any time an image with that class is clicked, the jQuery function will trigger and turn it into the full video embed.
            replace_shortcode_in_text = re.sub(r'\!youtube\(' + video_id_from_shortcode + '\)', r'<img class="youtube-embed-dummy-image" id="' + video_id_from_shortcode + '" src="' +  pelican_site_url + '/' + output_directory_for_thumbnails + '/' + video_id_from_shortcode + '.jpg" alt="Embedded Video - Click to view" title="Embedded Video - Click to view"></img>', full_content_of_page_or_post)

        # Replace the content of the page or post with our now-updated content (having gone through all instances of the !youtube() shortcode and updated them all, exiting the loop above.
        data_passed_from_pelican._content = replace_shortcode_in_text


# Make Pelican work (see http://docs.getpelican.com/en/3.3.0/plugins.html#how-to-create-plugins):
def register():
    signals.content_object_init.connect(process_youtube_shortcodes)
