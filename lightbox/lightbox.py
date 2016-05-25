"""
Lightbox
------------------------

This plugin:

- Enables automatic Lightbox for images
TODO: Need to add a test.py for this plugin.

"""
from pelican import signals
from bs4 import BeautifulSoup

def wrap_image_tags(p):
    """ Wrap image tags in links to add Lightbox support

    Any image tag in the content with class={LBPREFIX}-{SETNAME} will be
    wrapped with an anchored href with Lightbox support.  `LBPREFIX` is defined
    in the settings file as `LIGHTBOX_PREFIX` with a default of `'lb-'`.

    :param p: pelican instance
    :return: None
    """

    lbprefix = p.settings.get('LIGHTBOX_PREFIX', 'lb-')
    lbset = p.settings.get('LIGHTBOX_SET', 'images')

    if p._content is not None:
        content = p._content
        soup = BeautifulSoup(content)

        # Wrap each image tag in an anchor with a link.  Add the
        # attribute for the lightbox set to activate.
        if 'img' in content:
            for tag in soup('img'):

                # Skip if no class tag
                if not tag.has_attr('class'):
                    continue

                for c in tag['class']:
                    c.split(lbprefix)
                    substr = c.split(lbprefix,1)

                    # If the first element of the split is empty then the prefix
                    # is at the start of the string c.  We also must check that
                    # c is not empty.
                    if c and not substr[0]:
                        if substr[1]:
                            gallery = substr[1]
                        else:
                            gallery = lbgallery

                        link_wrapper = soup.new_tag("a", href=tag['src'])
                        link_wrapper['data-lightbox'] = substr[1] # We have to add data-lightbox seperately b/c it fails in the above as a seperate expression (- is a minus sign)

                        # Set the title (ie: lightbox caption) to the alt-text
                        if tag.has_attr('alt'):
                            link_wrapper['title'] = tag['alt']

                        # Set the title attribute as a caption, if the image is
                        # wrapped in a figure
                        fig = tag.find_parent('div', 'figure')
                        if fig:
                            caption = fig.findChild('p', 'caption')
                            if caption:
                                link_wrapper['title'] = caption.get_text()

                        tag.wrap(link_wrapper)

                        break # So we only use the first class specified

            p._content = soup.decode()

def register():
    signals.content_object_init.connect(wrap_image_tags)
