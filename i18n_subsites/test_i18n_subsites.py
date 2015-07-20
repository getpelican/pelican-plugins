'''Unit tests for the i18n_subsites plugin'''

import os
import locale
import unittest
import subprocess
from tempfile import mkdtemp
from shutil import rmtree

from . import i18n_subsites as i18ns
from pelican import Pelican
from pelican.tests.support import get_settings
from pelican.settings import read_settings


class TestTemporaryLocale(unittest.TestCase):
    '''Test the temporary locale context manager'''

    def test_locale_restored(self):
        '''Test that the locale is restored after exiting context'''
        orig_locale = locale.setlocale(locale.LC_ALL)
        with i18ns.temporary_locale():
            locale.setlocale(locale.LC_ALL, 'C')
            self.assertEqual(locale.setlocale(locale.LC_ALL), 'C')
        self.assertEqual(locale.setlocale(locale.LC_ALL), orig_locale)

    def test_temp_locale_set(self):
        '''Test that the temporary locale is set'''
        with i18ns.temporary_locale('C'):
            self.assertEqual(locale.setlocale(locale.LC_ALL), 'C')


class TestSettingsManipulation(unittest.TestCase):
    '''Test operations on settings dict'''

    def setUp(self):
        '''Prepare default settings'''
        self.settings = get_settings()

    def test_get_pelican_cls_class(self):
        '''Test that we get class given as an object'''
        self.settings['PELICAN_CLASS'] = object
        cls = i18ns.get_pelican_cls(self.settings)
        self.assertIs(cls, object)
        
    def test_get_pelican_cls_str(self):
        '''Test that we get correct class given by string'''
        cls = i18ns.get_pelican_cls(self.settings)
        self.assertIs(cls, Pelican)
        

class TestSitesRelpath(unittest.TestCase):
    '''Test relative path between sites generation'''

    def setUp(self):
        '''Generate some sample siteurls'''
        self.siteurl = 'http://example.com'
        i18ns._SITE_DB['en'] = self.siteurl
        i18ns._SITE_DB['de'] = self.siteurl + '/de'

    def tearDown(self):
        '''Remove sites from db'''
        i18ns._SITE_DB.clear()

    def test_get_site_path(self):
        '''Test getting the path within a site'''
        self.assertEqual(i18ns.get_site_path(self.siteurl), '/')
        self.assertEqual(i18ns.get_site_path(self.siteurl + '/de'), '/de')

    def test_relpath_to_site(self):
        '''Test getting relative paths between sites'''
        self.assertEqual(i18ns.relpath_to_site('en', 'de'), 'de')
        self.assertEqual(i18ns.relpath_to_site('de', 'en'), '..')

        
class TestRegistration(unittest.TestCase):
    '''Test plugin registration'''

    def test_return_on_missing_signal(self):
        '''Test return on missing required signal'''
        i18ns._SIGNAL_HANDLERS_DB['tmp_sig'] = None
        i18ns.register()
        self.assertNotIn(id(i18ns.save_generator),
                         i18ns.signals.generator_init.receivers)

    def test_registration(self):
        '''Test registration of all signal handlers'''
        i18ns.register()
        for sig_name, handler in i18ns._SIGNAL_HANDLERS_DB.items():
            sig = getattr(i18ns.signals, sig_name)
            self.assertIn(id(handler), sig.receivers)
            # clean up
            sig.disconnect(handler)
        

class TestFullRun(unittest.TestCase):
    '''Test running Pelican with the Plugin'''

    def setUp(self):
        '''Create temporary output and cache folders'''
        self.temp_path = mkdtemp(prefix='pelicantests.')
        self.temp_cache = mkdtemp(prefix='pelican_cache.')

    def tearDown(self):
        '''Remove output and cache folders'''
        rmtree(self.temp_path)
        rmtree(self.temp_cache)

    def test_sites_generation(self):
        '''Test generation of sites with the plugin

        Compare with recorded output via ``git diff``.
        To generate output for comparison run the command
        ``pelican -o test_data/output -s test_data/pelicanconf.py \
        test_data/content``
        Remember to remove the output/ folder before that.
        '''
        base_path = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.join(base_path, 'test_data')
        content_path = os.path.join(base_path, 'content')
        output_path = os.path.join(base_path, 'output')
        settings_path = os.path.join(base_path, 'pelicanconf.py')
        settings = read_settings(path=settings_path, override={
            'PATH': content_path,
            'OUTPUT_PATH': self.temp_path,
            'CACHE_PATH': self.temp_cache,
            'PLUGINS': [i18ns],
            }
        )
        pelican = Pelican(settings)
        pelican.run()

        # compare output
        out, err = subprocess.Popen(
            ['git', 'diff', '--no-ext-diff', '--exit-code', '-w', output_path,
             self.temp_path], env={'PAGER': ''},
            stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        self.assertFalse(out, 'non-empty `diff` stdout:\n{}'.format(out))
        self.assertFalse(err, 'non-empty `diff` stderr:\n{}'.format(out))
