
import io
import os
import subprocess
import shutil
from setuptools import setup, Command, find_packages

NAME = "hexwatershed"
DESCRIPTION = \
    "A mesh-independent flow direction model for hydrologic models"
AUTHOR = "Chang Liao"
AUTHOR_EMAIL = "chang.liao@pnnl.gov"
URL = "https://github.com/changliao1025/pyhexwatershed"
VERSION = "0.2.26"
REQUIRES_PYTHON = ">=3.8.0"
KEYWORDS = ["hexwatershed",
            "hydrology",
            "hydrologic modeling",
            "hydrologic model",
            "flow direction",
             "hexagon"]

REQUIRED = [
    "numpy",
    "gdal",    
    "shapely",
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
HERE = os.path.expandvars(HERE)
# Check if the expanded path exists
if os.path.exists(HERE):
    print('Path exists:', HERE)
else:
    print('Path does not exist:', HERE)

try:
    with io.open(os.path.join(
            HERE, "README.md"), encoding="utf-8") as f:
        LONG_DESCRIPTION = "\n" + f.read()

except FileNotFoundError:
    LONG_DESCRIPTION = DESCRIPTION

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
    setup_requires=['setuptools'],
    packages=find_packages(),
    install_requires=REQUIRED,
    classifiers=CLASSIFY,
    extras_require={
        'visualization': ['cython', 'matplotlib', 'cartopy>=0.21.0']
    }
)
