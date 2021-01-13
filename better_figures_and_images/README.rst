Requirements
------------

* pip install pillow beautifulsoup4 pysvg-py3

Summary
=======

This plug-in:

- Adds a ``style="width: ???px; height: auto;"`` attribute to any ``<img>`` tags in the content, by checking the dimensions of the image file and adding the appropriate ``style="width: ???px; height: auto;"`` to the ``<img>`` tag.

- Also finds any ``div class="figures"`` tags in the content, that contain images and adds the same style to them too.

- If ``RESPONSIVE_IMAGES`` setting is true, it adds ``style="width: ???px; max-width: 100%; height: auto;"`` instead.

- Corrects Alt text: If an img ``alt`` attribute equals the image filename, it sets it to ""


Assuming that the image is 250px wide, it turns this::

  <div class="figure">
    <img alt="/static/images/image.jpg" src="/static/images/image.jpg" />
    <p class="caption">
      This is the caption of the figure.
    </p>
    <div class="legend">
      Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod 	        tempor incididunt ut labore et dolore magna aliqua.
    </div>
  </div>

into this::

  <div class="figure" style="width: 250px; height: auto;">
    <img style="width: 250px; height: auto;" alt="" src="/static/images/image.jpg" />
    <p class="caption">
      This is the caption of the figure.
    </p>
    <div class="legend">
      Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    </div>
  </div>

or this, if ``RESPONSIVE_IMAGES = True``::

  <div class="figure" style="width: 250px; max-width: 100%; height: auto;">
    <img style="width: 250px; max-width: 100%; height: auto;" alt="" src="/static/images/image.jpg" />
    <p class="caption">
      This is the caption of the figure.
    </p>
    <div class="legend">
      Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    </div>
  </div>
