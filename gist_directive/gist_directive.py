try:
    from urllib.request import urlopen
except ImportError:
    from urllib import urlopen
import os
import io

from docutils.parsers.rst import directives
from pelican.rstdirectives import Pygments


def fetch(gid, filename, typ):
    if not os.path.exists('.gists'):
        os.mkdir('.gists')
    key = os.path.join('.gists', ("%s/%s/%s" % (typ, gid, filename)).replace('/', ';'))
    if os.path.isfile(key):
        print('LOAD-CACHED:', key)
        return io.open(key, encoding='utf8').read()
    else:
        if typ == 'gist':
            url = 'https://gist.githubusercontent.com/%s/raw/%s' % (gid, filename)
        elif typ == 'github':
            url = 'https://raw.githubusercontent.com/%s/%s' % (gid, filename)
        else:
            raise RuntimeError(typ)
        print('FETCHING:', url)
        fp = urlopen(url)
        if fp.getcode() != 200:
            print('FAILED TO FETCH:', url)
            print('   status code:', fp.getcode())
            print('   response:')
            try:
                print(fp.read())
            finally:
                raise SystemExit()
        data = fp.read()
        with open(key, 'wb') as fh:
            fh.write(data)
        return data.decode('utf8')


class Gist(Pygments):
    """ Embed Github Gist Snippets in rst text

        GIST_ID and FILENAME are required.

        Usage:
          .. gist:: GIST_ID FILENAME

    """

    required_arguments = 1
    optional_arguments = 2
    has_content = False
    gist_type = 'gist'

    def run(self):
        gist = self.arguments[0]
        filename = self.arguments[1] if len(self.arguments) > 1 else ''
        language = self.arguments[2] if len(self.arguments) > 2 else None
        self.arguments = [language]

        self.content = fetch(gist, filename, self.gist_type).splitlines()
        return super(Gist, self).run()


class Github(Gist):
    gist_type = 'github'


def register():
    directives.register_directive('gist', Gist)
    directives.register_directive('github', Github)
