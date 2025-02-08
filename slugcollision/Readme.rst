Slug collisions avoidance for Pelican
-------------------------------------

:author: Leonardo http://github.com/leofiore

When {slug} is the only parameter used for ARTICLE_URL, this plugin
prevents that different articles generates the same slug, by adding
a numerical increment at the end.

For instance, if ``ARTICLE_URL`` is setted as something like
``/posts/{slug}`` a collision will occur when two or more articles will
have the same title. The common solution is to specify the slug inside
the article's body. This is not an automatic solution and could be
error-prone. Instead, this plugin checks for already defined slugs
and search for an automatic disambiguation
