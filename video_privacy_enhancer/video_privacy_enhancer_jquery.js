$(document).ready(function() {
// NOTE WELL: This is wrapped in a `$(document).ready(function() {...})` function (i.e., a "Document Ready" function that starts a section that won't load until the rest of the document/page has loaded (i.e., is "ready")). HOWEVER, this makes it so that jQuery functions from different .js files here are not able to see and talk to functions within this Document Ready function. Within a Document Ready function, functions and variables lose global scope. See http://stackoverflow.com/a/6547906 for more information.
    
// Whenever a link for an image created with the video_privacy_enhancer plugin is clicked, transform it into a video embed:
$('body').on("click",'img.youtube-embed-dummy-image',function(event) // Whenever an image with the class "youtube-embed-dummy-image" is clicked...
	{
	    // '$(this)' below refers to the image that's been clicked. Before we go down into the function below, where the definition/scope of '$(this)' will change, we'll set it in a variable so that we can refer to it within the function below.
	    var image_that_was_clicked = $(this);
	    
	    var youtube_video_id = $(this).attr('id'); // This assumes that the img ID attribute is set to the youtube video id.

        // Fade out the image, and replace it with the iframe embed code for the actual YouTube video:
	    $(this).fadeOut(250, function() {
	        image_that_was_clicked.replaceWith('<iframe class="embedded_youtube_video" src="//www.youtube-nocookie.com/embed/' + youtube_video_id + '" frameborder="0" allowfullscreen></iframe>') // This will automatically show again.
			}); // End fadeOut.
	});


}) // End Document Ready wrapper.
