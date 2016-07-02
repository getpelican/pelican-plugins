# Better Figures and Images

## Summary

This plug-in:

-   Adds a `style="max-width: 100%; height: auto;"` attribute to any `<img>` tags in the content.
-   Also finds any `<figure>` tags in the content, that contain images and adds the same style to them too.
-   If `BETTER_FIGURES_BOOTSTRAP` setting is true, it adds `img-fluid` to the class attribute of img tags and `figure` into the figure class attribute.
-   Corrects Alt text: If an img `alt` attribute ends in `.gif`, `.jpg`, `.jpeg`, `.tiff`, or `.png`, it sets it to ""

## Important Version Change Notes

This version does not require pillow. It does not check the size of the photo and it will not insert the size of the photo into the style attribute. The benefit of this change is that this plugin will now work with the photos plugin.

## Requirements

`pip install beautifulsoup4`

## Usage

Turning on the plugin will add responsive class or style attributes to all figure and image tags.

It turns this:

```HTML5
  <figure>
    <img alt="/static/images/image.jpg" src="/static/images/image.jpg" />
    <figcaption> This is the caption of the figure. </figcaption>
  </figure>
```

into this:

```HTML5
<figure style="max-width: 100%; height: auto;">
  <img alt="/static/images/image.jpg" src="/static/images/image.jpg" style="max-width: 100%; height: auto;">
  <figcaption class="figure-caption"> This is the caption of the figure. </figcaption>
</figure>
```

or this, if `BETTER_FIGURES_BOOTSTRAP = True`:

```HTML5
<figure class="figure">
  <img alt="/static/images/image.jpg" class="img-fluid figure-img" src="/static/images/image.jpg" />
  <figcaption class="figure-caption text-center"> This is the caption of the figure. </figcaption>
</figure>
```

## Markdown Attribute Enhancement

White ReStructureText always allowed you to add attributes to your img tags Markdown does not. This version of the Better Figures and Images plugin allows you to add attributes to image elements. To use this feature you can add embedded JSON containing the attributes you would like to add. Note: you must surround the JSON with `` ` ``. This is to ensure that all list elements in the JSON are escaped within the markdown

It will now turn this:

```markdown
![Test Photo `{"caption": "This is a test caption", "class":["float-right"]}`]({photo}testgallery/IMG_0264.png)
```

Into this:

```HTML5
<img alt="Test Photo" caption="This is a test caption" class="img-fluid float-right" src="http://ninetenlevins.com/photos/testgallery/img_0264a.jpg"/>
```

As Markdown has no figure syntax, this plugin has a magic JSON element that will turn the Markdown img syntax into a figure. Adding a `"type": "figure"` will convert the img tag into a fully fledged figure tag. It will also add a caption and set it to the caption value if one is set or the alt value if one is not.

It will now turn this:

```markdown
![Test Photo `{"type": "figure", "caption": "This is a test caption", "class":["float-right"]}`]({photo}testgallery/IMG_0264.png)
```

Into this:

```HTML5
<figure class="figure">
 <img alt="Test Photo" caption="This is a test caption" class="img-fluid float-right figure-img" src="http://ninetenlevins.com/photos/testgallery/img_0264a.jpg"/>
 <figcaption class="figure-caption text-center">
  This is a test caption
 </figcaption>
</figure>
```
