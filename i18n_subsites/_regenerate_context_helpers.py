
import math
import random
from collections import defaultdict
from operator import attrgetter, itemgetter


def regenerate_context_articles(generator):
    """Helper to regenerate context after modifying articles draft state

    essentially just a copy from pelican.generators.ArticlesGenerator.generate_context
    after process_translations up to signal sending

    This has to be kept in sync untill a better solution is found
    This is for Pelican version 3.3.0
    """
    # Simulate __init__ for fields that need it
    generator.dates = {}
    generator.tags = defaultdict(list)
    generator.categories = defaultdict(list)
    generator.authors = defaultdict(list)
    

    # Simulate ArticlesGenerator.generate_context 
    for article in generator.articles:
        # only main articles are listed in categories and tags
        # not translations
        generator.categories[article.category].append(article)
        if hasattr(article, 'tags'):
            for tag in article.tags:
                generator.tags[tag].append(article)
        # ignore blank authors as well as undefined
        if hasattr(article, 'author') and article.author.name != '':
            generator.authors[article.author].append(article)


    # sort the articles by date
    generator.articles.sort(key=attrgetter('date'), reverse=True)
    generator.dates = list(generator.articles)
    generator.dates.sort(key=attrgetter('date'),
            reverse=generator.context['NEWEST_FIRST_ARCHIVES'])

    # create tag cloud
    tag_cloud = defaultdict(int)
    for article in generator.articles:
        for tag in getattr(article, 'tags', []):
            tag_cloud[tag] += 1

    tag_cloud = sorted(tag_cloud.items(), key=itemgetter(1), reverse=True)
    tag_cloud = tag_cloud[:generator.settings.get('TAG_CLOUD_MAX_ITEMS')]

    tags = list(map(itemgetter(1), tag_cloud))
    if tags:
        max_count = max(tags)
    steps = generator.settings.get('TAG_CLOUD_STEPS')

    # calculate word sizes
    generator.tag_cloud = [
        (
            tag,
            int(math.floor(steps - (steps - 1) * math.log(count)
                / (math.log(max_count)or 1)))
        )
        for tag, count in tag_cloud
    ]
    # put words in chaos
    random.shuffle(generator.tag_cloud)

    # and generate the output :)

    # order the categories per name
    generator.categories = list(generator.categories.items())
    generator.categories.sort(
            reverse=generator.settings['REVERSE_CATEGORY_ORDER'])

    generator.authors = list(generator.authors.items())
    generator.authors.sort()

    generator._update_context(('articles', 'dates', 'tags', 'categories',
                          'tag_cloud', 'authors', 'related_posts'))
    
