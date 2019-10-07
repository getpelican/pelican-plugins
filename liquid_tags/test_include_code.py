import re
import sys
import unittest

import pytest

from . import include_code

if 'nosetests' in sys.argv[0]:
    raise unittest.SkipTest('Those tests are pytest-compatible only')

@pytest.mark.parametrize(
        'input,expected', [
            (
                'test_data/main.c',
                ('test_data/main.c', None, None, None, None, None, None, None)
            ),
            (
                'test_data/main.c lang:c',
                ('test_data/main.c', 'c', None, None, None, None, None, None)
            ),
            (
                'test_data/main.c lang:c lines:1-10',
                ('test_data/main.c', 'c', '1-10', None, None, None, None, None)
            ),
            (
                'test_data/main.c lang:c lines:1-10 :hidefilename:',
                ('test_data/main.c', 'c', '1-10', ':hidefilename:', None, None,
                 None, None)
            ),
            (
                'test_data/main.c lang:c lines:1-10 :hidefilename: :hidelink:',
                ('test_data/main.c', 'c', '1-10', ':hidefilename:', ':hidelink:',
                 None, None, None)
            ),
            (
                'test_data/main.c lang:c lines:1-10 :hidefilename: :hidelink: '\
                ':hideall:',
                ('test_data/main.c', 'c', '1-10', ':hidefilename:', ':hidelink:',
                 ":hideall:", None, None)
            ),
            (
                'test_data/main.c lang:c lines:1-10 :hidefilename: :hidelink: '\
                ':hideall: codec:iso-8859-1',
                ('test_data/main.c', 'c', '1-10', ':hidefilename:', ':hidelink:',
                 ':hideall:', 'iso-8859-1', None)
            ),
            (
                'test_data/main.c lang:c lines:1-10 :hidefilename: :hidelink: '\
                ':hideall: codec:iso-8859-1 Hello It\'s me - Title',
                ('test_data/main.c', 'c', '1-10', ':hidefilename:', ':hidelink:',
                 ':hideall:', 'iso-8859-1', 'Hello It\'s me - Title')
            ),
        ]
)
def test_regex(input, expected):
    print(re.match(include_code.FORMAT, input).groups())
    assert re.match(include_code.FORMAT, input).groups() == expected

class Object:
    pass

class preprocessor:
    @classmethod
    def func(*x, safe=False):
        return ''.join([str(s) for s in x])

    def __init__(self):
        self.configs = Object()
        self.configs.getConfig = lambda x: ''
        self.configs.htmlStash = Object()
        self.configs.htmlStash.store = self.func

@pytest.mark.parametrize(
        'input, expected', [
            (
                'test_data/main.c',
                (
                    '<class \'liquid_tags.test_include_code.preprocessor\'>'
                    '<figure class=\'code\'>\n<figcaption>'
                    '<span>main.c</span> '
                    '<a href=\'/test_data/main.c\'>download</a>'
                    '\n'
                    '\n'
                    '    #include <stdio.h>\n'
                    '    \n'
                    '    int main(int argc, char** argv){\n'
                    '        printf("Hello world!");\n'
                    '    \n'
                    '        return 0;\n'
                    '    }\n'
                    '    \n'
                    '\n'
                    '<class \'liquid_tags.test_include_code.preprocessor\'>'
                    '</figure>\n'
                )
            ),
            (
                'test_data/main.c :hideall:',
                (
                    '<class \'liquid_tags.test_include_code.preprocessor\'>'
                    '<figure class=\'code\'>\n<figcaption>'
                    '\n'
                    '\n'
                    '    #include <stdio.h>\n'
                    '    \n'
                    '    int main(int argc, char** argv){\n'
                    '        printf("Hello world!");\n'
                    '    \n'
                    '        return 0;\n'
                    '    }\n'
                    '    \n'
                    '\n'
                    '<class \'liquid_tags.test_include_code.preprocessor\'>'
                    '</figure>\n'
                )
            ),
            (
                'test_data/main.c :hidefilename: C application',
                (
                    '<class \'liquid_tags.test_include_code.preprocessor\'>'
                    '<figure class=\'code\'>\n<figcaption>'
                    '<a href=\'/test_data/main.c\'>download</a>'
                    '\n'
                    '\n'
                    '    #include <stdio.h>\n'
                    '    \n'
                    '    int main(int argc, char** argv){\n'
                    '        printf("Hello world!");\n'
                    '    \n'
                    '        return 0;\n'
                    '    }\n'
                    '    \n'
                    '\n'
                    '<class \'liquid_tags.test_include_code.preprocessor\'>'
                    '</figure>\n'
                )
            ),
            (
                'test_data/main.c :hidelink:',
                (
                    '<class \'liquid_tags.test_include_code.preprocessor\'>'
                    '<figure class=\'code\'>\n<figcaption>'
                    '<span>main.c</span> '
                    '\n'
                    '\n'
                    '    #include <stdio.h>\n'
                    '    \n'
                    '    int main(int argc, char** argv){\n'
                    '        printf("Hello world!");\n'
                    '    \n'
                    '        return 0;\n'
                    '    }\n'
                    '    \n'
                    '\n'
                    '<class \'liquid_tags.test_include_code.preprocessor\'>'
                    '</figure>\n'
                )
            ),
            (
                'test_data/main.c lang:c',
                (
                    '<class \'liquid_tags.test_include_code.preprocessor\'>'
                    '<figure class=\'code\'>\n<figcaption>'
                    '<span>main.c</span> '
                    '<a href=\'/test_data/main.c\'>download</a>'
                    '\n'
                    '\n'
                    '    :::c\n'
                    '    #include <stdio.h>\n'
                    '    \n'
                    '    int main(int argc, char** argv){\n'
                    '        printf("Hello world!");\n'
                    '    \n'
                    '        return 0;\n'
                    '    }\n'
                    '    \n'
                    '\n'
                    '<class \'liquid_tags.test_include_code.preprocessor\'>'
                    '</figure>\n'
                )
            ),
            (
                'test_data/main.c lines:4-6',
                (
                    '<class \'liquid_tags.test_include_code.preprocessor\'>'
                    '<figure class=\'code\'>\n<figcaption>'
                    '<span>main.c [Lines 4-6]</span> '
                    '<a href=\'/test_data/main.c\'>download</a>'
                    '\n'
                    '\n'
                    '        printf("Hello world!");\n'
                    '    \n'
                    '        return 0;\n'
                    '\n'
                    '<class \'liquid_tags.test_include_code.preprocessor\'>'
                    '</figure>\n'
                )
            ),
            (
                'test_data/main_cz.c codec:iso-8859-1',
                (
                    '<class \'liquid_tags.test_include_code.preprocessor\'>'
                    '<figure class=\'code\'>\n<figcaption>'
                    '<span>main_cz.c</span> '
                    '<a href=\'/test_data/main_cz.c\'>download</a>'
                    '\n'
                    '\n'
                    '    #include <stdio.h>\n'
                    '    \n'
                    '    int main(int argc, char** argv){\n'
                    '        printf("Dobrý");\n'
                    '    \n'
                    '        return 0;\n'
                    '    }\n'
                    '    \n'
                    '\n'
                    '<class \'liquid_tags.test_include_code.preprocessor\'>'
                    '</figure>\n'
                )
            ),
            (
                'test_data/main.c C Application',
                (
                    '<class \'liquid_tags.test_include_code.preprocessor\'>'
                    '<figure class=\'code\'>\n<figcaption>'
                    '<span>C Application main.c</span> '
                    '<a href=\'/test_data/main.c\'>download</a>'
                    '\n'
                    '\n'
                    '    #include <stdio.h>\n'
                    '    \n'
                    '    int main(int argc, char** argv){\n'
                    '        printf("Hello world!");\n'
                    '    \n'
                    '        return 0;\n'
                    '    }\n'
                    '    \n'
                    '\n'
                    '<class \'liquid_tags.test_include_code.preprocessor\'>'
                    '</figure>\n'
                )
            ),
        ]
)
def test_create_html(input, expected):
    assert include_code.include_code(preprocessor(), 'include_code', input) == expected
