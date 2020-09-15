Reddit poster posts articles to reddit
===================================

You can use the 'subreddit' attribute in you articles to specify which 
subbreddit the article should be post in aside of your default sub.

We look for the subreddit in the metadata.
Then try to find a post that has the same title as this article.
If we can't find a post we create it.

## Usage
I followed these steps for praw: https://praw.readthedocs.io/en/latest/getting_started/authentication.html#script-application
Summeraized:
+ Go to https://www.reddit.com/prefs/apps/ 
+ create a script for example named 'reddit-poster'.
+ redirect uri is unused so can be http://localhost:8080
+ about uri is probably some page on your website, not important either I think

This will create an 'application', ie it let's reddit know you have a script by 
using the secret generated.
Interesting from this screen is the secret and the app id. copy those over 
somewhere.

We need 4 pieces of information from you which you must *not* commit to source 
code. These should all be considered private.
This script will expect these values to be set in the settings.
You should store them for real in either an ignored file, environment variables,
or pass them each time as command line options.
Also make sure to set your SITEURL, for proper backlinks

https://praw.readthedocs.io/en/latest/code_overview/models/subreddit.html#praw.models.Subreddit.search
https://praw.readthedocs.io/en/latest/code_overview/models/subreddit.html#praw.models.Subreddit.submit

### Config example

```python
REDDIT_POSTER_AUTH = {
    'username': 'blah',
    'password': 'pass',
    'client_id': 'client',
    'client_secret': 'secret',
    'user_agent': 'python:pelican_redditposter:1 by /u/jappieofficial'
}
REDDIT_POSTER_COLLECT_SUB = "jappie"
```
## Dependencies
+ praw 5.4

On fedora the praw in yum is too old, however the pip requests doesn't 
work for some reason, so I installed praw with pip and requests with dnf 
which seems to work (requests probably needed some sys lib or something)
