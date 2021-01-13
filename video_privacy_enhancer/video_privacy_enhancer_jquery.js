$(document).ready(function() {
// NOTE WELL: This is wrapped in a `$(document).ready(function() {...})` function (i.e., a "Document Ready" function that starts a section that won't load until the rest of the document/page has loaded (i.e., is "ready")). HOWEVER, this makes it so that jQuery functions from different .js files here are not able to see and talk to functions within this Document Ready function. Within a Document Ready function, functions and variables lose global scope. See http://stackoverflow.com/a/6547906 for more information.
    
///////////////////////////
// SETTINGS
///////////////////////////

	// NOTE WELL: It's expected to use the code 'VIDEO_ID_GOES_HERE' in the URLs below where the video ID should go. This phrase will be replaced by the video id below.
	// NOTE WELL: The URLS below should have 'http://' or 'https://' in front of them:
	var dictionary_of_embed_urls_for_different_services = {
		"youtube" : 'https://www.youtube-nocookie.com/embed/VIDEO_ID_GOES_HERE',
		"vimeo" : 'https://player.vimeo.com/video/VIDEO_ID_GOES_HERE'
	};

///////////////////////////
// END OF SETTINGS
///////////////////////////


// Whenever a link for an image created with the video_privacy_enhancer plugin is clicked, transform it into a video embed:
$('body').on("click",'img.video-embed-dummy-image',function(event) // Whenever an image with the class "video-embed-dummy-image" is clicked...
	{
	    // '$(this)' below refers to the image that's been clicked. Before we go down into the function below, where the definition/scope of '$(this)' will change, we'll set it in a variable so that we can refer to it within the function below.
	    var image_that_was_clicked = $(this);
	    
	    var video_id = $(this).attr('id'); // This assumes that the img ID attribute is set to the (e.g., youtube, Vimeo, etc.) video id.
		var service_name = $(this).attr('embed-service'); // This assumes that the 'embed-service' attribute is set to a name (e.g., youtube, vimeo), and that that name is in the dictionary below.
		
		
		var src_for_this_video = dictionary_of_embed_urls_for_different_services[service_name].replace("VIDEO_ID_GOES_HERE", video_id);

        // Fade out the image, and replace it with the iframe embed code for the actual video:
	    $(this).fadeOut(250, function() {
	        image_that_was_clicked.replaceWith('<iframe class="embedded_privacy_video" src="' + src_for_this_video + '" frameborder="0" allowfullscreen></iframe>') // This will automatically show again.
			}); // End fadeOut.
	});


}) // End Document Ready wrapper.
