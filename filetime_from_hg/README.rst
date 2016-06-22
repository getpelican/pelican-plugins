Use Mercurial commit to determine page date
===========================================

If your blog content is versioned via Mercurial, this plugin will set
articles' and pages' ``metadata['date']`` to correspond to that of the
hg commit.  This plugin depends on the ``hglib`` python package,
which can be installed via::

    sudo apt-get install python-hglib

or::

    pip install hglib

The date is determined via the following logic:

* if a file is not tracked by hg, or a file is added but never committed
    - metadata['date'] = filesystem time
    - metadata['modified'] = filesystem time
* if a file is tracked, but no changes in working directory
    - metadata['date'] = first commit time
    - metadata['modified'] = last commit time
* if a file is tracked, and has changes in working directory
    - metadata['date'] = first commit time
    - metadata['modified'] = filesystem time

When this module is enabled, ``date`` and ``modified`` will be determined
by hg status; no need to manually set in article/page metadata. And
operations like copy and move will not affect the generated results.

If you don't want a given article or page to use the hg time, set the
metadata to ``hgtime: off`` to disable it.

You can also set ``HG_FILETIME_FOLLOW`` to ``True`` in your settings to
make the plugin follow file renames — i.e., ensure the creation date matches
the original file creation date, not the date it was renamed.

Credits
=======

This plugin is based on filetime_from_git.
