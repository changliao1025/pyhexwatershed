
import io
import os
import sys
import subprocess
import shutil


try:
    from setuptools import setup, Extension, find_packages
    # Required for compatibility with pip (issue #177)
    from setuptools.command.install import install
    from setuptools.command.build_ext import build_ext
except ImportError:
    from distutils.core import setup, Extension
    from distutils.command.install import install
    from distutils.command.build import build
    from distutils.command.build_ext import build_ext
    from distutils.command.clean import clean
    from distutils import log
    from distutils.dir_util import remove_tree
    from distutils.spawn import spawn
try:
    from wheel.bdist_wheel import bdist_wheel
except ImportError:
    bdist_wheel = None




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

class CMakeExtension(Extension):
    def __init__(self, name, cmake_lists_dir='.', **kwa):
        Extension.__init__(self, name, sources=[], **kwa)
        self.cmake_lists_dir = os.path.abspath(cmake_lists_dir)


class cmake_build_ext(build_ext):

    def get_cmake_version():
        try:
            out = subprocess.check_output(
            ["cmake", "--version"]).decode("utf-8")
            sln = out.splitlines()[0]
            ver = sln.split()[2]
            return ver

        except:
            print("cmake not found!")
    def build_extensions(self):


        # Ensure that CMake is present and working
        try:
            out = subprocess.check_output(['cmake', '--version'])
        except OSError:
            raise RuntimeError('Cannot find CMake executable')

        for ext in self.extensions:

            extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
            cfg = 'Debug' if os.environ.get('DISPTOOLS_DEBUG','OFF') == 'ON' else 'Release'

            cmake_args = [
                '-DCMAKE_BUILD_TYPE=%s' % cfg,
                # Ask CMake to place the resulting library in the directory
                # containing the extension
                '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}'.format(cfg.upper(), extdir),
                # Other intermediate static libraries are placed in a
                # temporary build directory instead
                '-DCMAKE_ARCHIVE_OUTPUT_DIRECTORY_{}={}'.format(cfg.upper(), self.build_temp),
                # Hint CMake to use the same Python executable that
                # is launching the build, prevents possible mismatching if
                # multiple versions of Python are installed
                '-DPYTHON_EXECUTABLE={}'.format(sys.executable),

            ]

            if not os.path.exists(self.build_temp):
                os.makedirs(self.build_temp)

            # Config
            subprocess.check_call(['cmake', ext.cmake_lists_dir] + cmake_args,
                                  cwd=self.build_temp)

            # Build
            subprocess.check_call(['cmake', '--build', '.', '--config', cfg],
                                  cwd=self.build_temp)        



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
    ext_modules=[CMakeExtension(name='hexwatershed')],
    cmdclass={'build_ext':cmake_build_ext},
    classifiers=CLASSIFY
)
