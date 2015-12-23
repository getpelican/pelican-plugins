#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Script used to run the test suite of pelican plugins

Usage: ``./runtests.py [args]``

If no arg is provided it runs the test suite on all local plugins that provides
``test_*`` files(submodules are ignored).

You can pass args to run the script just on few plugins.

example: ``./runtests.py liquid_tags asciidoc_reader ``

"""
from __future__ import print_function

import csv
import fnmatch
import logging
import os
import re
import subprocess
import sys

PYTHON_VERSION = '.'.join(str(i) for i in sys.version_info[:2])
ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
# List of folders that are not plugins
EXCLUDE_DIRS = ['.git', '.tox', '__pycache__', 'test_data', 'latex']

#
# Create a set of plugins
#
# Plugins for which tests need to be fixed
EXCLUDE_PLUGINS = ['read_more_link']
# exclude plugins integrated as submodules
SUB_MOD = []
with open('.gitmodules', "r") as f:
    r = re.compile('(?<=path = ).*')
    for line in f:
        if re.search(r, line):
            m = re.search(r, line)
            SUB_MOD.append(m.group(0))

EXCLUDE = EXCLUDE_DIRS + EXCLUDE_PLUGINS + SUB_MOD
PLUGINS = set([dir for dir in os.listdir(ROOT_DIR)
               if os.path.isdir(dir) and dir not in EXCLUDE])

# override plugins set if arguments are passed
if len(sys.argv) > 1:
    PLUGINS = PLUGINS.intersection(sys.argv[1:])

REQ_FILE = '_requirements.txt'
exit_code = 0

# logging config
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


class ClassifyPlugins(object):
    """Classify plugins in categories to know how to run the tests"""

    def __init__(self):
        self.plug_dict = {'custom': set(),
                          'tests': set(),
                          }
        self.requirements = set()

    def _search_for_toxini(self):
        """Search plugins that provides their own tox.ini file"""

        for p in PLUGINS:
            if 'tox.ini' in os.listdir(p):
                self.plug_dict['custom'].add(p)

    def _search_for_tests(self):
        """Find plugins that provide test files with names matching `test_*`"""

        # TODO: loop is too long, stop at first match
        for p in PLUGINS:
            _test = False
            for root, dirs, files in os.walk(p):
                for f in files:
                    if fnmatch.fnmatch(f, 'test_*.py'):
                        _test = True
            if _test:
                self.plug_dict['tests'].add(p)

    def _list_requirements(self):
        """Store all requirements as a set"""
        self._search_for_toxini()

        default_plugs = PLUGINS.difference(self.plug_dict['custom'])
        for p in default_plugs:
            req_file = os.path.join(p, 'requirements.txt')
            if os.path.exists(req_file):
                with open(req_file) as f:
                    lines = [line.rstrip('\n') for line in f]
                    reqs = set(lines)
                    self.requirements.update(reqs)

    def main(self):
        """Return the plugins lists classfied into a dict"""
        self._search_for_toxini()
        self._search_for_tests()
        self._list_requirements()
        return self.plug_dict, self.requirements


class RunTests(object):
    """Run the tests using tox for each plugin"""

    def __init__(self, plug_dict, req_set):
        self.plug_dict = plug_dict
        self.req_set = req_set
        self.results = []

    def _write_req_file(self):
        """Write a requirements file from req set"""

        with open(REQ_FILE, "w") as rf:
            for req in self.req_set:
                rf.write('{}\n'.format(req))

    def _delete_req_file(self):
        os.remove(REQ_FILE)

    def _run_custom_tests(self):
        """Run tests for plugins that provides their own tox.ini file."""

        for p in self.plug_dict['custom']:
            os.chdir(p)
            errno = subprocess.call(['tox'])
            os.chdir(ROOT_DIR)
            self.results.append({'plugin': p,
                                 'test suite': 'custom',
                                 'exit code': errno})

    def _run_default_tests(self):
        """Run tests for plugins that provides their own tests but no tox.ini"""

        default_plugs = PLUGINS.difference(self.plug_dict['custom'])
        default_plugs_with_tests = default_plugs.intersection(self.plug_dict['tests'])
        for p in default_plugs_with_tests:
            errno = subprocess.call(['tox', '-c', 'default-tox.ini', p])
            self.results.append({'plugin': p,
                                 'test suite': 'default',
                                 'exit code': errno})

    def main(self):
        self._write_req_file()
        self._run_custom_tests()
        self._run_default_tests()
        self._delete_req_file()
        return self.results


if __name__ == "__main__":
    classify = ClassifyPlugins()
    plug_dict, req = classify.main()
    run = RunTests(plug_dict, req)
    results = run.main()
    # order by plugin name
    results = sorted(results, key=lambda r: r['plugin'])


    with open('tests_results.csv', 'w') as csvfile:
        dict_writer = csv.DictWriter(csvfile,
                                     fieldnames=('plugin',
                                                 'test suite',
                                                 'exit code'))
        dict_writer.writeheader()
        dict_writer.writerows(results)

    exit_code = sum(r['exit code'] for r in results)
    logging.info("{}/{} plugins failed their test suite.".format(exit_code,
                                                                 len(results)))
    logging.info("See tests_results.csv file for more details")
    sys.exit(exit_code)
