# Org Emacs Reader

Publish Emacs Org files alongside the rest of your website or blog.

- `ORG_READER_EMACS_LOCATION`: Required. Location of Emacs binary.
  If you use `Emacs for Mac OS X`,
  the location should be `/Applications/Emacs.app/Contents/MacOS/Emacs`,
  rather than `/usr/bin/emacs`.

- `ORG_READER_EMACS_SETTINGS`: Optional. An absolute path to an Elisp file, to
  run per invocation. Useful for initializing the `package` Emacs library if
  that's where your Org mode comes from, or any modifications to Org Export-
  related variables. If you want to use your standard emacs init file, you
  can ignore this variable.

- `ORG_READER_BACKEND`: Optional. A custom backend to provide to Org. Defaults
  to `'html`.

To provide metadata to Pelican, the following properties can be defined in
the org file's header:

    #+TITLE: The Title Of This BlogPost
    #+DATE: 2001-01-01
    #+CATEGORY: blog-category
    #+AUTHOR: My Name
    #+PROPERTY: LANGUAGE en
    #+PROPERTY: SUMMARY hello, this is the description
    #+PROPERTY: STATUS disable or enable document
    #+PROPERTY: SLUG test_slug
    #+PROPERTY: MODIFIED [2015-12-29 Di]
    #+PROPERTY: TAGS my, first, tags
    #+PROPERTY: SAVE_AS alternative_filename.html


- The `TITLE` is the only mandatory header property
- Timestamps (`DATE` and `MODIFIED`) are optional and can be either a string
  of `%Y-%m-%d` or an org timestamp
- The property names (`SUMMARY`, `SLUG`, `MODIFIED`, `TAGS`, `SAVE_AS`) can
  be either lower-case or upper-case
- The slug is automatically the filename of the Org file, if not explicitly
  specified
- It is not possible to pass an empty property to Pelican.  For this plugin,
  it makes no difference if a property is present in the Org file and left
  empty, or if it is not defined at all.
