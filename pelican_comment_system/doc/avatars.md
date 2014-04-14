# Avatars and Identicons
To activate the avatars and [identicons](https://en.wikipedia.org/wiki/Identicon) you have to set `PELICAN_COMMENT_SYSTEM_IDENTICON_DATA`.

##### Example
```python
PELICAN_COMMENT_SYSTEM_IDENTICON_DATA = ('author')
```
Now every comment with the same author tag will be treated as if written from the same person. And therefore have the same avatar/identicon. Of cause you can modify this tuple so other metadata are checked.

## Specific Avatars
To set a specific avatar for a author you have to add them to the `PELICAN_COMMENT_SYSTEM_AUTHORS` dictionary.

The `key` of the dictionary has to be a tuple of the form of `PELICAN_COMMENT_SYSTEM_IDENTICON_DATA`, so in our case only the author's name.

The `value` of the dictionary is the path to the specific avatar.

##### Example
```python
PELICAN_COMMENT_SYSTEM_AUTHORS = {
	('John'): "images/authors/john.png",
	('Tom'): "images/authors/tom.png",
}
```

## Theme
To display the avatars and identicons simply add the following in the "comment for loop" in your theme:

```html
<img src="{{ SITEURL }}/{{ comment.avatar }}"
		alt="Avatar"
		height="{{ PELICAN_COMMENT_SYSTEM_IDENTICON_SIZE }}"
		width="{{ PELICAN_COMMENT_SYSTEM_IDENTICON_SIZE }}">
```

Of cause the `height` and `width` are optional, but they make sure that everything has the same size (in particular  specific avatars).
