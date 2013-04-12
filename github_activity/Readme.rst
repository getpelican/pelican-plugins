GitHub activity
---------------

This plugin makes use of the `feedparser`_ library that you'll need to
install.

Set the ``GITHUB_ACTIVITY_FEED`` parameter to your GitHub activity feed.
For example, to track Pelican project activity, the setting would be::

     GITHUB_ACTIVITY_FEED = 'https://github.com/getpelican.atom'

On the template side, you just have to iterate over the ``github_activity``
variable, as in this example::

     {% if GITHUB_ACTIVITY_FEED %}
        <div class="social">
                <h2>Github Activity</h2>
                <ul>

                {% for entry in github_activity %}
                    <li><b>{{ entry[0] }}</b><br /> {{ entry[1] }}</li>
                {% endfor %}
                </ul>
        </div><!-- /.github_activity -->
     {% endif %}

``github_activity`` is a list of lists. The first element is the title,
and the second element is the raw HTML from GitHub.

.. _feedparser: https://crate.io/packages/feedparser/
