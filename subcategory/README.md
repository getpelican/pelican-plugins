#Subcategory Plugin#

Adds support for subcategories in addition to article categories.

Subcategories are heirachial. Each subcategory has a parent, which is either a
regular category or another subcategory.

Feeds can be generated for each subcategory just like categories and tags.


##Usage##

Subcategories are an extension to categories. Add subcategories to an article's
category metadata using a `/` like this:

    Category: Regular Category/Sub-Category/Sub-Sub-category

then create a `subcategory.html` template in your theme similar to the 
`category.html` or `tag.html`

In your templates `article.category` continues to act the same way. Your 
subcategories are stored in a list `aricles.subcategories`. To create a 
breadcrumb style navigation you might try something like this:

    <nav class="breadcrumb">
    <ol>
        <li>
            <a href="{{ SITEURL }}/{{ arcticle.category.url }}">{{ article.category}}</a>
        </li>
    {% for subcategory in article.subcategories %}
        <li>
            <a href="{{ SITEURL }}/{{ subcategory.url }}>{{ subcategory.shortname }}</a>
        </li>
    {% endfor %}
    </ol>
    </nav>
 
##Subcategory Names##
Each subcategory's name is a `/` seperated list of it parents and itself.
This is neccesary to keep each subcategory unique. It means you can have 
`Category 1/Foo` and `Category 2/Foo` and the won't intefere with each other. 
Each subcategory has an attribute `shortname` which is just the name without 
it's parents associated. For example if you had
    
    Category/Sub Category1/Sub Category2

the name for Sub Category 2 would be `Category/Sub Category1/Sub Category2` and
the shortname would be `Sub Category2`

If you need to use the slug, it is generated from the short name, not the full
name.


##Settings##

Consistent with the default settings for Tags and Categories, the default 
settings for subcategoris are:
    
    'SUBCATEGORY_SAVE_AS' = os.path.join('subcategory', '{savepath}.html')
    'SUBCATEGORY_URL' = 'subcategory/(fullurl).html'

`savepath` and `fullurl` are generated recursively, using slugs. So the full
url would be:
    
    category-slug/sub-category-slug/sub-sub-category-slug

with `savepath` being similar but joined using `os.path.join`

Similarily you can save a subcategory feeds by adding one of the following 
to your pelicanconf file

    SUBCATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'
    SUBCATEGORY_FEED_RSS = 'feeds/%s.rss.xml'

and this will create a feed with `fullurl` of the subcategory. Eg.
    
    feeds/category/subcategory.atom.xml
