# Mau reader

This plugin allows you to use [Mau](https://github.com/Project-Mau/mau) to write your posts. File extension should be `.mau`.

If you want to use Mau you need to install it with `pip install mau`.

## Settings

The Pelican setting for Mau is called `MAU`.

You can customise the default templates that Mau usses to render HTML adding them under `custom_templates`. E.g. to change the way Mau renders the source code blocks add

``` python
MAU = {
	"custom_templates": {
		"source.html": '<div class="source">{{ code }}</div>'
	}
}
```

Check Mau's documentation for details on how to customise the templates.

