
import io
import os
import sys
import subprocess
import shutil

from setuptools import setup, find_packages, Command
from packaging import version

NAME = "hexwatershed"
DESCRIPTION = \
    "A mesh-independent flow direction model for hydrologic models"
AUTHOR = "Chang Liao"
AUTHOR_EMAIL = "chang.liao@pnnl.gov"
URL = "https://github.com/changliao1025/pyhexwatershed"
VERSION = "0.2.0"
REQUIRES_PYTHON = ">=3.8.0"
KEYWORDS = "hexwatershed hexagon"

REQUIRED = [
    "packaging",
    "numpy",
    "matplotlib",
    "gdal",
    "pyflowline"
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

class build_external(Command):

    description = "build external hexwatershed dependencies"

    user_options = []

    def initialize_options(self): pass

    def finalize_options(self): pass

    def run(self):
        """
        The actual cmake-based build steps for hexwatershed

        """
        if (self.dry_run): return

        # Define the Git command to download the submodule
        git_command = "git submodule update --init --recursive"

        cwd_pointer = os.getcwd()

        try:
            self.announce("cmake config.", level=3)

            source_path = os.path.join(
                HERE, "external", "hexwatershed")
            # Run the command using subprocess
            shutil.rmtree(source_path)

            subprocess.run(git_command.split(), check=True)

            builds_path = \
                os.path.join(source_path, "build")

            os.makedirs(builds_path, exist_ok=True)

            exesrc_path = \
                os.path.join(source_path, "bin")

            libsrc_path = \
                os.path.join(source_path, "lib")

            exedst_path = os.path.join(
                HERE, "pyhexwatershed", "_bin")

            libdst_path = os.path.join(
                HERE, "pyhexwatershed", "_lib")

            shutil.rmtree(
                exedst_path, ignore_errors=True)
            shutil.rmtree(
                libdst_path, ignore_errors=True)

            os.chdir(builds_path)

            config_call = [
                "cmake",  "CMakeLists.txt"]
            #' -G "Unix Makefiles"',
            subprocess.run(config_call, check=True)

            self.announce("cmake complie", level=3)

            ver = get_cmake_version()
            if version.parse(ver) < version.parse("3.12"):
                compilecall = [
                    "cmake", "--build", ".",
                    "--config", "Release",
                    "--target", "install"
                    ]
            else:            
                compilecall = [
                    "cmake", "--build", ".",
                    "--config", "Release",
                    "--target", "install",
                    "--parallel", "4"
                    ]

            subprocess.run(compilecall, check=True)

            self.announce("cmake cleanup", level=3)

            shutil.copytree(exesrc_path, exedst_path)
            #shutil.copytree(libsrc_path, libdst_path)

        finally:
            os.chdir(cwd_pointer)
            shutil.rmtree(builds_path)


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
    packages=find_packages(exclude=["tests",]),
    package_data={"pyhexwatershed": ["_bin/*", "_lib/*"]},
    install_requires=REQUIRED,
    cmdclass={"build_external": build_external},
    classifiers=CLASSIFY
)
