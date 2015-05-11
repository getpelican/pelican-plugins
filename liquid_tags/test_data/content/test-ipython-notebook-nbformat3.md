Title: test ipython notebook nb format 3
Date: 2015-03-03
Authors: Testing Man


Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod
tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At
vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren,
no sea takimata sanctus est Lorem ipsum dolor sit amet.

#Loading an entire notebook nbformat = 3.0

{% notebook test_nbformat3.ipynb %}

#Loading selected cells from a notebook nbformat = 3.0

{% notebook test_nbformat3.ipynb cells[1:5] %}
