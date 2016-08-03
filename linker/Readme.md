# Linker

This plugin allows to define custom linker commands in analogy to the builtin
`{filename}`, `{attach}`, `{category}`, `{tag}`, `{author}`, and `{index}`
syntax.

## Provided commands (each of which in its own submodule)

### `{mailto}`

**Purpose:** Helps to create `mailto:` links with javascript (JS) on top of a
non-JS fallback.

* **How the HTML code is replaced step by step**
  * your code in a content file (page or article):

    ```
    <a href="{mailto}webmaster" rel="nofollow">Send me a mail</a>
    ```

  * plugin replacement (after computing `'jroznfgre' = rot_13('webmaster')`):

    ```
    <a href="/mailto/jroznfgre/" rel="nofollow">Send me a mail</a>
    ```

  * result of a JS-powered transform (which you could add):

    ```
    <a href="mailto:webmaster@example.com" rel="nofollow">Send me a mail</a>
    ```

  * As a fallback for users without JS, the static page
  `mailto/jroznfgre/index.html` is generated using the template
  `mailto_fallback`.

* **Usage instruction**
  * activate nested `{mailto}` plugin using

    ```
    PLUGINS = ['linker.mailto']
    ```

  * provide the `mailto_fallback` template (accessing `mailto` which is injected
  into the template)
  * optionally, add some JS to improve the user experience as sketched above

## Other included submodules

### `content_objects`

This plugin collects all `pelican.contents.Content` instances in a `set` which
can be accessed using `context['content_objects']`.