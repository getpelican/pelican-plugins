#!/usr/bin/python -B

import os
import subprocess

# This gets used by the gfm plugin as well as the check_configure function
LIBCMARKLOCATION = "/usr/lib/x86_64-linux-gnu"

ARCHIVES = "https://github.com/github/cmark-gfm/archive"
VERSION = "0.28.3.gfm.12"
LOCAL = "cmark-gfm.$VERSION.orig.tar.gz"
WORKSPACE = '/tmp/build-cmark'


def dpkg_installed(package):
    t1 = subprocess.Popen(["dpkg", "-l"], stdout=subprocess.PIPE)
    t2 = subprocess.Popen(["grep", "-q", package],
                          stdout=subprocess.PIPE,
                          stdin=t1.stdout,)
    ec = t2.wait()
    return ec


def test_setup():
    installed = ["cmake", "make", "wget"]
    removed = ["libcmark-gfm-dev",
               "libcmark-gfm-extensions-dev",
               "libcmark-gfm0",
               "libcmark-gfm-extensions0", ]
    for package in installed:
        if str(dpkg_installed(package)) == "1":
            print(package + " not installed")
            return 1

    for package in removed:
        if dpkg_installed == "0":
            print(package + " needs removed")
            return 1


def apt_install(package):
    # I need to be able to do this a better, in a less sudo + apt-y way
    subprocess.call(["apt-get", "install", package, "-y"])


def apt_remove(package):
    # I need to be able to do this a better, in a less sudo + apt-y way
    subprocess.call(["apt-get", "purge", package, "-y"])


def cleanUp():
    subprocess.call(["rm", "-rf", WORKSPACE])


def setup():
    test_setup()
    # Configure the environment if it's not already configured
    if not os.path.isdir(WORKSPACE):
        os.mkdir(WORKSPACE)
    subprocess.call(["wget",
                     "--quiet",
                     ARCHIVES + "/" + VERSION + ".tar.gz", WORKSPACE,
                     "-P",
                     WORKSPACE])
    subprocess.call(['tar',
                     'zxf',
                     WORKSPACE + "/" + VERSION + ".tar.gz",
                     "-C",
                     WORKSPACE])
    BUILDSPACE = WORKSPACE + "/" + "cmark-gfm-" + VERSION + "/build"
    if not os.path.isdir(BUILDSPACE):
        os.mkdir(BUILDSPACE)
    thing1 = subprocess.Popen(["cmake",
                               "-DCMARK_TESTS=OFF",
                               "-DCMARK_STATIC=OFF",
                               ".."],
                              cwd=BUILDSPACE)
    thing1.wait()

    thing2 = subprocess.Popen(["make"], cwd=BUILDSPACE)
    thing2.wait()

    # Move the libcmark.so artifacts in place
    print("Moving files")
    gfmfile = BUILDSPACE+"/src/libcmark-gfm.so."+VERSION
    gfmextfile = BUILDSPACE+"/extensions/libcmark-gfmextensions.so."+VERSION
    subprocess.call(["mv",
                     gfmfile,
                     LIBCMARKLOCATION + "libcmark-gfm.so"])
    subprocess.call(["mv",
                     gfmextfile,
                     LIBCMARKLOCATION + "libcmark-gfmextensions.so"])


def test_configuration():
    gfmfile = LIBCMARKLOCATION + "/libcmark-gfm.so"
    gfmextfile = LIBCMARKLOCATION + "/libcmark-gfmextensions.so"
    if os.path.isfile(gfmfile) and os.path.isfile(gfmextfile):
        return 0
    else:
        return 1


def configure():
        print("Configuring!!!")
        setup()
        cleanUp()


if __name__ == "__main__":
    configure()
