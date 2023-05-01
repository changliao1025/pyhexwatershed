
import io

import subprocess
import shutil


try:
    from setuptools import setup, Extension, find_packages
    # Required for compatibility with pip (issue #177)
    from setuptools.command.install import install
except ImportError:
    from distutils.core import setup, Extension
    from distutils.command.install import install

try:
    from wheel.bdist_wheel import bdist_wheel
except ImportError:
    bdist_wheel = None

from distutils.command.build import build
from distutils.command.build_ext import build_ext
from distutils.command.clean import clean
from distutils import log
from distutils.dir_util import remove_tree
from distutils.spawn import spawn
import os
import sys

NAME = "hexwatershed"
DESCRIPTION = \
    "A mesh independent flow direction model for hydrologic models"
AUTHOR = "Chang Liao"
AUTHOR_EMAIL = "chang.liao@pnnl.gov"
URL = "https://github.com/changliao1025/pyhexwatershed"
VERSION = "0.1.14"
REQUIRES_PYTHON = ">=3.8.0"
KEYWORDS = "hexwatershed hexagon"

REQUIRED = [
    "pyflowline",
    "cxx-compiler",
    "cmake"
]

CLASSIFY = [
    "Development Status :: 4 - Beta",
    "Operating System :: OS Independent",
    "Intended Audience :: Science/Research",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: C++",
    "Topic :: Scientific/Engineering",
    "Topic :: Scientific/Engineering :: Hydrology",
    "Topic :: Scientific/Engineering :: GIS",
    "Topic :: Scientific/Engineering :: Physics"
]

HERE = os.path.abspath(os.path.dirname(__file__))

try:
    with io.open(os.path.join(
            HERE, "README.md"), encoding="utf-8") as f:
        LONG_DESCRIPTION = "\n" + f.read()

except FileNotFoundError:
    LONG_DESCRIPTION = DESCRIPTION

def get_cmake_version():
    try:
        out = subprocess.check_output(
            ["cmake", "--version"]).decode("utf-8")
        sln = out.splitlines()[0]
        ver = sln.split()[2]
        return ver

    except:
        print("cmake not found!")


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    license="custom",
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    python_requires=REQUIRES_PYTHON,
    keywords=KEYWORDS,
    url=URL,
    packages=find_packages(),    
    install_requires=REQUIRED,
    classifiers=CLASSIFY
)
