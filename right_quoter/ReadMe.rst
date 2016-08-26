Right Quoter
------------

When used with the ``TYPOGRIFY`` setting, this plugin attempts to fix
the direction of the curly single quote for contractions with leading
apostrophes, e.g. two-digit decade or year references like '90s or '78.

Examples:

::

    &#8216;00s               --> &#8217;00s
    &#8216;87                --> &#8217;87
    Get &#8216;em!           --> Get &#8217;em!
    &#8216;Tis but a scratch --> &#8217;Tis but a scratch

| ‘00s → ’00s
| ‘87 → ’87
| Get ‘em! → Get ’em!
| ‘Tis but a scratch. → ’Tis but a scratch.

By piggybacking on the expected behavior of ``typogrify`` (which uses
``smartypants`` for the curlying), it should respect the same ignored
tags as ``typogrify``. (And only have an effect if ``typogrify`` is
enabled.)

It also handles wrapping spans that may be applied during processing
before the plugin is able to act on the content, e.g.:

::

    <span class="quo">&#8217;</span>Tis
    &#8217;<span class="caps">TWAS</span>
    <span class="quo">&#8217;</span><span class="caps">TIS</span>

Unfortunately it will also "fix" situations like this:

| ‘98’ → ’98’
| ‘98 things’ → ’98 things’

Which is a challenge for another day.
