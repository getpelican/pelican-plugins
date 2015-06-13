Pelican ``gist_directive`` plugin
=================================

This plugin adds a ``gist`` reStructuredText directive. Eg::

   .. gist:: ionelmc/eb11afbcca187bad5273 setup.py python
   
It will download (with cache) and include the gist contents in the document.

.. note::

    It also supports embedding content from github directly.
    
    Example, to include ``https://raw.githubusercontent.com/ionelmc/cookiecutter-pylibrary/master/%7B%7Bcookiecutter.repo_name%7D%7D/setup.py``::
    
        .. github:: ionelmc/cookiecutter-pylibrary master/{{cookiecutter.repo_name}}/setup.py
    
    