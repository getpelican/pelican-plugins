Summary
===========

This plug-in finds any `div class="figures"` tags in the output, finds the image contained inside each one,
then checks the dimensions of the image file and adds the appropriate style="width: ???px;" to both the img tag
and it's containing div.figure tag.


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

TODO: Currently only does the first figure, not all of them
