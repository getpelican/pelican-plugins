# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pelican', 'pelican.plugins.tipue_search']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.1,<5.0.0', 'pelican>=4.5,<5.0']

extras_require = \
{'markdown': ['markdown>=3.2.2,<4.0.0']}

setup_kwargs = {
    'name': 'pelican-tipue-search',
    'version': '0.0.0',
    'description': 'Serialize generated HTML content to a JS variable for use by the Tipue static search jQuery plugin',
    'long_description': 'Tipue Search\n============\n\nA Pelican plugin to serialize generated HTML to a JS variable that can be used by jQuery plugin - Tipue Search.\n\nCopyright (c) Talha Mansoor\n\nAuthor          | Talha Mansoor\n----------------|-----\nAuthor Email    | talha131@gmail.com \nAuthor Homepage | http://onCrashReboot.com \nGithub Account  | https://github.com/talha131 \n\nWhy do you need it?\n===================\n\nStatic sites do not offer search feature out of the box. [Tipue Search](http://www.tipue.com/search/)\nis a jQuery plugin that search the static site without using any third party service, like DuckDuckGo or Google.\n\nTipue search requires the textual content of site in a JS variable.\n\nRequirements\n============\n\nTipue Search requires BeautifulSoup.\n\n```bash\npip install beautifulsoup4\n```\n\nHow Tipue Search works\n=========================\n\nTipue Search serializes the generated HTML into JSON and saves it into a JS variable. Format of JSON is as follows\n\n```javascript\nvar tipuesearch = {\n    "pages": [\n        { \n            "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer nec odio. Praesent libero. Sed cursus ante dapibus diam. Sed nisi. Nulla quis sem at nibh elementum imperdiet. Duis sagittis ipsum. Praesent mauris. Fusce nec tellus sed augue semper porta. Mauris massa. Vestibulum lacinia arcu eget nulla. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Curabitur sodales ligula in libero.",\n            "tags": "Example Category",\n            "url" : "http://oncrashreboot.com/plugin-example.html",\n            "title": "Everything you want to know about Lorem Ipsum"\n        },\n        { \n            "text": "Sed dignissim lacinia nunc. Curabitur tortor. Pellentesque nibh. Aenean quam. In scelerisque sem at dolor. Maecenas mattis. Sed convallis tristique sem. Proin ut ligula vel nunc egestas porttitor. Morbi lectus risus, iaculis vel, suscipit quis, luctus non, massa. Fusce ac turpis quis ligula lacinia aliquet. Mauris ipsum. Nulla metus metus, ullamcorper vel, tincidunt sed, euismod in, nibh.",\n            "tags": "Example Category",\n            "url" : "http://oncrashreboot.com/plugin-example-2.html",\n            "title": "Review of the book Lorem Ipsum"\n        }\n    ]\n};\n```\n\nJS variable is written to file `tipuesearch_content.js` which is created in the root of `output` directory.\n\nHow to use\n==========\n\nYour theme needs to have Tipue Search properly configured in it. [Official documentation](http://www.tipue.com/search/help/) has the required details.\n\nIn addition to the instructions from Tipue, the following has to be added in `pelicanconf.py`.\n\n```python\nPLUGIN_PATH = \'plugins\'\nPLUGINS = [\'tipue_search\']\nDIRECT_TEMPLATES = [\'index\', \'tags\', \'categories\', \'authors\', \'archives\', \'search\']\n```\n\nFurthermore, the generated JavaScript variable has to be sourced in the relevant html pages.\n\n```html\n<script src="{{ SITEURL }}tipuesearch_content.js"></script>\n```\n\nPelican [Elegant Theme](https://github.com/talha131/pelican-elegant) and [Plumage theme](https://github.com/kdeldycke/plumage) have Tipue Search configured. You can view their code to understand the configuration.\n\nBackward Compatibility\n======================\n\nThis plugin requires Tipue Search Version 7.0 or higher.\n\nTipue used to expect content in a json file. Around Version 7.0, Tipue maintainers made a switch to JavaScript variable. tipue_search plugin was updated to reflect this change in commit `4a5f171fc`. Latest version of tipue_search plugin will not work with older versions of Tipue Search.\n\nIf you are using older Tipue Search, prior to 7.0 release, then you will find old version of tipue_search plugin in commit `2dcdca8c8`. \n',
    'author': 'Talha Mansoor',
    'author_email': 'talha131@gmail.com',
    'url': 'https://github.com/getpelican/pelican-plugins/tree/master/tipue_search',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
