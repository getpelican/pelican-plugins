'''
Created on Jan 25, 2016

@author: Aaron Kitzmiller <aaron_kitzmiller@harvard.edu?
'''
import unittest, os, sys
import shutil
import logging
import glob
from pelican import Pelican
from pelican.settings import read_settings

logging.basicConfig(stream=sys.stderr, level=logging.CRITICAL)

class Test(unittest.TestCase):


    def setUp(self):
        try:
            import rpy2
            import rmd_reader
        except Exception, e:
            raise unittest.SkipTest("rpy not installed.  Will not test rmd_reader.")
        
        self.testtitle = 'rtest'
        self.cwd = os.path.dirname(os.path.abspath(__file__))
        
        # Setup content dir and test rmd file
        self.contentdir = os.path.join(self.cwd,'test-content')
        try:
            os.mkdir(self.contentdir)
        except Exception:
            pass
        self.contentfile = os.path.join(self.contentdir,'test.rmd')
        self.testrmd = '''Title: %s
Date: 2014-06-23

Let's make a simple plot about cars.
```{r}
cars <- c(1, 3, 6, 4, 9)
plot(cars)
```
''' % self.testtitle
        with open(self.contentfile,'w') as f:
            f.write(self.testrmd)
            
        # Setup output dir
        self.outputdir = os.path.join(self.cwd,'test-output')
        try:
            os.mkdir(self.outputdir)
        except Exception:
            pass
        
        self.figpath = 'images'
        


    def tearDown(self):
        if os.path.isdir(self.outputdir):
            shutil.rmtree(self.outputdir)
        if os.path.isdir(self.contentdir):
            shutil.rmtree(self.contentdir)


    def testKnitrSettings(self):
        settings = read_settings(path=None, override={
            'PATH': self.contentdir,
            'OUTPUT_PATH': self.outputdir,
            'KNITR_OPTS_CHUNK': {'fig.path' : '%s/' % self.figpath},
            'PLUGIN_PATHS': ['../'],
            'PLUGINS': ['rmd_reader'],
        })
        pelican = Pelican(settings=settings)
        pelican.run()
        
        outputfilename = os.path.join(self.outputdir,'%s.html' % self.testtitle)
        self.assertTrue(os.path.exists(outputfilename),'File %s was not created.' % outputfilename)
        imagesdir = os.path.join(self.outputdir,self.figpath)
        self.assertTrue(os.path.exists(imagesdir), 'figpath not created.')
        images = glob.glob('%s/*' % imagesdir)
        self.assertTrue(len(images) == 1,'Contents of images dir is not correct: %s' % ','.join(images))
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()