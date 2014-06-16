# RMD Reader

This plugin helps you creating posts with knitr's RMarkdown files.
[knitr](http://yihui.name/knitr/) is a template engine which executes and displays embedded R code.
So, being short you can write an executable paper with codes, formulas and graphics.

## Dependency

This plugin needs [rpy2](https://pypi.python.org/pypi/rpy2) to work.
Install it with:

```
pip install rpy2
```

## Usage

The plugin detects RMD files ending with `.Rmd` or `.rmd` so you only have to write a RMarkdown files inside content directory.

This plugin calls R to process these files and generates markdown files that are processed by Python Markdown (with `meta`, `codehilite(css_class=highlight)`, and `extra` extensions) before returning the content and metadata to pelican engine.

