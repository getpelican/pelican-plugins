"""A function for each service to download the video thumbnail

Each function should accept one argument (the video id from that service) and should return the download URL for the video's thumbnail.

"""

"""
LIBRARIES
"""

# from urllib.request import urlopen # For downloading the video thumbnails. Not as clean as, e.g., the requests module, but installed by default in many Python distributions.
from six.moves.urllib.request import urlopen

import json

"""
END OF LIBRARIES
"""

def generate_thumbnail_download_link_youtube(video_id_from_shortcode):
	"""Thumbnail URL generator for YouTube videos."""
	
	thumbnail_download_link="https://img.youtube.com/vi/" + video_id_from_shortcode + "/0.jpg"
	return thumbnail_download_link

def generate_thumbnail_download_link_vimeo(video_id_from_shortcode):
	"""Thumbnail URL generator for Vimeo videos."""
	
	# Following the Vimeo API at https://developer.vimeo.com/api#video-request, we need to request the video's metadata and get the thumbnail from that. First, then, we'll get the metadata in JSON format, and then will parse it to find the thumbnail URL.
	video_metadata = urlopen("https://vimeo.com/api/v2/video/" + str(video_id_from_shortcode) + ".json").read() # Download the video's metadata in JSON format.
	video_metadata_parsed = json.loads(video_metadata.decode('utf-8')) # Parse the JSON
	video_thumbnail_large_location = video_metadata_parsed[0]['thumbnail_large'] # Go into the JSON and get the URL of the thumbnail.
	return video_thumbnail_large_location	
