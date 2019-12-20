#!/usr/bin/python3 -B
from __future__ import absolute_import

import sys
import os
import subprocess
import shutil
import tarfile
import tempfile
from gfm import Settings

# Eventually, equivalents for
# other operating systems / package
# managers could be written for this


def dpkg_installed(package):
    """ Uses Dpkg to determine whether or not a package is installed
    requires: <package name>"""
    t1 = subprocess.Popen(["dpkg", "-l"], stdout=subprocess.PIPE)
    t2 = subprocess.Popen([
                            "grep",
                            "-q",
                            package
                          ], stdout=subprocess.PIPE, stdin=t1.stdout)
    data = t2.communicate()
    ec = t2.wait()
    return ec


def dpkg_packages_installed():
    """ Checking to see if the appropriate packages are installed"""
    installed = ["cmake", "make", "wget"]
    removed = [
                "libcmark-gfm-dev",
                "libcmark-gfm-extensions-dev",
                "libcmark-gfm0",
                "libcmark-gfm-extensions0"
              ]

    need_to_be_removed = [package for package in removed
                          if dpkg_installed(package) == 0
                          ]

    need_to_be_installed = [
                            package for package in installed
                            if dpkg_installed(package) == 1
                           ]

    if len(need_to_be_removed) is not 0:
        raise Exception("Found the following conflicting packages\
 which should be removed:" + str(need_to_be_removed))
        rem = False
    else:
        rem = True

    if len(need_to_be_installed) is not 0:
        raise Exception("Could not find the following required\
 packages: " + need_to_be_installed)
        ins = False
    else:
        ins = True

    if rem is True and ins is True:
        print("Packages seem in order.")
        return True


def setup():
    dpkg_packages_installed()

    if test_configuration() == 1:
        print("System appears to be configured")
    else:
        # Configure the environment if it's not already configured

        with tempfile.TemporaryDirectory() as WORKSPACE:
            # Pull into the workspace
            subprocess.call([
                             "wget",
                             "--quiet",
                             os.path.join(Settings.ARCHIVES, Settings.VERSION + ".tar.gz"),
                             WORKSPACE,
                             "-P",
                             WORKSPACE
                             ])

            # Untar the files
            tf = tarfile.open(os.path.join(WORKSPACE, Settings.VERSION + ".tar.gz"))
            tf.extractall(path=WORKSPACE)

            # Create a buildspace for your cmake operation
            BUILDSPACE = WORKSPACE + "/cmark-gfm-" + Settings.VERSION + "/build"

            if not os.path.isdir(BUILDSPACE):
                os.mkdir(BUILDSPACE)

            thing1 = subprocess.Popen([
                                        "cmake",
                                        "-DCMARK_TESTS=OFF",
                                        "-DCMARK_STATIC=OFF",
                                        ".."
                                      ], cwd=BUILDSPACE)
            thing1.wait()

            thing2 = subprocess.Popen(["make"], cwd=BUILDSPACE)
            thing2.wait()

            # Move the libcmark.so artifacts in place
            print("Moving files")
            shutil.move(BUILDSPACE + "/src/libcmark-gfm.so." + Settings.VERSION,
                        Settings.LIBCMARKLOCATION + "/libcmark-gfm.so")
            shutil.move(BUILDSPACE + "/extensions/libcmark-gfmextensions.so." + Settings.VERSION,
                        Settings.LIBCMARKLOCATION + "/libcmark-gfmextensions.so")


def test_configuration():
    """ Tests to ensure that the files that the plugin needs are in place. """
    if os.path.isfile(Settings.LIBCMARKLOCATION + "/libcmark-gfm.so") and \
            os.path.isfile(Settings.LIBCMARKLOCATION + "/libcmark-gfmextensions.so"):
        return True
    else:
        return False


def configure():
        print("Checking out the configuration")
        setup()


if __name__ == "__main__":
    configure()
