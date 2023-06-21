Requirements
------------

* pip install beautifulsoup4

Summary
=======

This plug-in:

- Adds an id tag to header tags, so that you can deep link into a page's or an article's content: post.html#title
- The string of the anchor is the content of the header, lowercased with spaces stripped
- There's no check for repeated anchor names or collision with other existing ids

Example
=======
Given the following generated HTML:

    <h2>Introduction</h2>
    <h3>Longer Subtitle</h3>

the HTML code will be changed into:

    <h2 id="introduction">Introduction</h2>
    <h3 id="longersubtitle">Longer Subtitle</h3>

so that you can link to the introduction paragraph in this manner:

    <a href="page.html#introduction">See the introduction</a>
