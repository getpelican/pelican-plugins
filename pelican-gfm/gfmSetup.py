#!/usr/bin/python3 -B

import sys
import os
import subprocess
import config
from backports import tempfile

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
 packages: " + need_to_be_installed )
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
            subprocess.call([
                             "wget",
                             "--quiet",
                             config.ARCHIVES + "/" + config.VERSION + ".tar.gz",
                             WORKSPACE,
                             "-P",
                             WORKSPACE
                             ])
            subprocess.call([
                             'tar',
                             'zxf',
                             WORKSPACE + "/" + config.VERSION + ".tar.gz",
                             "-C",
                             WORKSPACE
                             ]
                            )

            BUILDSPACE = WORKSPACE + "/" + "cmark-gfm-" + config.VERSION + "/build"

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
            subprocess.call([
                             "mv",
                             BUILDSPACE + "/src/libcmark-gfm.so." + config.VERSION,
                             config.LIBCMARKLOCATION + "libcmark-gfm.so"
                            ]
                            )
            subprocess.call([
                             "mv",
                             BUILDSPACE + "/extensions/libcmark-gfmextensions.so." + config.VERSION,
                             config.LIBCMARKLOCATION + "libcmark-gfmextensions.so"
                            ]
                            )


def test_configuration():
    """ Tests to ensure that the files that the plugin needs are in place. """
    CMARKPATH = config.LIBCMARKLOCATION + "/libcmark-gfm.so." + config.VERSION
    if os.path.isfile(config.LIBCMARKLOCATION + "/libcmark-gfm.so") and \
            os.path.isfile(config.LIBCMARKLOCATION + "/libcmark-gfmextensions.so"):
        return True
    else:
        return False


def configure():
        print("Checking out the configuration")
        setup()


if __name__ == "__main__":
    configure()
