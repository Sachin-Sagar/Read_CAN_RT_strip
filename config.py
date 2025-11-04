# config.py

import platform

# This file contains all the configuration settings for the CAN logger.
# Modify the values here to match your setup.

# --- CAN Hardware Settings ---

# Select the CAN interpreter. Options: 'peak', 'kvaser'
# This will be updated dynamically by the user's choice in main.py.
CAN_INTERPRETER = "peak"

CAN_BITRATE = 500000
OS_SYSTEM = platform.system()

# Default values, to be overridden by the logic below
CAN_INTERFACE = None
CAN_CHANNEL = None

if CAN_INTERPRETER == "peak":
    if OS_SYSTEM == "Windows":
        CAN_INTERFACE = "pcan"
        CAN_CHANNEL = "PCAN_USBBUS1"
    elif OS_SYSTEM == "Linux":
        CAN_INTERFACE = "socketcan"
        CAN_CHANNEL = "can0"
elif CAN_INTERPRETER == "kvaser":
    if OS_SYSTEM == "Windows":
        # On Windows, Kvaser uses the canlib library directly
        CAN_INTERFACE = "kvaser"
        CAN_CHANNEL = 0 # Typically the first channel is 0
    elif OS_SYSTEM == "Linux":
        # On Linux, Kvaser also uses the canlib library
        CAN_INTERFACE = "kvaser"
        CAN_CHANNEL = 0 # Typically the first channel is 0
else:
    print(f"Error: Unknown CAN_INTERPRETER: {CAN_INTERPRETER}")
    # Exit or handle the error as appropriate
    exit()

if CAN_INTERFACE is None:
    print(f"Error: Unsupported OS '{OS_SYSTEM}' for CAN_INTERPRETER '{CAN_INTERPRETER}'")
    # Exit or handle the error as appropriate
    exit()


# --- General Settings ---
# Set to True to enable verbose debug printing, False to disable.
DEBUG_PRINTING = False


# --- File and Directory Paths ---
# The script will look for the input files in this directory.
# The path is relative to the project's root folder.
INPUT_DIRECTORY = "input"

# The script will save the output log file in this directory.
# This directory will be created automatically if it doesn't exist.
OUTPUT_DIRECTORY = "output"

# The name of your DBC file, located in the INPUT_DIRECTORY.
DBC_FILE = "VCU.dbc"

# The name of your signal list file, located in the INPUT_DIRECTORY.
# This file should contain one signal per line in the format:
# CAN_ID,Signal_Name
# Example: 0x123,EngineSpeed
SIGNAL_LIST_FILE = "master_sigList.txt"
