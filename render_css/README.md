Plugin to render CSS files
==========================

This plugin lets you use css-templates so you can use config-variables like `{{ SITEURL }}` in css files. Just add css files to your templates folder. 

## Installation
Add the following to your pelican settings:
`PLUGINS = ["render_css"]`

## Usage
* Add your css templates in the theme template folder
* Pelican now renders the css files and put them into the css output folder
