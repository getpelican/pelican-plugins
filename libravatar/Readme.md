# Libravatar plugin for Pelican

## Description

This plugin allows the inclusion of [Libravatar](http://www.libravatar.org)
user profile pictures, according to the email address of the article's
author.

## Usage

### Specifying the author's email address

The default email address is taken from the `LIBRAVATAR_AUTHOR_EMAIL`
variable in the Pelican configuration file.  This default value can be
overridden in a per-article basis, according to the email address found in
the article's metadata.

In ReSTructuredText:

```rst
:email: bart.simpson@example.com
```

In Markdown:

```markdown
Email: bart.simpson@example.com
```

If the avatar for the specified email address is not found at Libravatar,
it is searched at [Gravatar](http://www.gravatar.com).  If it is not found
there neither, a default picture is shown.  The default for the "missing
picture" can be defined in the configuration variable `LIBRAVATAR_MISSING`.

### Adjusting the template

This plugin assigns the `author_libravatar` variable to the Libravatar URL
and makes the variable available within the article's context.  For
instance, you can add the following to a template file (for example, to the
`article_infos.html` template file of the notmyidea theme), just before the
infomation about the author:

```html
{% if article.author_libravatar %}
<div align="center">
        <img src="{{ article.author_libravatar }}">
</div>
{% endif %}
```

## Settings

The following variables can be set in the Pelican configuration file:

- `LIBRAVATAR_AUTHOR_EMAIL`: site-wide default for the author's email address.

- `LIBRAVATAR_MISSING`: The default for the missing picture.  This can be
either a url (e.g. `'http://example.com/nobody.png'`) or the name of a
library of logos (e.g. `'wavatar'`; for the full set of alternativas, see
the [Libravatar API](https://wiki.libravatar.org/api/)).

- `LIBRAVATAR_SIZE`: The size, in pixels, of the profile picture (it is
always square, so the height is equal to the width).  If not specified, the
default size (80×80) is returned by Libravatar.

## Credits

Inspiration for this plugin came from the
[gravatar plugin](https://github.com/getpelican/pelican-plugins/tree/master/gravatar).

## Author

Copyright (C) 2015  Rafael Laboissiere (<rafael@laboissiere.net>)

Released under the GNU Affero Public License, version 3 or later.  No warranties.
