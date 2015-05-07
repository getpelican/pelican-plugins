# Author Pages

This plugin adds an attribute `page` to the author object which can be used
in templates by themes. The page is processed as an ordinary Pelican page,
so it can be Markdown, reStructuredText, etc.

## Configuration

| Setting            | Default   | Notes                                                                                                                                                         |
|--------------------|-----------|---------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `AUTHOR_PAGE_PATH` | `authors` | The location, relative to the project root where author pages can be found. The filename of the author page minus the extension must match the Author's slug. |

## Template Variables

| Setting       | Notes                                                                                                                                                         |
|---------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `author.page` | The location, relative to the project root where author pages can be found. The filename of the author page minus the extension must match the Author's slug. |
