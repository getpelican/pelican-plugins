# Better Code Line Numbering Plugin

## Copyright, Contact, and Acknowledgements

This plugin is copyright 2014 Jacob Levernier  
It is released under the BSD 2-Clause License (http://opensource.org/licenses/BSD-2-Clause). This basically means that you can do whatever you want with the code, provided that you include this copyright and license notice.

Some of this code is modified from my YouTube Privacy Enhancer plugin for Pelican (https://github.com/getpelican/pelican-plugins/pull/183).


### To contact the author:

* jleverni at uoregon dot edu  
* http://AdUnumDatum.org  
* BitBucket: https://bitbucket.org/jlev_uo/  
* Github: https://github.com/publicus  

This is the second plugin that I've written for Pelican, and it was intended as a training project for learning Pelican as well as Python better. I would be very happy to hear constructive feedback on the plugin and for suggestions for making it more efficient and/or expandable. Also, I've heavily annotated all of the Python code in order to make it easier to understand for others looking to learn more, like I was when I wrote the plugin.

### Acknowledgements

I'm grateful to the authors of the plugins in the pelican-plugins repo; being able to look over other plugins' authors' code helped me immensely in learning more about how Pelican's [signals](http://docs.getpelican.com/en/3.3.0/plugins.html#how-to-create-plugins "Pelican documentation on creating plugins") system works.


## Explanation and Rationale

Pelican uses Python's built-in code highlighting extension when processing Markdown. This extension, called Code HiLite (https://pythonhosted.org/Markdown/extensions/code_hilite.html), can add line numbers to any code that is enclosed in triple backticks (and, by default, has a shebang as a first line), like this:

```
#!python

code goes here

more code goes here
```

This works well, except for one problem: If the lines of code are long (or if the page template is narrow), the code will run off of the page, requiring that the user scroll sideways to read it. This can be annoying in some circumstances (e.g., if the code block scrollbar is at the very bottom of a long block of code). The Code HiLite Python extension creates line numbers by making a table with all of the line numbers in one column (as a big line of text, not separated into different table rows) and the code in the second column, like this:

Column 1  | Column 2  
--------- | -------------  
1         | Code line 1 goes here, and maybe is very very long.  
2         | Code line 2 goes here.  

It is possible to use CSS to get this code to wrap, but the line numbers can become mis-matched with the code to which they're supposed to refer, like this:

Column 1  | Column 2  
--------- | -------------  
1         | Code line 1 goes here, and  
2         | maybe is very very long.  
          | Code line 2 goes here.

This plugin enables the use of a CSS technique from http://bililite.com/blog/2012/08/05/line-numbering-in-pre-elements/ . All that this plugin does is wrap every individual line of a code block with <span class="code-line">...</span>. When you combine this with the CSS that's included in the setup instructions below, your code blocks will word-wrap and have nicely formatted line numbers. Since they're added with CSS, the line numbers will not be highlighted when a user wants to copy and paste the contents of the code block, making it easier for the user to benefit from what you've written.


## Usage

**After you set up the plugin (by following the steps below), any code written in triple backticks will have line numbers added to it.** Thus, to avoid line numbers, you can use a single backtick to include code `like this`, and can add line numbers by using three backticks

```
like this
```

That's all there is to it!

Since this plugin builds on the Code HiLite plugin, you can change syntax highlighting by using one of two methods:

```{python}
This code will highlight as python
```

```
#!python
This code will also highlight as python
```


**In order for this plugin to work optimally, you need to do just a few things:**

1. Enable the plugin in pelicanconf.py (see http://docs.getpelican.com/en/3.3.0/plugins.html for documentation):  
    PLUGIN_PATH = "/pelican-plugins"  
    PLUGINS = ["better_codeblock_line_numbering"]

2. Add the following to your pelicanconf.py file:  
```
MD_EXTENSIONS = [
    'codehilite(css_class=highlight,linenums=False)',
    'extra'
    ]
```  
This sets python's CodeHiLite Markdown extension (http://pythonhosted.org/Markdown/extensions/code_hilite.html) so that it never assigns line numbers (since we're taking care of those ourselves now), and to wrap code blocks in a div with class="highlight". As is the default for Pelican (see http://docs.getpelican.com/en/3.1.1/settings.html, under "MD_EXTENSIONS"), this also keeps the 'extra' extension (http://pythonhosted.org/Markdown/extensions/extra.html) active.

3. Add the following code to your CSS file:  
```
/* For use with the code_line-number_word-wrap_switcher_jquery.js Pelican plugin */
code {
	overflow: auto;
	/* This uses `white-space: pre-wrap` to get elements within <pre> tags to wrap. Python, for code chunks within three backticks (```), doesn't wordwrap code lines by default, because they're within <pre> tags, which don't wrap by default. See https://github.com/github/markup/issues/168 , which is specifically about this parsing issue, even though that link's discussion is talking about GitHub. */
	white-space: pre-wrap;       /* css-3 */
    white-space: -moz-pre-wrap;  /* Mozilla, since 1999 */
    white-space: -pre-wrap;      /* Opera 4-6 */
    white-space: -o-pre-wrap;    /* Opera 7 */
    word-wrap: break-word;       /* Internet Explorer 5.5+ */
}

/* Following http://bililite.com/blog/2012/08/05/line-numbering-in-pre-elements/, use CSS to add line numbers to all spans that have the class 'code-line' */

.highlight pre {
    counter-reset: linecounter;
    padding-left: 2em;
}
.highlight pre span.code-line {
	counter-increment: linecounter;
    padding-left: 1em;
	text-indent: -1em;
	display: inline-block;
}
.highlight pre span.code-line:before {
    content: counter(linecounter);
    padding-right: 1em;
    display: inline-block;
    color: grey;
    text-align: right;
}
```

