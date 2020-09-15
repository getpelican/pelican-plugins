# Auto Pages

This plugin adds an attribute `page` to the author, category, and tag
objects which can be used in templates by themes. The page is processed as
an ordinary Pelican page, so it can be Markdown, reStructuredText, etc.

## Configuration

| Setting              | Default      | Notes                                                                                                                                                               |
|----------------------|--------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `AUTHOR_PAGE_PATH`   | `authors`    | The location, relative to the project root where author pages can be found. The filename of the author page minus the extension must match the Author's slug.       |
| `CATEGORY_PAGE_PATH` | `categories` | The location, relative to the project root where category pages can be found. The filename of the category page minus the extension must match the Category's slug. |
| `TAG_PAGE_PATH`      | `tags`       | The location, relative to the project root where tag pages can be found. The filename of the tag page minus the extension must match the Tag's slug.                |

## Template Variables

| Variable        | Notes                                |
|-----------------|--------------------------------------|
| `author.page`   | `Page` object for the author page.   |
| `category.page` | `Page` object for the category page. |
| `tag.page`      | `Page` object for the tag page.      |
