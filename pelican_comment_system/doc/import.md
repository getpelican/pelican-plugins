# Importing Comments

**Note**: Contributions to this section are welcomed!

When moving to Pelican and the Pelican Comment System, it may be desirable to move over your comments as well.

The scripts to support this are found in the `import` directory.

## Blogger

Blogger is good in that it will give you an export of everything, but the bad news is it's one giant XML file. XML is great if you're a computer, but a bit of a pain if you're a human. 

The code I used to export my comments from Blogger is found at [blogger_comment_export.py](../import/blogger_comment_export.py).

To use it
yourself, you will need to first adjust the constants at the beginning of the 
script (lines 26-33) to point to your Blogger XML export and where you want
the comments to be exported to. You will also need to install `untangle`
(available through pip -- `pip install untangle`).

Comments will be exported into folders matching
the Blogger slug of the post. The email for all authors will be `noreply@blogger.com`. The other file created will be `authors.txt`
which lists the various comment authors, and a link to the profile
picture used on Blogger. These pictures will need to be manually downloaded
and then configured using the `PELICAN_COMMENT_SYSTEM_AUTHORS` setting.
In my case, that looked like this:

```python
# in pelicanconf.py
PELICAN_COMMENT_SYSTEM_AUTHORS = {
    ('PROTIK KHAN', 'noreply@blogger.com'): "images/authors/rabiul_karim.webp",
    ('Matthew Hartzell', 'noreply@blogger.com'): "images/authors/matthew_hartzell.webp",
    ('Jens-Peter Labus', 'noreply@blogger.com'): "images/authors/jens-peter_labus.png",
    ('Bridget', 'noreply@blogger.com'): "images/authors/bridget.jpg",
    ('melissaclee', 'noreply@blogger.com'): "images/authors/melissa_lee.jpg",
    ('Melissa', 'noreply@blogger.com'): "images/authors/melissa_lee.jpg"
}
```

The script was developed for Python 3.6, but should work on Python 3.4+
without modification.

For more information on this script on, you can read my
[blog post](http://blog.minchin.ca/2016/12/blogger-comments-exported.html)
where I introduced it.

-- Wm. Minchin (@MinchinWeb), January 10, 2017
