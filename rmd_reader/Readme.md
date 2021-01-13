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

This plugin requires [rpy2](https://pypi.python.org/pypi/rpy2) in a 2.x version.
Install it with:

```
pip install "rpy2<3"
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

`rmd_reader` has these variables that can be set in `pelicanconf`.

- `RMD_READER_CLEANUP` (`True`): The RMarkdown file is converted into a Markdown file with the extension `.aux` (to avoid conflicts while pelican is processing). This file is processed by pelican's MarkdownReader and is removed after that (the cleanup step). So if you want to check this file set `RMD_READER_CLEANUP=True`.
- `RMD_READER_RENAME_PLOT` (`chunklabel`): the figures generated for plots are named with a default prefix (usually `unnamed-chunk`) followed by a sequential number. That sequence starts on 1 for every processed file, which causes naming conflicts among files. In order to avoid these conflicts `RMD_READER_RENAME_PLOT` can be set `chunklabel` and that prefix is replaced with the name of the markdown source, without extension. Alternatively, `RMD_READER_RENAME_PLOT` can be set `directory` in which case the `fig.path` (defaults to `figure/`) is augmented with the path to markdown source including the name of the source file without extension.  Another way to avoid conflicts is naming the chuncks and in that case this variable can be set to any other string.
- `RMD_READER_KNITR_QUIET` (`True`): sets `knitr`'s quiet argument.
- `RMD_READER_KNITR_ENCODING` (`UTF-8`): sets `knitr`'s encoding argument.
- `RMD_READER_KNITR_OPTS_CHUNK` (`None`): sets `knitr`'s `opts_chunk`.
- `RMD_READER_KNITR_OPTS_KNIT` (`None`): sets `knitr`'s `opts_knit`.


### Plotting

I strongly suggest using the variable `RMD_READER_RENAME_PLOT='chunklabel'`.
That helps with avoiding naming conflits among different posts.
`rmd_reader` sets knitr's `unnamed.chunk.label` option to the Rmd file name (without extension) in runtime.

Alternatively, Rebecca Weiss (@rjweiss) suggested using `opts_chunk` to set knitr's `fig.path` ([link](http://rjweiss.github.io/articles/2014_08_25/testing-rmarkdown-integration/)).
Now that can be done directly in `pelicanconf` thougth `RMD_READER_KNITR_OPTS_CHUNK`, that variable receives a `dict` with options to be passed to knitr's `opts_chunk`. With this scheme you can set `RMD_READER_RENAME_PLOT='directory'` and add the generated figures directory to `STATIC_PATHS`.

```
RMD_READER_RENAME_PLOT = 'directory'
RMD_READER_KNITR_OPTS_CHUNK = {'fig.path': 'figure/'}
STATIC_PATHS = ['figure']
```

