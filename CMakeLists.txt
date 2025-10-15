# CMakeLists.txt

cmake_minimum_required(VERSION 3.12)
project(FastReader C)

# --- Configuration ---
# Set this to the installation path of your Kvaser CANlib SDK.
# This should now match the path you verified.
set(KVASER_SDK_PATH "C:/Program Files (x86)/Kvaser/Canlib" CACHE PATH "Path to Kvaser CANlib SDK")
# --- End Configuration ---

# Verify the Kvaser SDK path exists.
if(NOT EXISTS "${KVASER_SDK_PATH}")
    message(FATAL_ERROR "Kvaser SDK path not found at '${KVASER_SDK_PATH}'. Please verify the path in CMakeLists.txt.")
endif()

# Find Python 3.10 or newer
find_package(Python 3.10 REQUIRED COMPONENTS Interpreter Development)

# --- Select library path based on build architecture ---
# Check if we are compiling for a 64-bit architecture
if(CMAKE_SIZEOF_VOID_P EQUAL 8)
    message(STATUS "Configuring for 64-bit build (UCRT64/MinGW64).")
    # CORRECTED PATH: Using "Lib/x64" to match the actual folder case
    set(KVASER_LIB_DIR "${KVASER_SDK_PATH}/Lib/x64")
    set(KVASER_LIB_NAME "canlib32")
else()
    message(STATUS "Configuring for 32-bit build.")
    # CORRECTED PATH: Using "Lib/win32"
    set(KVASER_LIB_DIR "${KVASER_SDK_PATH}/Lib/win32")
    set(KVASER_LIB_NAME "canlib32")
endif()

# Find the Kvaser CANlib library file using the determined name and path
find_library(CANLIB_LIBRARY
    NAMES ${KVASER_LIB_NAME}
    PATHS "${KVASER_LIB_DIR}"
    DOC "Kvaser CAN library"
)

# If the library is still not found, stop with a helpful error message
if(NOT CANLIB_LIBRARY)
    message(FATAL_ERROR "Kvaser library '${KVASER_LIB_NAME}.lib' not found in '${KVASER_LIB_DIR}'! Please use Windows File Explorer to check that this file exists and correct the path if necessary.")
endif()

# Define the Python module
add_library(fast_reader MODULE fast_reader.c)

# Link the module to the Python and Kvaser libraries
target_include_directories(fast_reader PRIVATE
    ${Python_INCLUDE_DIRS}
    "${KVASER_SDK_PATH}/inc"
)
target_link_libraries(fast_reader PRIVATE
    ${Python_LIBRARIES}
    ${CANLIB_LIBRARY}
)

# Set the correct output file extension for Python on Windows (.pyd)
set_target_properties(fast_reader PROPERTIES
    PREFIX ""
    SUFFIX ".pyd"
)

message(STATUS "Using Python executable: ${Python_EXECUTABLE}")
message(STATUS "Found Kvaser library: ${CANLIB_LIBRARY}")