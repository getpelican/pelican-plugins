#!/usr/bin/env python
# -*- coding: utf-8 -*- #

from pelican import signals
import html5lib

RAW_FOOTNOTE_CONTAINERS = ["code"]

def getText(node, recursive = False):
    """Get all the text associated with this node.
       With recursive == True, all text from child nodes is retrieved."""
    L = [u'']
    for n in node.childNodes:
        if n.nodeType in (node.TEXT_NODE, node.CDATA_SECTION_NODE):
            L.append(n.data)
        else:
            if not recursive:
                return None
        L.append(getText(n) )
    return u''.join(L)

def sequence_gen(genlist):
    for gen in genlist:
        for elem in gen:
            yield elem


def parse_for_footnotes(article_or_page_generator):
    all_content = [
      getattr(article_or_page_generator, attr, None) \
      for attr in [u'articles',u'drafts',u'pages'] ]
    all_content = [ x for x in all_content if x is not None ]
    for article in sequence_gen(all_content):
        if u"[ref]" in article._content and u"[/ref]" in article._content:
            content = article._content.replace(u"[ref]", u"<x-simple-footnote>").replace(u"[/ref]", u"</x-simple-footnote>")
            parser = html5lib.HTMLParser(tree=html5lib.getTreeBuilder(u"dom"))
            dom = parser.parse(content)
            endnotes = []
            count = 0
            for footnote in dom.getElementsByTagName(u"x-simple-footnote"):
                pn = footnote
                leavealone = False
                while pn:
                    if pn.nodeName in RAW_FOOTNOTE_CONTAINERS:
                        leavealone = True
                        break
                    pn = pn.parentNode
                if leavealone:
                    continue
                count += 1
                fnid = u"sf-%s-%s" % (article.slug, count)
                fnbackid = u"%s-back" % (fnid,)
                endnotes.append((footnote, fnid, fnbackid))
                number = dom.createElement(u"sup")
                number.setAttribute(u"id", fnbackid)
                numbera = dom.createElement(u"a")
                numbera.setAttribute(u"href", u"#%s" % fnid)
                numbera.setAttribute(u"class", u"simple-footnote")
                numbera.appendChild(dom.createTextNode(unicode(count)))
                txt = getText(footnote, recursive=True).replace(u"\n", u" ")
                numbera.setAttribute(u"title", txt)
                number.appendChild(numbera)
                footnote.parentNode.insertBefore(number, footnote)
            if endnotes:
                ol = dom.createElement(u"ol")
                ol.setAttribute(u"class", u"simple-footnotes")
                for e, fnid, fnbackid in endnotes:
                    li = dom.createElement(u"li")
                    li.setAttribute(u"id", fnid)
                    while e.firstChild:
                        li.appendChild(e.firstChild)
                    backlink = dom.createElement(u"a")
                    backlink.setAttribute(u"href", u"#%s" % fnbackid)
                    backlink.setAttribute(u"class", u"simple-footnote-back")
                    backlink.appendChild(dom.createTextNode(u'\u21a9'))
                    li.appendChild(dom.createTextNode(u" "))
                    li.appendChild(backlink)
                    ol.appendChild(li)
                    e.parentNode.removeChild(e)
                dom.getElementsByTagName(u"body")[0].appendChild(ol)
                s = html5lib.serializer.HTMLSerializer(omit_optional_tags=False, quote_attr_values='legacy')
                output_generator = s.serialize(html5lib.treewalkers.getTreeWalker(u"dom")(dom.getElementsByTagName(u"body")[0]))
                article._content =  u"".join(list(output_generator)).replace(
                    u"<x-simple-footnote>", u"[ref]").replace(u"</x-simple-footnote>", u"[/ref]").replace(
                    u"<body>", u"").replace(u"</body>", u"")


def register():
    signals.article_generator_finalized.connect(parse_for_footnotes)
    signals.page_generator_finalized.connect(parse_for_footnotes)
