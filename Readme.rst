Pelican Plugins
###############

**Important note:** We are in the process of migrating plugins from this monolithic repository to their own individual repositories under the new `Pelican Plugins`_ organization, a place for plugin authors to collaborate more broadly with Pelican maintainers and other members of the community. The intention is for all the plugins under the new organization to be in the new “namespace plugin” format, which means these plugins can easily be Pip-installed and recognized immediately by Pelican 4.5+ — without having to explicitly enable them.

This transition process will take some time, so we appreciate your patience in the interim. If you would like to help speed up this transition, the following would be very helpful:

* **If you find a plugin here that has not yet been migrated to the new organization**, create a new issue under this repository and communicate which plugin you would like to help migrate, after which a Pelican maintainer will guide you through the process.

* **If you have come here to submit a pull request to add your plugin**, please consider instead moving your plugin under the `Pelican Plugins`_ organization. To get started, create a new issue under this repository with the details of your plugin, after which a Pelican maintainer will guide you through the process.

Whether you are creating a new plugin or migrating an existing plugin, please use the provided `Cookiecutter template <https://github.com/getpelican/cookiecutter-pelican-plugin>`_ to generate a scaffolded namespace plugin that conforms to community conventions. Have a look at the `Simple Footnotes <https://github.com/pelican-plugins/simple-footnotes>`_ repository to see an example of a migrated plugin.

The rest of the information below is relevant for legacy plugins but not for the new namespace plugins found at the `Pelican Plugins`_ organization.

.. _Pelican Plugins: https://github.com/pelican-plugins

Legacy plugins
==================

Legacy plugins are in the **legacy** branch and will probably not work with
Pelican v4.5 and newer without changes.

To install and use these plugins clone this repo and branch::

    git clone --branch legacy --recursive https://github.com/maphew/pelican-plugins

And then refer to ``Readme-legacy`` document at top of the ``pelican-plugins``
folder.


Contributing a plugin
=====================

Please refer to the `Contributing`_ file.

.. _Contributing: Contributing.rst

----------------------------------------------------------------------------

*This fork is a prototype to demo an alternate way of organizing and
presenting the pelican-plugins repo in way that is easier to track and
understand the difference between pre- and and post- Pelican v4.5 plugins.*

*The default branch has been renamed to ``main`` from ``master`` to ensure
people learn about the post-v4.5 migration and only use legacy plugins on purpose.*

*To make this demo 'real' search and replace ``github.com/maphew`` with 
``github.com/getpelican`` and delete these footer paragraphs before merging
the Pull Request.*
