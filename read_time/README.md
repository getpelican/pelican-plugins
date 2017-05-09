Read Time
===================================

This plugin calculates the read time for each article based on the number of words and a words per minute count. There are two ways to set up the plugin: using words per minute only or using the more advanced language option.

## Setting Up

#### 1. Words Per Minute Only

In your settings you would use assign the `READ_TIME` variable to an integer like so:

***pelicanconf.py***
```
READ_TIME = 180
```

Every article's read time would  be calculated using this average words per minute count. (See the Usage section for how to use the calculated read times in templates). This is the simplest read time method.

#### 2. Words Per Minute per language

This is the preferred method if you are dealing with multiple languages. Take a look at the following settings


***pelicanconf.py***
```
READ_TIME = {
    'default': {
        'wpm': 180,
        'plurals': ['minute', 'minutes']
    },
    'es': {
        'wpm': 200,
        'plurals': ['minuto', 'minutos']
    },
    'it': {
    	'plurals': ['minuto', 'minuti']
	}
}
```


In this example the default reading time for all articles is 180 words per minute. Any articles in spanish will be calculated at 200 wpm. This is useful for information dense languages where the read time varies rapidly.

Also notice the Italian language, the read time for all italian articles will be 180wpm (the default value). However, the article will also be able to take advantage of the plurality option. An italian article that takes four minutes to read will have access to a variable that prints "4 minuti". (See the Usage section for how to use the calculated read times in templates)

Chances are the average reading time will not vary rapidly from language to language, however using this method also allows you to set plurals which make templating easier in the long run.

## Usage

Two variables are accessible through the read time plugin, **read_time** and **read_time_string**

```
This article takes {{article.read_time}} minute(s) to read.
// This article takes 4 minute(s) to read
```

```
This article takes {{article.read_time_string}} to read.
// This article takes 4 minutes to read
```

## Contact

Deepak Bhalla https://deepakrb.com 2016