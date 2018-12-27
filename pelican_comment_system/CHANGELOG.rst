Change Log
==========

All notable changes to this project will be documented in this file.
This project adheres to `Semantic Versioning <http://semver.org/>`__.

1.4.0 - 2017-02-20
------------------

Added
~~~~~

-  add ``setup.py`` to allow posting plugin to PyPI `PR
   #862 <https://github.com/getpelican/pelican-plugins/pull/862>`__

1.3.0 - 2017-01-10
------------------

Added
~~~~~

-  add
   `blogger\_comment\_export.py <import/blogger_comment_export.py>`__
   script to export comments from Blogger XML export and `associated
   documentation <docs/import.md>`__ `PR
   #835 <https://github.com/getpelican/pelican-plugins/pull/835>`__

1.2.2 – 2016-12-19
------------------

Fixed
~~~~~

-  Correct jQuery expression in cancelReply method `PR
   #820 <https://github.com/getpelican/pelican-plugins/pull/820>`__

1.2.1 – 2016-09-22
------------------

Fixed
~~~~~

-  Add support for the autoreload mode of pelican `PR
   #782 <https://github.com/getpelican/pelican-plugins/pull/782>`__
   `Fixes
   pelican#1949 <https://github.com/getpelican/pelican/issues/1949>`__

1.2.0 – 2016-05-23
------------------

Fixed - Documentation
~~~~~~~~~~~~~~~~~~~~~

-  Correct template path `PR
   #713 <https://github.com/getpelican/pelican-plugins/pull/713>`__

Added - Documentation
~~~~~~~~~~~~~~~~~~~~~

-  Adds Quickstart guide + default theme `PR
   #686 <https://github.com/getpelican/pelican-plugins/pull/686>`__

Fixed
~~~~~

-  Fix mailto link: use '' instead of '' `PR
   #720 <https://github.com/getpelican/pelican-plugins/pull/720>`__
-  Fix comparison of offset-naive and offset-aware datetimes `PR
   #722 <https://github.com/getpelican/pelican-plugins/pull/722>`__

Added
~~~~~

-  Logs a warning if the parent of a comment can not be found `PR
   #715 <https://github.com/getpelican/pelican-plugins/pull/715>`__

1.1.0 – 2016-02-18
------------------

Fixed – Documentation
~~~~~~~~~~~~~~~~~~~~~

-  Updated old URLs `PR
   #677 <https://github.com/getpelican/pelican-plugins/pull/677>`__

Changed
~~~~~~~

-  Main logic runs a bit earlier (allows other plugins to access
   comments earlier) `PR
   #677 <https://github.com/getpelican/pelican-plugins/pull/677>`__
-  The writer to generate the feeds can now be exchanged (via a normal
   pelican writer plugin) `PR
   #677 <https://github.com/getpelican/pelican-plugins/pull/677>`__

1.0.1 – 2015-10-04
------------------

Fixed – Documentation
~~~~~~~~~~~~~~~~~~~~~

-  Add commas indicating tuple (``PELICAN_COMMENT_SYSTEM_AUTHORS``) `PR
   #579 <https://github.com/getpelican/pelican-plugins/pull/579>`__

1.0.0 – 2014-11-05
------------------

Added
~~~~~

-  Basic static comments
-  Atom Feeds
-  Replies to comments
-  Avatars and identicons

This change log uses `Keep a CHANGELOG <http://keepachangelog.com/>`__
as a template.
