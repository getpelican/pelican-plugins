# Linker

This plugin allows to define custom linker commands in analogy to the builtin
`{attach}`, `{author}`, `{category}`, `{filename}`, `{index}`, `{static}` and
`{tag}` syntax.

## Provided commands (each of which in its own submodule)

### `{mailto}`

**Purpose:** Helps to create `mailto:` links with javascript (JS) on top of a
non-JS fallback.

* **How the HTML code is replaced step by step**

  * Your code in a content file (page or article):

    ```
    `Send me a mail <{mailtor}webmaster>`_
    ```

  * Pelican generated output:

    ```
    <a href="{mailto}webmaster">Send me a mail</a>
    ```

  * Plugin replacement (after computing `'jroznfgre' = rot_13('webmaster')`):

    ```
    <a href="/mailto/jroznfgre/">Send me a mail</a>
    ```

  * Result of a JS-powered transform (which you must add):

    ```
    <a href="mailto:webmaster@example.com">Send me a mail</a>
    ```

  * As a fallback for users without JS, the static page
  `mailto/jroznfgre/index.html` is generated using the template
  `mailto_fallback`.

* **Usage instruction**

  * Activate nested `{mailto}` plugin using

    ``
    PLUGINS = ['linker.mailto']
    ``

  * Provide the `mailto_fallback` template (accessing `mailto` which is injected
  into the template)

  * Add JS to the theme to improve the user experience as sketched above

    ```
    <script>
        var pattern = new RegExp("mailto\/([a-z_\.\-]+)\/")
        var a = document.querySelectorAll('a[href^="/mailto/"]');
        for (var i = 0, len = a.length; i < len; i++) {
            var match = pattern.exec(a[i])
            if (match.length == 2) {
                a[i].setAttribute('href', 'mailto:'+match[1].replace(/[a-zA-Z]/g,function(c){return String.fromCharCode((c<="Z"?90:122)>=(c=c.charCodeAt(0)+13)?c:c-26);})+'@example.com')
            }
        }
    </script>
    ```

## Other included submodules

### `content_objects`

This plugin collects all `pelican.contents.Content` instances in a `set` which
can be accessed using `context['content_objects']`.
