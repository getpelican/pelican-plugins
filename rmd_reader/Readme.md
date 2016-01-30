# RMD Reader

This plugin helps you creating posts with knitr's RMarkdown files.
[knitr](http://yihui.name/knitr/) is a template engine which executes and displays embedded R code.
So, being short you can write an executable paper with codes, formulas and graphics.

## Loading

It is a good idea to load `rmd_reader` at last.
It uses settings loaded at runtime and it is important to be sure that all settings have been loaded.

```
PLUGINS = ['sitemap',
           'summary',
           ...
           'render_math',
           'rmd_reader']  # put it here!
```

## Dependency

This plugin needs [rpy2](https://pypi.python.org/pypi/rpy2) to work.
Install it with:

```
pip install rpy2
```

Of course, R must be installed and also the knitr package.
Execute the command below in R to get knitr installed.

```
R> install.packages('knitr')
```

## Usage

The plugin detects RMD files ending with `.Rmd` or `.rmd` so you only have to write a RMarkdown files inside `content` directory.

This plugin calls R to process these files and generates markdown files that are processed by Pelican's `MarkdownReader` in order to generate html files from ordinary `.md` files.

### Configuration

`rmd_reader` has these 3 variables that can be set in `pelicanconf`.

- `RMD_READER_CLEANUP` (`True`): The RMarkdown file is converted into a Markdown file with the extension `.aux` (to avoid conflicts while pelican is processing). This file is processed by pelican's MarkdownReader and is removed after that (the cleanup step). So if you want to check this file set `RMD_READER_CLEANUP=True`.
- `RMD_READER_KNITR_QUIET` (`True`): sets `knitr`'s quiet argument.
- `RMD_READER_KNITR_ENCODING` (`UTF-8`): sets `knitr`'s encoding argument.
- `RMD_READER_KNITR_OPTS_CHUNK` (`None`): sets `knitr`'s `opts_chunk`.


### Plotting

The code below must be pasted inside the `.Rmd` file in order to correctly set the `src` attribute of `img` tag.

	```{r, echo=FALSE}
	hook_plot <- knit_hooks$get('plot')
	knit_hooks$set(plot=function(x, options) {
	    if (!is.null(options$pelican.publish) && options$pelican.publish) {
	        x <- paste0("{filename}", x)
	    }
	    hook_plot(x, options)
	})
	opts_chunk$set(pelican.publish=TRUE)
	```

I usually paste it just after the Markdown header.
There is a R [template](https://github.com/almartin82/pelicanRMD) available that has the base elements needed by `rmd_reader`.
