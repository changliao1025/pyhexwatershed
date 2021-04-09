cmake_minimum_required(VERSION 3.10)
project(hexwatershed CXX)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_VERBOSE_MAKEFILE ON)

Include_directories(../hexwatershed/src)

file(GLOB hexwatershed_srcs ../hexwatershed/src/conversion.cpp
        ../hexwatershed/src/conversion.h
        ../hexwatershed/src/data.cpp
        ../hexwatershed/src/data.h
        ../hexwatershed/src/depression.cpp
        ../hexwatershed/src/depression.h
        ../hexwatershed/src/domain.cpp
        ../hexwatershed/src/domain.h
        ../hexwatershed/src/global.cpp
        ../hexwatershed/src/global.h
        ../hexwatershed/src/hexagon.cpp
        ../hexwatershed/src/hexagon.h
        ../hexwatershed/src/main.cpp
        ../hexwatershed/src/segment.cpp
        ../hexwatershed/src/segment.h
        ../hexwatershed/src/system.cpp
        ../hexwatershed/src/system.h
        ../hexwatershed/src/watershed.cpp
        ../hexwatershed/src/watershed.h)

add_executable(hexwatershed ${hexwatershed_srcs})

set(default_build_type Debug)
if(EXISTS "${CMAKE_SOURCE_DIR}/../hexwatershed/.git")
    set(default_build_type Debug)
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

target_compile_options(hexwatershed PUBLIC)


set(INSTALL_DIR ${CMAKE_CURRENT_SOURCE_DIR}/../hexwatershed/bin)
install(TARGETS hexwatershed RUNTIME DESTINATION ${INSTALL_DIR})

find_package(OpenMP)

if (OPENMP_FOUND)
    set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
    set (CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_EXE_LINKER_FLAGS}")
endif()

set(GDAL_INCLUDE_DIR "/Library/Frameworks/GDAL.framework/Headers")
set(GDAL_LIBRARY "/Library/Frameworks/GDAL.framework/unix/lib/libgdal.dylib")
include_directories(${GDAL_INCLUDE_DIR})
find_package(GDAL)

message("GDAL_LIBRARY = ${GDAL_LIBRARY}")

target_link_libraries(hexwatershed ${GDAL_LIBRARY} -std=c++11)
