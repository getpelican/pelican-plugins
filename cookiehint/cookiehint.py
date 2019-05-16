"""
Copyright (c) 2019 Ronny Friedland

Cookie Hint
-----------
With this plugin you can display hint if your website uses cookies to the user.

"""
from pelican import signals, generators

plugin_content = {
   'text' : "This website uses cookies. Please read my privacy policy.",
   'html' : """<div id=cookie-hint><div><span>%s</span></div><span id=cookie-confirm onclick='document.cookie="hide-cookie-hint=1;path=/",jQuery("#cookie-hint").slideUp()'>OK</span></div><script>-1!=document.cookie.indexOf("hide-cookie-hint=1")?jQuery("#cookie-hint").hide():(jQuery("#cookie-hints").prependTo("body"),jQuery("#cookie-confirm").show())</script>""",
   'css' : """<style>#cookie-hint div{padding:10px;padding-right:40px}#cookie-hint{outline:1px solid #000000;text-align:right;border-top:1px solid #fff;background:#dedede;position:fixed;bottom:0;z-index:10000;width:100%;font-size:12px;line-height:16px}#cookie-confirm{color:#777;font:14px/100% sans-serif;position:absolute;right:5px;text-decoration:none;text-shadow:0 1px 0 #fff;top:5px;cursor:pointer;border-top:1px solid #fff;border:1px solid #fff;padding:4px}#cookie-confirm:hover{border-bottom:1px solid #fff;border:1px solid #000000}</style>"""
}


def add_cookie_hint(path, context):
    """
    Adds html snippet. 
    """
    with open(path, 'r') as file:
       content = file.read()
       content = content.replace('</body>', plugin_content['html'] % (plugin_content['text']) + '</body>', 1)
       content = content.replace('</head>', plugin_content['css'] + '</head>>', 1) 
    with open(path, 'w') as file:
       file.write(content)


def pelican_initialized(pelican_obj):
    """
    Reads settings.
    """
    try:
        plugin_content.update(pelican_obj.settings['COOKIE_HINT'])
    except:
        pass


def pelican_all_generators_finalized(path, context):
    """
    Process all generated pages and add cookie hint block
    """
    add_cookie_hint(path, context)


def register():
    signals.initialized.connect(pelican_initialized)
    signals.content_written.connect(pelican_all_generators_finalized)
