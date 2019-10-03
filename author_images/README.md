# author_images

This Pelican plugin adds support for author images and avatars. You may choose
to display one or the other.

## Configuration

Add the directory to the base plugins directory to `PLUGIN_PATHS` in
`pelicanconf.py`, and then add `author_images` to the `PLUGINS` list. For example,

    PLUGIN_PATHS = ["../git/pelican-plugins"]
    PLUGINS = ['author_images']

You can also configure the directory for the author images and avatars. Note
that both of these directories should exist in your theme, inside the static
directory. This feels like the best way to approach this.

    AUTHOR_AVATARS = 'images/author_avatars'
    AUTHOR_IMAGES = 'images/author_images'

### Adding images

Now you can place images and avatars into the correct places. The location for
these is `THEME / THEME_STATIC_DIR / AUTHOR_AVATARS`. For instance,
`strudel/static/images/author_avatars` for my particular setup. Note that in
this case, `strudel` is my theme.

### Naming images

Images have to named correctly for the plugin to find them. Currently, this
means you need to take a `sha256` of the authors name. The extension of
the file can be one of `svg`, `jpg`, `jpeg` or `png`. For instance, my name is
William Pettersson, so I can run

    python -c 'import hashlib; print(hashlib.sha256("William Pettersson".encode("UTF-8")).hexdigest())'

to get the hash sum of my name. Then I just rename my images or avatars to have
that name, but with the appropriate extension. For simplicity, there is a
`generate_hashsum.py` which can also be used as follows

    python generate_hashsum.py "William Pettersson"

which prints out
`a40249517dfaf4e83264ced7d802c9fe9b811c8425b1ce1b3e8b9e236b52fa3e`. This means
my files have to be named
`a40249517dfaf4e83264ced7d802c9fe9b811c8425b1ce1b3e8b9e236b52fa3e.png`, or
`a40249517dfaf4e83264ced7d802c9fe9b811c8425b1ce1b3e8b9e236b52fa3e.jpg` or
similar.


### Using in themes

These images and avatars are made available to themes through the
`author.avatar` and `author.image` variables.

