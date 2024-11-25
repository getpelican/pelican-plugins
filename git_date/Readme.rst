Date Metadata from GIT
----------------------

This plugin allows to use git timestamps as `date` metadata. This enables you to
avoid explicitly defining timestamps for each of your posts if your content is
stored in a git repository. 

This plugin will overwrite explicitly set `date` metadata.


Settings
========

You can set `GIT_TIME_LAST_MODIFIED` to `True` or `False` in your pelican
configuration (Default: False). When choosing `True`, timestamps of contents
will be computed from timestamps of the commit containing the *last
modification* of the file. When choosing `False`, timestamps of the *first
commit* containing the file will be used. 
