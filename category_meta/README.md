Category Metadata
-----------------

A plugin to read metadata for each category from an index file in that
category's directory.

For this plugin to work properly, your articles should not have a
Category: tag in their metadata; instead, they should be stored in
(subdirectories of) per-category directories.  Each per-category
directory must have a file named 'index.ext' at its top level, where
.ext is any extension that will be picked up by an article reader.
The metadata of that article becomes the metadata for the category,
copied over verbatim, with three special cases:

 * The category's name is set to the article's title.
 * The category's slug is set to the name of the parent directory
   of the index.ext file.
 * The _text_ of the article is stored as category.description.

You can use this, for example, to control the slug used for each
category independently of its name, or to add a description at the top
of each category page.
