cmake_minimum_required(VERSION 2.6)

set(CMAKE_SWIG_FLAGS "-Wall;-O")
set(CMAKE_CXX_FLAGS "-std=gnu++11 -Ofast")

if(WIN32)
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -D_hypot=hypot")
  if(CMAKE_SIZEOF_VOID_P EQUAL 8)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -D MS_WIN64")
  endif()
endif()

if(DEFINED ENV{PYRY3D_CXXFLAGS})
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} $ENV{PYRY3D_CXXFLAGS}")
endif()

find_package(PythonLibs 2.5 REQUIRED)
find_package(SWIG 2.0 REQUIRED)

include_directories(${PYTHON_INCLUDE_PATH} ${CMAKE_CURRENT_SOURCE_DIR})

file(GLOB_RECURSE PYRY3D_SRC "*.cpp")
set_property(SOURCE pyry3d_cpp.i PROPERTY CPLUSPLUS ON)

include(${SWIG_USE_FILE})
swig_add_module(pyry3d_cpp python pyry3d_cpp.i ${PYRY3D_SRC})
swig_link_libraries(pyry3d_cpp ${PYTHON_LIBRARY})
