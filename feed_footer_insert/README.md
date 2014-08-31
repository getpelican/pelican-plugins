# Feed Footer Insert

This plugin allows you to insert a `FEED_FOOTER_INSERT_HTML` to the end of the blog.


## Usage

Insert `FEED_FOOTER_INSERT_HTML` to your `pelicanconf.py`. You can use
title / url / author / authors / slug / category / summary
/ date infomation in the config like this: `%(title)s`.

eg.

```
FEED_FOOTER_INSERT_HTML = u"""
<hr>
<div class="panel">
<div class="panel-body">
   <small>原文链接: <a href="http://blog.log4d.com/%(url)s">http://blog.log4d.com/%(url)s</a></small><br>
   <small>3a1ff193cee606bd1e2ea554a16353ee</small>
</div>
</div>
"""
```
