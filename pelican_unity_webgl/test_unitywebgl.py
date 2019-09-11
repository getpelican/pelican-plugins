from unittest import TestCase
from docutils.core import publish_string
from docutils.parsers.rst import directives

from pelican_unity_webgl import config
from pelican_unity_webgl.UnityGameDirective import UnityWebgl


class TestUnityWebgl(TestCase):

    def test_directive_basic(self):

        # test directive html output with default template
        # and settings

        directives.register_directive('unitywebgl', UnityWebgl)

        config.GAMES_ROOT_DIR = '/test_games_root'
        config.TEMPLATE_PATH = '/test_template_path/template'
        config.DEFAULT_WIDTH = 960
        config.DEFAULT_HEIGHT = 600

        html =['<link rel="stylesheet" href="/test_template_path/template/style.css">',
        '<script src="/test_template_path/template/UnityProgress.js">',
        '<script src="/test_games_root/testgame/Build/UnityLoader.js">',
        '<script>\n        var gameInstance = UnityLoader.instantiate("gameContainer", "/test_games_root/testgame/Build/testgame.json", {onProgress: UnityProgress});\n    </script>',
        '<div id="gameContainer" style="width: 960px; height: 600px; left: 50%; transform: translateX(-50%);"></div>']

        res = publish_string('.. unitywebgl:: testgame', writer_name='html', settings_overrides={'output_encoding': 'unicode'})

        passed = True

        for line in html:
            if line not in res:
                passed = False
                break

        assert passed


    def test_directive_with_params(self):

        # test directive html output with all optional parameters,
        # default template and settings

        directives.register_directive('unitywebgl', UnityWebgl)

        config.GAMES_ROOT_DIR = 'test_games_root'
        config.TEMPLATE_PATH = 'test_template_path'
        config.DEFAULT_WIDTH = 960
        config.DEFAULT_HEIGHT = 600

        html =['<link rel="stylesheet" href="/games2/template2/style.css">',
        '<script src="/games2/template2/UnityProgress.js">',
        '<script src="/games2/testgame/Build/UnityLoader.js">',
        '<script>\n        var gameInstance = UnityLoader.instantiate("gameContainer", "/games2/testgame/Build/testgame.json", {onProgress: UnityProgress});\n    </script>',
        '<div id="gameContainer" style="width: 640px; height: 480px; left: 50%; transform: translateX(-50%);"></div>']

        d = '.. unitywebgl:: testgame\n\t:gameroot: /games2\n\t:template: /games2/template2\n\t:width: 640\n\t:height: 480'

        res = publish_string(d, writer_name='html', settings_overrides={'output_encoding': 'unicode'})

        passed = True

        for line in html:
            if line not in res:
                passed = False
                break

        assert passed