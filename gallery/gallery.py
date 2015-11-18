import os
from pelican import signals


def get_content_path(pelican):
    return pelican.settings.get('PATH')


def get_gallery_path(pelican):
    gallery_path = pelican.settings.get('GALLERY_PATH', 'images/gallery')
    content_path = get_content_path(pelican)

    return os.path.join(content_path, gallery_path)


def add_gallery_post(generator):
    gallerycontentpath = get_gallery_path(generator)

    for article in generator.articles:
        if 'gallery' in article.metadata.keys():
            album = article.metadata.get('gallery')
            galleryimages = []

            articlegallerypath=os.path.join(gallerycontentpath, album)

            if(os.path.isdir(articlegallerypath)):
                for i in os.listdir(articlegallerypath):
                    if not i.startswith('.') and os.path.isfile(os.path.join(os.path.join(gallerycontentpath, album), i)):
                        galleryimages.append(i)

            article.album = album
            article.galleryimages = sorted(galleryimages)


def add_gallery_page(generator):
    gallerycontentpath = get_gallery_path(generator)

    for page in generator.pages:
        if 'gallery' in page.metadata.keys():
            album = page.metadata.get('gallery')
            galleryimages = []

            pagegallerypath=os.path.join(gallerycontentpath, album)

            if(os.path.isdir(pagegallerypath)):
                for i in os.listdir(pagegallerypath):
                    if not i.startswith('.') and os.path.isfile(os.path.join(os.path.join(gallerycontentpath, album), i)):
                        galleryimages.append(i)

            page.album = album
            page.galleryimages = sorted(galleryimages)


def generate_gallery_page(generator):
    gallerycontentpath = get_gallery_path(generator)

    for page in generator.pages:
        if page.metadata.get('template') == 'gallery':
            gallery = dict()

            for a in os.listdir(gallerycontentpath):
                if not a.startswith('.') and os.path.isdir(os.path.join(gallerycontentpath, a)):

                    for i in os.listdir(os.path.join(gallerycontentpath, a)):
                        if not a.startswith('.') and os.path.isfile(os.path.join(os.path.join(gallerycontentpath, a), i)):
                            gallery.setdefault(a, []).append(i)
                    gallery[a].sort()

            page.gallery=gallery


def register():
    signals.article_generator_finalized.connect(add_gallery_post)
    signals.page_generator_finalized.connect(generate_gallery_page)
    signals.page_generator_finalized.connect(add_gallery_page)
