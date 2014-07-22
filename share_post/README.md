Share Post
==========

A Pelican plugin to create share URLs of article

Copyright (c) Talha Mansoor

Author          | Talha Mansoor
----------------|-----
Author Email    | talha131@gmail.com
Author Homepage | http://onCrashReboot.com
Github Account  | https://github.com/talha131

Why do you need it?
===================

Almost all website have share widgets to let readers share posts on social
networks. Most of these widgets are used by vendors for online tracking. These
widgets are also visual which quite often become a distraction and negatively
affect readers attention.

`share_post` creates old school URLs for some popular sites which your theme
can use. These links do not have the ability to track the users. They can also
be unobtrusive depending on how Pelican theme uses them.

Requirements
============

`share_post` requires BeautifulSoup

```bash
pip install beautifulsoup4
```

How to Use
==========

`share_post` adds a dictionary attribute to `article` which can be accessed via
`article.share_post`. Keys of the dictionary are as follows,

1. `facebook`
1. `google-plus`
1. `email`
1. `twitter`

Template Example
================

```python
{% if article.share_post and article.status != 'draft' %}
<section>
    <p id="post-share-links">
        Share on:
        <a href="{{article.share_post['twitter']}}" target="_blank" title="Share on Twitter">Twitter</a>
        ❄
        <a href="{{article.share_post['facebook']}}" target="_blank" title="Share on Facebook">Facebook</a>
        ❄
        <a href="{{article.share_post['google-plus']}}" target="_blank" title="Share on Google Plus">Google+</a>
        ❄
        <a href="{{article.share_post['email']}}" target="_blank" title="Share via Email">Email</a>
    </p>
</section>
{% endif %}
```

