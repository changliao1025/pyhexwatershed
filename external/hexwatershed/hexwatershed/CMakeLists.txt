cmake_minimum_required(VERSION 3.10)
project(hexwatershed CXX)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_VERBOSE_MAKEFILE ON)

#set(CMAKE_INSTALL_PREFIX ./bin)
#set(CMAKE_INSTALL_LOCAL_ONLY TRUE)


# Add the cmake folder so the FindSphinx module is found
message("PROJECT_SOURCE_DIR = ${PROJECT_SOURCE_DIR}")
set(CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/cmake" ${CMAKE_MODULE_PATH})
message("CMAKE_MODULE_PATH = ${CMAKE_MODULE_PATH}")
Include_directories(./src)


file(GLOB hexwatershed_srcs ./src/conversion.cpp
        ./src/conversion.h
        ./src/data.cpp
        ./src/data.h
        ./src/depression.cpp
        ./src/depression.h
        ./src/domain.cpp
        ./src/domain.h
        ./src/global.cpp
        ./src/global.h
        ./src/hexagon.cpp
        ./src/hexagon.h
        ./src/main.cpp
        ./src/segment.cpp
        ./src/segment.h
        ./src/system.cpp
        ./src/system.h
        ./src/vertex.cpp
        ./src/vertex.h
        ./src/watershed.cpp
        ./src/watershed.h)

add_executable(hexwatershed ${hexwatershed_srcs})
add_subdirectory ("docs")
set(default_build_type Debug)
if(EXISTS "${CMAKE_SOURCE_DIR}/.git")
    set(default_build_type Release)
endif()

if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  message(STATUS "Setting build type to '${default_build_type}' as none was specified.")
  set(CMAKE_BUILD_TYPE "${default_build_type}" CACHE
      STRING "Choose the type of build." FORCE)
  # Set the possible values of build type for cmake-gui
  set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS
    "Debug" "Release" "MinSizeRel" "RelWithDebInfo")
endif()

message("build type = ${default_build_type}")

target_compile_options(hexwatershed PUBLIC -std=c++11)

set(INSTALL_DIR ${CMAKE_CURRENT_SOURCE_DIR}/bin)
install(TARGETS hexwatershed RUNTIME DESTINATION ${INSTALL_DIR})

find_package(OpenMP)

if (OPENMP_FOUND)
    set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
    set (CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_EXE_LINKER_FLAGS}")
endif()

set(GDAL_INCLUDE_DIR "/share/apps/gdal/2.3.1/include/")
set(GDAL_LIBRARY "/share/apps/gdal/2.3.1/lib/libgdal.so")
include_directories(${GDAL_INCLUDE_DIR})
find_package(GDAL)

message("GDAL_LIBRARY = ${GDAL_LIBRARY}")

target_link_libraries(hexwatershed ${GDAL_LIBRARY} -std=c++11)


