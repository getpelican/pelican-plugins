# Video Privacy Enhancer

This plugin is a conceptual port of the Electronic Frontier Foundation's (EFF's) [MyTube Drupal plugin](https://www.eff.org/pages/mytube-limit-privacy-risks-embedded-video "EFF blog post about the MyTube Plugin") to Pelican. **It increases user privacy by stopping Google's ability to place cookies on a user's system through an embedded YouTube video without that user explicitly opting-in to viewing the video (by clicking on it).** In the future, support will hopefully expand to include other video platforms.


## Copyright, Contact, and Acknowledgements

This plugin is copyright 2014 Jacob Levernier  
It is released under the GNU AFFERO GENERAL PUBLIC LICENSE Version 3 (as is the default for Pelican Plugins in the getpelican/pelican-plugins repository).

Although not required by the license, I would very much appreciate it if you placed a note in the "About" page of your website that you use this plugin, in order to raise user awareness of web tracking issues.

### To contact the author:

* jleverni at uoregon dot edu  
* http://AdUnumDatum.org  
* BitBucket: https://bitbucket.org/jlev_uo/  
* Github: https://github.com/publicus  

This is the first plugin that I've written for Pelican, and it was intended as a training project for learning Pelican as well as Python better. I would be very happy to hear constructive feedback on the plugin and for suggestions for making it more efficient and/or expandable. Also, I've heavily annotated all of the Python and jQuery code in order to make it easier to understand for others looking to learn more, like I was when I wrote the plugin.

### Acknowledgements

I'm grateful to [Jordi Burgos](http://jordiburgos.com/post/2014/first-pelican-plugin-readtime.html "Blog post on writing plugins for Pelican") and [Duncan Lock](http://duncanlock.net/blog/2013/10/18/how-i-upgraded-this-website-to-pelican-33/ "Another blog post on writing plugins for Pelican") for writing helpful introductory blog posts on writing Pelican plugins. Both of these posts helped to decrease the intimidation factor associated with learning a new system like Pelican.

I'm also grateful to the authors of the plugins in the pelican-plugins repo; being able to look over other plugins' authors' code helped me immensely in learning more about how Pelican's [signals](http://docs.getpelican.com/en/3.3.0/plugins.html#how-to-create-plugins "Pelican documentation on creating plugins") system works.


## Explanation and Rationale

YouTube videos that are embedded in a website are capable of placing a cookie (or using other tracking methods) on a visitor's computer even if that visitor does not play the movie. For certain sites that deal with political or other potentially sensitive topics, this automatic tracking could raise privacy concerns among users. Thus, this plugin fetches and stores, on your server, a copy of the thumbnail image of each embedded YouTube video on your website. It then displays that image instead of the video until the user "opts-in" to watching the video by clicking on the thumbnail (at which point the image is replaced by the youtube embed iframe).

This plugin allows the shortcode **`!youtube(video_id)`** (for example, `!youtube(2XID_W4neJo)` for the video available at [https://www.youtube.com/watch?v=2XID_W4neJo](https://www.youtube.com/watch?v=2XID_W4neJo)) to be used in any Pelican page or article. During the `make html` process, the plugin will find every instance of the shortcode, and for each instance, will automatically download the video's thumbnail from YouTube if it hasn't been downloaded previously, and will save the thumbnail to the Pelican output folder (by default, to /output/images/youtube-thumbnails). It will then replace the shortcode with the thumbnail image. A jQuery script then watches for thumbnail image clicks; when a user clicks a thumbnail image, the jQuery script will fade the image out, and replace it with the actual youtube video iframe.

YouTube does have a ["privacy-enhanced mode"](https://support.google.com/youtube/answer/171780?expand=PrivacyEnhancedMode#privacy) that purports not to place cookies on a user's page until the user clicks on a video. However, if you are a website author who wants to *ensure* that no cookies are initially placed, this plugin puts that power in your hands.


## Usage

`!youtube(2XID_W4neJo)` written anywhere in the content of a page or post will become `<img class="youtube-embed-dummy-image" id="2XID_W4neJo" src="YOUR_SITEURL/images/youtube-thumbnails/2XID_W4neJo.jpg" alt="Embedded Video - Click to view" title="Embedded Video - Click to view"></img>` during the `make html` process ('YOUR_SITEURL' is replaced by your actual `SITEURL` from pelicanconf.py). The plugin will take care of downloading `2XID_W4neJo.jpg`.

The plugin comes with an example jQuery file to copy into your theme's static folder. **With this jQuery script, anytime a thumbnail image is clicked by a user, the thumbnail will fade out and then be replaced by the actual video embed.** Thus, the `<img>...</img>` code above will become `<iframe width="853" height="480" src="//www.youtube-nocookie.com/embed/2XID_W4neJo" frameborder="0" allowfullscreen></iframe>` when clicked.

To set the plugin up, just read the instructions at the top of youtube_privacy_enhancer.py. That file also includes some example CSS to copy into your theme's CSS file, as well as a setting or two for you to look over.


## To Do

As noted in an EFF [blog post](https://www.eff.org/deeplinks/2010/08/upgrade-mytube "EFF blog post about updates to MyTube"), the Drupal MyTube plugin from which this plugin takes its idea is capable of handling videos not only from YouTube, but also from Vimeo, Comedy Central, and other sites. It would be nice to expand this Pelican plugin in the future to do the same. In addition, the code could likely be refactored to make extending the plugin easier.
