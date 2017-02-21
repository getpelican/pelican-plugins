
import os
import re
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

base_dir = os.path.dirname(os.path.abspath(__file__))


def get_version(filename="pelican_comment_system/__init__.py"):
    with open(os.path.join(base_dir, filename), encoding="utf-8") as initfile:
        for line in initfile.readlines():
            m = re.match("__version__ *= *['\"](.*)['\"]", line)
            if m:
                return m.group(1)


setup(
    name="pelican_comment_system",
    version=get_version(),
    description="Allows you to add static comments to your articles on your Pelican blog.",
    long_description="\n\n".join([open(os.path.join(base_dir, "Readme.rst")).read(),
                                  open(os.path.join(base_dir, "CHANGELOG.rst")).read()]),
    author="Bernhard Scheirle",
    # author_email="",
    url="http://bernhard.scheirle.de/posts/2014/March/29/static-comments-via-email/",
    packages=['pelican_comment_system',
              'pelican_comment_system.identicon'],
    include_package_data=True,
    install_requires=[
        'pelican>=3.4',
        'pillow',
        ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.4',
        # 'Programming Language :: Python :: 3.5',
        # 'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
)
