
import io
import os
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
VERSION = "0.2.15"
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

        cwd_pointer = os.getcwd()

        try:
            self.announce("cmake config.", level=3)

            source_path = os.path.join(
                HERE, "external", "hexwatershed")
            
            source_path = os.path.expandvars(source_path)

            # Check if the expanded path exists
            if os.path.exists(source_path):
                print('Path exists:', source_path)
            else:
                print('Path does not exist:', source_path)      

            builds_path =  os.path.join(source_path, "build")

            if os.path.exists(builds_path):                
                sFilename_cache  = os.path.join(builds_path, "CMakeCache.txt")
                if os.path.exists(sFilename_cache):
                    os.remove(sFilename_cache)
                else:
                    #print('File or directory does not exist')
                    pass
                pass
            else:
                os.mkdir(builds_path)

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
            #copy cmakelistx.txt to the build folder            
            dst = os.getcwd()
            shutil.copy("../CMakeLists.txt", dst)
            config_call = ["cmake",  "CMakeLists.txt"]
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
    data_files=[('external', ["hexwatershed/*.txt",
                              "hexwatershed/src/*.h","hexwatershed/src/*.cpp",
                              "hexwatershed/src/compset/*.h","hexwatershed/src/compset/*.cpp",
                              "hexwatershed/src/domain/*.h","hexwatershed/src/domain/*.cpp",
                              "hexwatershed/src/json/*.h","hexwatershed/src/json/*.cpp",
                               "rapidjson/*.h", "rapidjson/*.cpp",
                               "rapidjson/error/*.h", "rapidjson/error/*.cpp",
                               "rapidjson/internal/*.h", "rapidjson/internal/*.cpp",
                               "rapidjson/msinttypes/*.h", "msinttypes/error/*.cpp"
                               ])
                               ],
    packages=['pyhexwatershed'],
    package_data={
        "pyhexwatershed": ["_bin/*", "_lib/*"]       
        },
    install_requires=REQUIRED,
    cmdclass={"build_external": build_external},
    classifiers=CLASSIFY
)
