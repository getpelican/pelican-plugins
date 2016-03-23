<script id="mathjaxscript_pelican_#%@#$@#" type="text/javascript">
//see https://docs.mathjax.org/en/v2.5-latest/configuration.html#using-plain-javascript
    var align = "{{align}}",
        indent = "{{indent}}",
        linebreak = {{ 'true' if process_escapes else 'false'}};

    if ({{responsive}}) {
        align = (screen.width < {{responsive_break}}) ? "left" : align;
        indent = (screen.width < {{responsive_break}}) ? "0em" : indent;
        linebreak = (screen.width < {{responsive_break}}) ? true : linebreak;
    }
    window.MathJax = {
        config: ['MMLorHTML.js'],
        TeX: {
            extensions: [
                {% for ext in tex_extensions %}
                    {% if not loop.last %}
                        "{{ext}}",
                    {% else %}
                        "{{ext}}"
                    {% endif %}
                {% endfor %}
            ],
            equationNumbers: { autoNumber: 'AMS' } },
        jax: ['input/TeX','input/MathML','output/HTML-CSS'],
        extensions: ['tex2jax.js','mml2jax.js','MathMenu.js','MathZoom.js'],
        displayAlign: align,
        displayIndent: indent,
        showMathMenu: {{'true' if show_menu else 'false'}},
        messageStyle: '{{message_style}}',
        tex2jax: { 
            inlineMath: [ ['\\(','\\)'] ], 
            displayMath: [ ['$$','$$'] ],
            processEscapes: {{'true' if process_escapes else 'false'}},
            preview: '{{latex_preview}}',
        }, 
        "HTML-CSS": { 
            styles: { '.MathJax_Display, .MathJax .mo, .MathJax .mi, .MathJax .mn': {color: '{{color}} !important'} },
            linebreaks: {
                automatic: linebreak,
                width: '90% container' },
        }, 
    }; 
    if ('{{mathjax_font}}' !== 'default') {
        window.MathJax.AuthorInit = function() {
            MathJax.Hub.Register.StartupHook('HTML-CSS Jax Ready',function () {
                var VARIANT = MathJax.OutputJax['HTML-C}'].FONTDATA.VARIANT;
                VARIANT['normal'].fonts.unshift('MathJax_{{mathjax_font}}');
                VARIANT['bold'].fonts.unshift('MathJax_{{mathjax_font}}-bold');
                VARIANT['italic'].fonts.unshift('MathJax_{{mathjax_font}}-italic');
                VARIANT['-tex-mathit'].fonts.unshift('MathJax_{{mathjax_font}}-italic');
            });
            MathJax.Hub.Register.StartupHook('SVG Jax Ready',function () {
                var VARIANT = MathJax.OutputJax.SVG.FONTDATA.VARIANT;
                VARIANT['normal'].fonts.unshift('MathJax_{{mathjax_font}}');
                VARIANT['bold'].fonts.unshift('MathJax_{{mathjax_font}}-bold');
                VARIANT['italic'].fonts.unshift('MathJax_{{mathjax_font}}-italic');
                VARIANT['-tex-mathit'].fonts.unshift('MathJax_{{mathjax_font}}-italic');
            });
        }
    }
</script>
<script id="mathjaxscript_pelican_#%@#$@#"
        type="text/javascript"
        src="{{source}}" >
</script>