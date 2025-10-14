Real-Time CAN Signal Logger
A lightweight, command-line tool designed for high-performance, real-time logging of specific CAN bus signals. This application connects to a Kvaser CAN hardware interface, decodes messages using a DBC file, and saves the desired signal data to a timestamped JSON Lines file.

It is built to be simple, efficient, and easily configurable, making it ideal for dedicated data acquisition tasks without the overhead of a graphical user interface.

Features
Real-Time Monitoring: Directly connects to a Kvaser CAN interface for live data capture.

Selective Logging: Parses a user-defined list of signals to log only the data you need, reducing noise and file size.

DBC-Based Decoding: Uses an industry-standard .dbc file to decode raw CAN messages into human-readable physical values.

Robust JSON Output: Saves data in the JSON Lines (.json) format, where each line is a valid JSON object. This format is highly resilient to interruptions and easy to parse.

Timestamped Log Files: Automatically creates a new, uniquely named log file with a timestamp for every session, preventing data from being overwritten.

Configuration-Driven: All settings (CAN parameters, file paths) are managed in a simple config.py file for easy setup.

Lightweight & Efficient: Stripped down to essential packages (python-can, cantools) for minimal overhead and reliable performance.

Project Structure
The project is organized into a clean and understandable structure:

can_logger/
├── input/
│   ├── your_database.dbc
│   └── signals_to_monitor.txt
├── output/
│   └── can_log_YYYY-MM-DD_HH-MM-SS.json
├── main.py
├── config.py
├── can_handler.py
├── utils.py
└── pyproject.toml
input/: Place your configuration files here.

your_database.dbc: Your CAN database file.

signals_to_monitor.txt: The list of signals you wish to log.

output/: All generated log files will be saved in this directory.

main.py: The main entry point of the application.

config.py: A centralized file for all user-configurable settings.

can_handler.py: Manages the connection and real-time reading from the CAN hardware.

utils.py: Contains helper functions for parsing input files.

pyproject.toml: Defines project dependencies and metadata.

Installation and Setup
Follow these steps to get the logger running.

1. Prerequisites
Python 3.8 or newer.

Kvaser Drivers: You must install the Kvaser CANlib SDK from the official Kvaser website for the script to communicate with the hardware.

2. Create a Virtual Environment (Recommended)
It is highly recommended to use a virtual environment to manage project dependencies. If you are using uv, follow these steps:

Bash

# Create a new virtual environment in a .venv directory
uv venv

# Activate the virtual environment
# On Windows (Command Prompt/PowerShell):
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
3. Install Dependencies
With your virtual environment activated, install the required packages using uv:

Bash

# Install the packages listed in pyproject.toml
uv pip install -e .
Configuration
Before running the logger, you must configure it to match your specific setup.

1. Configure Hardware Settings
Open the config.py file and modify the following constants:

CAN_INTERFACE: Set to "kvaser" for Kvaser devices.

CAN_CHANNEL: Set to your device's channel number (usually 0).

CAN_BITRATE: Set to the bitrate of your CAN bus (e.g., 500000).

2. Add Your Input Files
Place your files in the input/ directory:

DBC File: Rename your CAN database file to your_database.dbc or update the DBC_FILE variable in config.py to match your filename.

Signal List: Create or edit the signals_to_monitor.txt file.

The signals_to_monitor.txt file must follow a strict CAN_ID,Signal_Name format, with one signal per line.

Example signals_to_monitor.txt:

Plaintext

# This is a comment and will be ignored
# Format: CAN_ID,Signal_Name

0x18F00403,EngineSpeed
0x18F00403,CalculatedEngineLoad
0x18FEEF00,WheelBasedVehicleSpeed
0xCF00300,EngineOilPressure
Usage
Once configured, run the logger from your terminal:

Make sure your virtual environment is activated.

Ensure your Kvaser CAN hardware is connected.

Execute the main.py script:

Bash

python main.py
The logger will start, connect to the CAN bus, and begin saving data to the output folder. To stop the logger, press Ctrl+C. The application will shut down gracefully, ensuring the log file is closed correctly.

Output Format
The logger generates files in the output/ directory with names like can_log_2025-10-14_18-30-00.json.

The data is stored in the JSON Lines format. Each line in the file is a complete JSON object representing a single, decoded signal value. This format is easy to parse and robust against data corruption.

Example output line:

JSON

{"timestamp": "2025-10-14T18:30:05.123456", "message_id": "0x18F00403", "signal": "EngineSpeed", "value": 2450.5}
{"timestamp": "2025-10-14T18:30:05.223456", "message_id": "0x18FEEF00", "signal": "WheelBasedVehicleSpeed", "value": 62.1}