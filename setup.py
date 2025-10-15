# setup.py
from setuptools import setup, Extension
import os

# --- Configuration ---
# Set this to the installation path of your Kvaser CANlib SDK.
# This should be the path with the '(x86)' folder.
KVASER_SDK_PATH = "C:/Program Files (x86)/Kvaser/Canlib"
# --- End Configuration ---

# Verify the path exists
if not os.path.exists(KVASER_SDK_PATH):
    raise FileNotFoundError(f"Kvaser SDK path not found at '{KVASER_SDK_PATH}'. Please update the path in setup.py.")

# Define the C extension module
fast_reader_module = Extension(
    'fast_reader',
    sources=['fast_reader.c'],
    # Point to the Kvaser include directory
    include_dirs=[os.path.join(KVASER_SDK_PATH, 'inc')],
    # Point to the correct 64-bit library directory
    library_dirs=[os.path.join(KVASER_SDK_PATH, 'Lib', 'x64')],
    # Link against the library file (the name is canlib32, even in the x64 folder)
    libraries=['canlib32']
)

setup(
    name='fast_reader_module',
    version='1.0',
    description='A C extension for fast CAN bus reading, built with MSVC.',
    ext_modules=[fast_reader_module]
)