find_package(Python 3
    REQUIRED COMPONENTS Interpreter Development.Module
    OPTIONAL_COMPONENTS Development.SABIModule
)

if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
    set(CMAKE_BUILD_TYPE Release CACHE STRING "Choose the type of build." FORCE)
    set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS "Debug" "Release" "MinSizeRel" "RelWithDebInfo")
endif()

execute_process(
    COMMAND "${Python_EXECUTABLE}" -m nanobind --cmake_dir
    OUTPUT_STRIP_TRAILING_WHITESPACE OUTPUT_VARIABLE NB_DIR)
list(APPEND CMAKE_PREFIX_PATH "${NB_DIR}")

find_package(nanobind CONFIG REQUIRED)

nanobind_add_module(
    _bochscpu NB_STATIC
    src/bochscpu_callbacks.cpp
    src/bochscpu_cpu.cpp
    src/bochscpu_mem.cpp
    src/bochscpu.cpp
)

target_include_directories(_bochscpu PRIVATE ${CMAKE_SOURCE_DIR} ${CMAKE_SOURCE_DIR}/python/inc)
target_link_directories(_bochscpu PRIVATE ${CMAKE_SOURCE_DIR}/bochscpu/lib/${CMAKE_BUILD_TYPE})
target_link_libraries(_bochscpu PRIVATE)

if(MSVC)
    target_link_libraries(_bochscpu PRIVATE Userenv.lib Bcrypt.lib Ws2_32.lib kernel32.lib ntdll.lib bochscpu_ffi.lib)
else()
    target_link_libraries(_bochscpu PRIVATE bochscpu_ffi)
endif()

if(APPLE)
    target_link_libraries(_bochscpu PRIVATE "-framework CoreFoundation" -Wl -lm)
endif()

install(DIRECTORY bochscpu DESTINATION .)
install(TARGETS _bochscpu LIBRARY DESTINATION bochscpu)

if(MSVC)
    install(FILES $<TARGET_PDB_FILE:_bochscpu> DESTINATION . OPTIONAL)
endif(MSVC)

#
# Build with ASAN if available AND debug build
#
include(CheckCXXCompilerFlag)
CHECK_CXX_COMPILER_FLAG("-fsanitize=address" HAS_ASAN_AVAILABLE)

if(HAS_ASAN_AVAILABLE)
    message(STATUS "Found Address Sanitizer")
    target_compile_definitions(_bochscpu
    PUBLIC
        $<$<CONFIG:Debug>:_DISABLE_VECTOR_ANNOTATION _DISABLE_STRING_ANNOTATION >
    )
    target_compile_options(_bochscpu
    PUBLIC
        $<$<CONFIG:Debug>:-fsanitize=address>
    )
else()
    message(STATUS "Address Sanitizer not found")
endif(HAS_ASAN_AVAILABLE)

