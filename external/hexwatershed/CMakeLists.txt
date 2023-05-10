cmake_minimum_required(VERSION 3.10)
project(hexwatershed CXX)

set(CMAKE_CXX_STANDARD 11)
message("CMAKE_CURRENT_SOURCE_DIR is = ${CMAKE_CURRENT_SOURCE_DIR}")
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/../src)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_VERBOSE_MAKEFILE ON)

set(hexwatershed_srcs 
        ${CMAKE_CURRENT_SOURCE_DIR}/../src/compset/compset_depression.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/../src/compset/compset_direction.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/../src/compset/compset_initialize.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/../src/compset/compset_run.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/../src/compset/compset_save.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/../src/compset/compset_stream.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/../src/compset/compset.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/../src/compset/compset.h
        ${CMAKE_CURRENT_SOURCE_DIR}/../src/domain/domain_read.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/../src/domain/domain.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/../src/domain/domain.h
        ${CMAKE_CURRENT_SOURCE_DIR}/../src/json/cell.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/../src/json/cell.h
        ${CMAKE_CURRENT_SOURCE_DIR}/../src/json/mesh.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/../src/json/mesh.h        
        ${CMAKE_CURRENT_SOURCE_DIR}/../src/json/basin.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/../src/json/basin.h
        ${CMAKE_CURRENT_SOURCE_DIR}/../src/json/multibasin.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/../src/json/multibasin.h   
        ${CMAKE_CURRENT_SOURCE_DIR}/../src/json/JSONBase.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/../src/json/JSONBase.h     
        ${CMAKE_CURRENT_SOURCE_DIR}/../src/conversion.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/../src/conversion.h
        ${CMAKE_CURRENT_SOURCE_DIR}/../src/data.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/../src/data.h         
        ${CMAKE_CURRENT_SOURCE_DIR}/../src/edge.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/../src/edge.h   
        ${CMAKE_CURRENT_SOURCE_DIR}/../src/flowline.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/../src/flowline.h   
        ${CMAKE_CURRENT_SOURCE_DIR}/../src/geology.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/../src/geology.h
        ${CMAKE_CURRENT_SOURCE_DIR}/../src/global.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/../src/global.h
        ${CMAKE_CURRENT_SOURCE_DIR}/../src/hexagon.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/../src/hexagon.h
        ${CMAKE_CURRENT_SOURCE_DIR}/../src/main.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/../src/parameter.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/../src/parameter.h
        ${CMAKE_CURRENT_SOURCE_DIR}/../src/segment.cpp        
        ${CMAKE_CURRENT_SOURCE_DIR}/../src/segment.h
        ${CMAKE_CURRENT_SOURCE_DIR}/../src/subbasin.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/../src/subbasin.h
        ${CMAKE_CURRENT_SOURCE_DIR}/../src/system.cpp        
        ${CMAKE_CURRENT_SOURCE_DIR}/../src/system.h
        ${CMAKE_CURRENT_SOURCE_DIR}/../src/json/vertex.cpp        
        ${CMAKE_CURRENT_SOURCE_DIR}/../src/json/vertex.h
        ${CMAKE_CURRENT_SOURCE_DIR}/../src/watershed.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/../src/watershed.h       
        )

add_executable(hexwatershed ${hexwatershed_srcs})

set(default_build_type Debug)
if(EXISTS "${CMAKE_SOURCE_DIR}/../.git")
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

set(INSTALL_DIR ${CMAKE_CURRENT_SOURCE_DIR}/../bin)
install(TARGETS hexwatershed RUNTIME DESTINATION ${INSTALL_DIR})

find_package(OpenMP)

if (OPENMP_FOUND)
    set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
    set (CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_EXE_LINKER_FLAGS}")
endif()

set(RAPIDJSON_NCLUDE_DIR ${CMAKE_CURRENT_SOURCE_DIR}external/rapidjson)

include_directories(${RAPIDJSON_NCLUDE_DIR})

target_link_libraries(hexwatershed  -std=c++11)
