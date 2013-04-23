Summary
===========

This plug-in:

- Adds a `style="width: ???px;"` attribute to any `<img>` tags in the content, by checking
the dimensions of the image file and adding the appropriate style="width: ???px;" to the `<img>` tag.
- Also finds any `div class="figures"` tags in the content, that contain images and adds the same style to them too.


Assuming that the image is 250px wide, it turns output like this:

	<div class="figure" style="width: 250px;">
	    <img style="width: 250px;" alt="map to buried treasure" src="/static/images/image.jpg" />
	    <p class="caption">
	        This is the caption of the figure.
	    </p>
	    <div class="legend">
	        Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
	        tempor incididunt ut labore et dolore magna aliqua.
	    </div>
	</div>

into output like this:

	<div class="figure" style="width: 250px;">
	    <img style="width: 250px;" alt="map to buried treasure" src="/static/images/image.jpg" />
	    <p class="caption">
	        This is the caption of the figure.
	    </p>
	    <div class="legend">
	        Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
	        tempor incididunt ut labore et dolore magna aliqua.
	    </div>
	</div>

