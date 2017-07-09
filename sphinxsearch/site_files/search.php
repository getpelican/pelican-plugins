/*
This file is part of Shinxsearch for Pelican

Copyright (C) 2017 Ysard

Shinxsearch for Pelican is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

Shinxsearch for Pelican is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with Shinxsearch for Pelican.  If not, see <http://www.gnu.org/licenses/>.
*/
<?php
    //Sanitize the input
    if (isset($_GET['q']) AND !empty($_GET['q'])) {

        $q = htmlspecialchars((string)$_GET['q']);

        // Support of booleans operators
        // NOT is preceed by OR or AND or nothing
        // => no space before it (people don't send 2 spaces but only 1 after OR or AND)
        $booleans = array(' OR ', ' or ', ' AND ', ' and ', 'NOT ', 'not ');
        $bool_ops = array(' | ', ' | ', ' && ', ' && ', '! ', '! ');
        $q = str_replace($booleans, $bool_ops, $q);

        $sphinx = new SphinxClient;
        $sphinx->setServer('localhost', 9312);
        $sphinx->setSortMode(SPH_SORT_RELEVANCE);
        // enable extended query syntax where you could combine "AND", "OR", "NOT" operators
        // http://sphinxsearch.com/docs/current.html#extended-syntax
        $sphinx->setMatchMode(SPH_MATCH_EXTENDED2);
        $sphinx->setConnectTimeout(2);

        // Returns FALSE on failure.
        // Query on 'my_blog' index
        $found = $sphinx->query($q, 'my_blog');

        //var_dump($q);
        //echo '<pre>', print_r($found, true), '</pre>';
    }
/*
Array
(
    [error] =>
    [warning] =>
    [status] => 0
    [fields] => Array
        (
            [0] => content
            [1] => title
        )

    [attrs] => Array
        (
            [published] => 2
            [category] => 1073741825
            [title] => 7
            [author] => 7
            [url] => 7
            [summary] => 7
            [slug] => 7
        )

    [matches] => Array
        (
            [637352186] => Array
                (
                    [weight] => 1678
                    [attrs] => Array
                        (
                            [published] => 1482102000
                            [category] => Array
                                (
                                )

                            [title] => mock title
                            [author] => mock user
                            [url] => /mock.html
                            [summary] => mock summary.
                            [slug] => mock_slug
                        )

                )

                [total] => 2
    [total_found] => 2
    [time] => 0
    [words] => Array
        (
            [mock] => Array
                (
                    [docs] => 2
                    [hits] => 2
                )
        )
)
*/
?>
{% extends "base.html" %}
{% block content_title %}{% endblock %}
{% block content %}
<h2 itemprop="name headline"><?php echo 'Results for "' . htmlspecialchars((string)$_GET['q']) . '":'; ?></h2>

<?php
if (isset($found) AND $found !== FALSE AND $found['status'] == 0) {

    if ($found['total_found'] != 0) {

        foreach ($found['matches'] as &$document) {

            //echo '<p>' . $document['attrs']['title'] . "<br>" . $document['attrs']['summary'] . "</p>";
            // Get date from timestamp
            $date = new DateTime();
            $date->setTimestamp($document['attrs']['published']);

            ?>

            <div class="article" itemscope itemtype="http://schema.org/BlogPosting">
                <a href="{{ SITEURL }}/<?php echo $document['attrs']['slug']; ?>.html">
                    <h3 itemprop="name headline"><?php echo $document['attrs']['title']; ?></h3>
                </a>
                <time datetime="<?php echo $date->format('c'); ?>" itemprop="datePublished"><?php echo $date->format('D. j M Y'); ?></time>
                &nbsp;—&nbsp;
                <span itemprop="author" itemscope="" itemtype="http://schema.org/Person">
                    <span itemprop="name"><?php echo $document['attrs']['author']; ?></span>
                </span>
                <div class="summary"><?php echo $document['attrs']['summary']; ?></div>
            </div>

            <?php
        }
        // Destruct ref on last element
        unset($document);

        // if !empty results
        echo '</div><div class="col-md-8 col-md-offset-2">';
        echo '<p>' . $found['total_found'] . ' article(s) found in ' . $found['time'] .'s.</p></div>';

    } else {
        // No results
        echo '</div><div class="col-md-8 col-md-offset-2">';
        echo '<p>There are no results for your query.</p></div>';

    }

} elseif (isset($found) AND !$found) {
    // Shinxsearch error
    echo '</div><div class="col-md-8 col-md-offset-2">';
    echo '<p>Error: ' . $sphinx->getLastError() . '.</p></div>';

} else {
    // Bad/no parameters
    echo '</div><div class="col-md-8 col-md-offset-2">';
    echo '<p>Did you forget the query?</p></div>';

}
?>
{% endblock content %}
