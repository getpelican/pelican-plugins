#Subcategory Plugin#

Adds support for subcategories in addition to article categories.

Subcategories are heirachial. Each subcategory has a parent, which is either a
regular category or another subcategory. Subcategories with the same name but 
different parents are not the same. Their articles won't be grouped together 
under that name.

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
            <a href="{{ SITEURL }}/{{ arcticle.categor.url }}">{{ article.category}}</a>
        </li>
    {% for subcategory in article.subcategories %}
        <li>
            <a href="{{ SITEURL }}/{{ category.url }}>{{ subcategory }}</a>
        </li>
    {% endfor %}
    </ol>
    </nav>
 

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
