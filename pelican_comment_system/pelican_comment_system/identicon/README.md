identicon.py: identicon python implementation.
==============================================
:Author:Shin Adachi <shn@glucose.jp>

## usage

### commandline

    python identicon.py [code]

### python

    import identicon
    identicon.render_identicon(code, size)

Return a PIL Image class instance which have generated identicon image.
`size` specifies patch size. Generated image size is 3 * `size`.