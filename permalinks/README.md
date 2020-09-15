permalink
=========

This plugin enables a kind of permalink which can be used to refer to a piece
of content which is resistant to the file being moved or renamed.

It does this by creating additional output html in `PERMALINK_PATH`
(default permalinks/) which include redirect code to point user at original
page.

To work each page has to have an additional piece of metadata with the key
`permalink_id` (configurable with `PERMALINK_ID_METADATA_KEY`
which should remain static even through renames and should also
be unique on the site.

This can be generated automatically with the filetime_from_git module and
the `GIT_FILETIME_GENERATE_PERMALINK` option. 
This should always be used with `GIT_FILETIME_FOLLOW` to ensure this
persists across renames.


Hacky redirects
---------------
To make this work with things like github.io I'm forced to use HTML and
Javascript redirects rather than HTTP redirects which is obviously suboptimal.
