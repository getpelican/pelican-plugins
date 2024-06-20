Evernote to pelican plugin
-----------------
##Description

Plugin pulls notes from your Evernote account and store them as articles/blogposts 

* Allows you to filter notes by tags or anything else (see here https://dev.evernote.com/doc/articles/search_grammar.php)
* Notes are not getting recreared(they are getting stored by the name of there guid 
and on the next run plugin will check if that note already exists)

##how to use it
1. You should get evernote dev account(see requirements)
2. Install requirements 
3. Put mandatory variables to your pelicanconf.py
```
EVERNOTE_CONSUMER_KEY = '***'
EVERNOTE_CONSUMER_SECRET = '***'
EVERNOTE_TOKEN = '***'
```
4.  Add pelican_evernote to your plugins
```
PLUGINS = ['pelican_evernote']
```
5. At that point everything should already work but I would also suggest evernote folder(it will throw an Exception if folder isnt there)
and filter 
that you want to use for notes(so it wont pull all of them)
```
EVERNOTE_FILTER_WORDS = 'tag:pelican'
EVERNOTE_ARTICLE_FOLDER = 'evernote_notes' #that folder is relative to your PATH

```
##Requirements
* Free evernote dev account(https://dev.evernote.com/ _hit get an API key on top right corner_)
* Evernote sdk (_pip install evernote_)
* Markdownify(_pip install markdownify_)