# Collate Content
*Author: Edward J. Stronge <ejstronge@gmail.com>*

Makes categories of content available to the template as lists through a
`collations` attribute. I primarily developed this to make it easier
to work with `Page` objects that contain category metadata.

## Installation

If you downloaded this module as part of the pelican-plugins repository, 
add it to your Pelican configuration as follows:

    PLUGIN_PATH = '/path/to/pelican-plugins'
    PLUGINS = ['pelican_collate_content', ]
    
Otherwise, you can import it into Python as a normal module if you place
this repository in your `$PYTHONPATH`.

## Usage

To display all content in the category `Software Development`, 
you could use the following block in a template. In the template, the category
will appear in lowercase with internal whitespace and '-' characters
converted to underscores:

    ```html
    <h1>Development blog</h1>
    <ul> 
    {% for a in collations.software_development_articles %}
        <li>a.date - a.title</li> 
    {% endfor %}
    </ul>
    
    <h1> Open source projects </h1>
    I'm an active contributor to the following projects:
    
    <ul>
    {% for p in software_development_pages %}
        <li> p.title - p.summary</li> 
    {% endfor %}
    </ul>
    ```

### Articles or pages with multiple categories

Multiple categories are supported out-of-the box. Categories may not
contain commas but otherwise work with no problem.

## Settings

To limit which categories and subcategories are collated, set the
`CATEGORIES_TO_COLLATE` option in your Pelican configuration file.

If this option is present and is a list, only categories present
in `CATEGORIES_TO_COLLATE` will be collated:

    CATEGORIES_TO_COLLATE = ['category-of-interest', 'another-cool-category']
