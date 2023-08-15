cmake_minimum_required(VERSION 3.20)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED True)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_INTERPROCEDURAL_OPTIMIZATION True)

project(
    PyBochsCPU
    LANGUAGES CXX
    VERSION 0.1.0
    DESCRIPTION "Python bindings for BochsCPU"
    HOMEPAGE_URL https://github.com/hugsy/Py-BochsCPU
)

set(PROJECT_AUTHOR hugsy)
set(PROJECT_LICENSE MIT)

set(CXX_STANDARD 20)

add_subdirectory(python)
