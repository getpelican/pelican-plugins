<script id="mathjaxscript_pelican_#%@#$@#"
        type="text/javascript"
        src="{{source}}" >
    var align = "{{align}}",
    var indent = "{{indent}}",
    var linebreak = "{{linebreak_automatic}}";

    if ({{responsive}}) {
        align = (screen.width < {{responsive_break}}) ? "left" : align;
        indent = (screen.width < {{responsive_break}}) ? "0em" : indent;
        linebreak = (screen.width < {{responsive_break}}) ? 'true' : linebreak;
    }
    MathJax.Hub.Config({
        config: ['MMLorHTML.js'],
        TeX: {
            extensions: {{tex_extensions|join(',')}}],
            equationNumbers: { autoNumber: 'AMS' } },
        jax: ['input/TeX','input/MathML','output/HTML-CSS'],
        extensions: ['tex2jax.js','mml2jax.js','MathMenu.js','MathZoom.js'],
        displayAlign: align,
        displayIndent: indent,
        showMathMenu: '{{show_menu}}',
        messageStyle: '{{mesage_style}}',
        tex2jax: { 
            inlineMath: [ ['\\(','\\)'] ], 
            displayMath: [ ['$$','$$'] ],
            processEscapes: {{process_escapes}},
            preview: '{{latex_preview}}',
        }, 
        HTML-CSS: { 
            styles: { '.MathJax_Display, .MathJax .mo, .MathJax .mi, .MathJax .mn': {color: '{{color}} !important'} },
            linebreaks: { automatic: linebreak, width: '90% container' },
        }, 
    }); 
    if ('{{mathjax_font}}' !== 'default') {
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
</script>