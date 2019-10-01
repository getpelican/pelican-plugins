"""minimum config to enable distribution via pip and pipenv."""

import setuptools

with open('README.rst', 'r') as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name='pelican-plugins',
    version='0.0.1',
    description='A collection of plugins for the Pelican static site generator.',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/x-rst',
    url='https://github.com/getpelican/pelican-plugins',
    packages=setuptools.find_packages(),
    license='License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    classifiers=[
        'Framework :: Pelican :: Plugins',
    ],
)
