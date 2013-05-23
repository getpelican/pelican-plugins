A Yaml Plugin For Pelican and Emacs org-mode.
=============================================

author: Ian Barton (ian@manor-farm.org) with thanks to bas@baslab, who
turned my original code into a plugin and also to contact@saimon.org,
who fixed the problems I was having with unicode.


This plugin provides a reader for yaml formatted files. Its main purpose is to allow user of Emacs org-mode to export their blog posts as html with a yaml frontend and use Pelican to publish them.

Usage.
------

In order to use this plugin with org-mode you need to define your org-publish-project-alist:

    #+begin_src emacs-lisp
    (require 'ox-html)
    (setq org-publish-project-alist
          '(

           ;; ... add all the components here (see below)...

      ("org-ianbarton"
              :base-directory "~/Documents/emacs/web_sites/ianbarton/org/_posts"
              :base-extension "org"
              :publishing-directory "~/Documents/emacs/web_sites/ianbarton/pelican/blog/content"
              :recursive t
              :publishing-function org-html-publish-to-html
              :headline-levels 4             ; Just the default for this project.
              :auto-preamble t
              :auto-index f
              :html-extension "yml"
              :auto-preamble t
              :body-only t
        )

      ("org-static-ian"
              :base-directory "~/Documents/emacs/web_sites/ianbarton/org/_posts"
              :base-extension "css\\|js\\|png\\|jpg\\|gif\\|pdf\\|mp3\\|ogg\\|swf\\|php"
              :publishing-directory "~/Documents/emacs/web_sites/ianbarton/pelican/blog/content"
              :recursive t
              :publishing-function org-ox-publish-attachment)


        ("ianbarton" :components ("org-ianbarton" "org-static-ian"))



          ))

Writing a Blog Post.
--------------------
Posts shoud be formatted as shown in the example below. The yaml front matter is enclosed inside the "---" block. Any text below this will be converted to html by the org-mode exporter. If you want to include any html in your post you can enclose it between #+begin_html and #+end_html tags in your text. An example org file is shown below.

#+STARTUP: showall indent
#+STARTUP: hidestars
#+INFOJS_OPT: view:info toc:t ltoc:nil
#+OPTIONS: H:2 num:nil tags:nil toc:nil timestamps:nil
#+TITLE: Mynydd Mawr.
#+BEGIN_HTML
---
date: 2010-02-17
layout: post
title: Mynydd Mawr.
summary: Mynydd Mawr is an outlier of the Moel Hebog group and is situated between Snowdon and the Nantlle Ridge. It's not very high - 698m or 2269ft, but because of it's position the views from the top are spectacular.
category: blog
comments: true
tags: [mountaineering, trips]
---
#+END_HTML
The body of your article goes here.

Insert some literal html into your article:

#+BEGIN_HTML
<p> An example of inserting html </p>
#+END_HTML

Mynydd Mawr is an outlier of the Moel Hebog group and is situated
between Snowdon and the Nantlle Ridge. It's not very high - 698m or
2269ft, but because of it's position the views from the top are
spectacular.
