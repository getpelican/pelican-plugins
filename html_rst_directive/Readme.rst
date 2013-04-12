HTML tags for reStructuredText
------------------------------

This plugin allows you to use HTML tags from within reST documents. 


Directives
----------


::

    .. html::

        (HTML code)


Example
-------

A search engine::

    .. html::

       <form action="http://seeks.fr/search" method="GET">
         <input type="text" value="Pelican v2" title="Search" maxlength="2048" name="q" autocomplete="on" />
         <input type="hidden" name="lang" value="en" />
         <input type="submit" value="Seeks !" id="search_button" />
       </form>


A contact form::

    .. html::

        <form method="GET" action="mailto:some email">
          <p>
            <input type="text" placeholder="Subject" name="subject">
            <br />
            <textarea name="body" placeholder="Message">
            </textarea>
            <br />
            <input type="reset"><input type="submit">
          </p>
        </form>
