# Creole Reader

This plugins allows you to write your posts using the wikicreole syntax. Give to
these files the creole extension. The medata are between `<<header>> <</header>>`
tags.

## Dependency
This plugin relies on [python-creole](https://pypi.python.org/pypi/python-creole/) to work. Install it with:
`pip install python-creole`

## Syntax
Use ** for strong, // for emphasis, one = for 1st level titles.

For the complete syntax, look at: http://www.wikicreole.org/

## Basic example
```
<<header>>
title: Créole
tags: creole, python, pelican_open
date: 2013-12-12
<</header>>

= Title 1
== Title 2

Some nice texte with **strong** and //emphasis//.

* A nice list
** With subelements
* Python

# An ordered list
# A second item
```
