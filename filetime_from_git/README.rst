Use git commit to determine page date
======================================

If the blog content is managed by git repo, this plugin will set articles'
and pages' ``metadata['date']`` according to git commit. This plugin depends
on python package ``gitpython``, install::

    pip install gitpython

The determine logic will works so:

* if a file is not tracked by git, or a file is staged but never commited
    - metadata['date'] = fs time
    - metadata['updated'] = fs time
* if a file is tracked, but no changes in stage area or work dir
    - metadata['date'] = first commit time
    - metadata['updated'] = last commit time
* if a file is tracked, and has changes in stage area or work dir
    - metadata['date'] = first commit time
    - metadata['updated'] = fs time

When this module is enabled, ``date`` and ``updated`` will be set automatically
by git status, no need to manually set in article/page's metadata. And
operations like copy, move will not affect the generated results.

If some article or page doesn't like to use git time, set a ``gittime: off``
metadata to disable it.

You can also set GIT_FILETIME_FOLLOW to True in your pelican config to 
make the plugin follow file renames i.e. ensure the creation date matches
the original file creation date, not the date is was renamed.

FAQ
---

### Q. I get a GitCommandError: 'git rev-list ...' when I run the plugin. What's up?
Be sure to use the correct gitpython module for your distros git binary.
Using the GIT_FILETIME_FOLLOW option to True may also make your problem go away as it uses
a different method to find commits.

Some notes on git
~~~~~~~~~~~~~~~~~~

* How to check if a file is managed?

.. code-block:: sh

   git ls-files $file --error-unmatch

* How to check if a file has changes?

.. code-block:: sh

   git diff $file            # compare staged area with working directory
   git diff --cached $file   # compare HEAD with staged area
   git diff HEAD $file       # compare HEAD with working directory

* How to get commits related to a file?

.. code-block:: sh

   git status $file

with ``gitpython`` package, it's easier to parse commited time:

.. code-block:: python

   repo = Git.repo('/path/to/repo')
   commits = repo.commits(path='path/to/file')
   commits[-1].committed_date    # oldest commit time
   commits[0].committed_date     # latest commit time
