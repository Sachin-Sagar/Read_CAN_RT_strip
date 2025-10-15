High-Performance Real-Time CAN Signal Logger
A lightweight, command-line tool designed for high-performance, real-time logging of specific CAN bus signals, even on buses with mixed high- and low-frequency messages. This application connects to a Kvaser CAN hardware interface, decodes messages using a DBC file, and saves the desired signal data to a timestamped JSON Lines file.

It is built for efficiency and reliability, making it ideal for demanding data acquisition tasks where capturing every message is critical.

Features
High-Frequency Data Capture: Utilizes a parallel processing pipeline to reliably log signals from high-speed (e.g., 10ms cycle time) and low-speed (e.g., 100ms cycle time) messages simultaneously without data loss.

Selective Logging: Parses a user-defined list of signals to log only the data you need, reducing noise and file size.

DBC-Based Decoding: Uses an industry-standard .dbc file to decode raw CAN messages into human-readable physical values.

Robust JSON Output: Saves data in the JSON Lines (.json) format, where each line is a valid JSON object. This format is highly resilient to interruptions and easy to parse.

Timestamped Log Files: Automatically creates a new, uniquely named log file with a timestamp for every session, preventing data from being overwritten.

Configuration-Driven: All settings (CAN parameters, file paths) are managed in a simple config.py file for easy setup.

High-Performance Architecture
To reliably capture data from a mixed-frequency CAN bus, this logger uses a multi-threaded, dual-pipeline architecture. This design prevents high-frequency messages from overwhelming the system and causing data loss.

The system is composed of four main threads:

Dispatcher Thread (can_handler.py):

This is the only thread that communicates directly with the CAN hardware.

It reads all incoming CAN messages from the hardware's buffer.

It instantly checks the ID of each message and dispatches it to one of two dedicated queues: a high-frequency queue or a low-frequency queue.

This ensures that the hardware buffer is read as quickly as possible, preventing overflows.

High-Frequency Processor Thread (data_processor.py):

Runs in parallel, dedicated solely to processing messages from the high-frequency queue.

Its only job is to decode the raw messages, format them into JSON strings, and place the results into a final logging queue.

Low-Frequency Processor Thread (data_processor.py):

A second instance of the same processor class, running in parallel.

It works with the low-frequency queue, decoding and formatting the slower messages.

Main Thread (Logging Thread):

The main application thread has the simplest and fastest job: it pulls fully-formed JSON strings from the final logging queue and writes them directly to the output file.

This separation of concerns ensures that no single part of the system becomes a bottleneck. The time-consuming tasks of decoding and file writing do not block the critical task of reading data from the hardware.

Project Structure
/
├── input/
│   ├── VCU.dbc                 # Your CAN database file
│   └── master_sigList.txt      # The list of signals to monitor
├── output/
│   └── can_log_YYYY-MM-DD.json # Generated log files appear here
├── main.py                     # Main application entry point and orchestrator
├── config.py                   # Hardware and file path settings
├── can_handler.py              # Reads from CAN and dispatches messages
├── data_processor.py           # Decodes and formats messages in parallel
├── utils.py                    # Helper function for parsing the signal list
└── pyproject.toml              # Project definition and dependencies
Installation and Setup
1. Prerequisites
Python 3.10 or newer.

Kvaser Drivers: You must install the Kvaser CANlib SDK from the official Kvaser website for the script to communicate with the hardware.

2. Create a Virtual Environment
It is highly recommended to use a virtual environment. If you are using uv, follow these steps:

Bash

# Create a new virtual environment
uv venv

# Activate the virtual environment
# On Windows (PowerShell):
.venv\Scripts\Activate.ps1
# On macOS/Linux:
source .venv/bin/activate
3. Install Dependencies
With the virtual environment activated, install the required packages:

Bash

# Install the packages listed in pyproject.toml
uv pip install -e .
Configuration
Before running, you must configure the logger for your specific setup.

1. Configure Hardware Settings
Open the config.py file and modify the constants:

CAN_INTERFACE: Set to "kvaser" for Kvaser devices.

CAN_CHANNEL: Set to your device's channel number (usually 0).

CAN_BITRATE: Set to the bitrate of your CAN bus (e.g., 500000).

2. Add Your Input Files
Place your files in the input/ directory:

DBC File: Place your CAN database file in this folder. Update the DBC_FILE variable in config.py to match your filename.

Signal List: Create or edit the master_sigList.txt file.

The master_sigList.txt file must follow a strict CAN_ID,Signal_Name,CycleTime format, with one signal per line. The cycle time must be either 10 or 100 (for 10ms and 100ms respectively).

Example master_sigList.txt:
Plaintext

# This is a comment and will be ignored
# Format: CAN_ID,Signal_Name,CycleTime

# High-frequency signals (10ms)
0x0A0,ETS_VCU_imuProc_xaccel,10
0x0A0,ETS_VCU_imuProc_yaccel,10

# Low-frequency signals (100ms)
0x30F,ETS_VCU_VehSpeed_Act_kmph,100
0x310,ETS_VCU_AccelPedal_Act_perc,100
Usage
Once configured, run the logger from your terminal:

Make sure your virtual environment is activated.

Ensure your Kvaser CAN hardware is connected to the computer and the CAN bus.

Execute the script:

Bash

uv run .\main.py
The logger will start, connect to the CAN bus, and begin saving data to the output/ folder. To stop the logger, press Ctrl+C. The application will shut down gracefully, ensuring all threads are stopped and the log file is closed correctly.

Output Format
The logger generates files in the output/ directory with names like can_log_2025-10-15_12-00-00.json.

The data is stored in the JSON Lines format. Each line in the file is a complete JSON object representing a single, decoded signal value. This format is easy to parse and robust against data corruption.

Example Output:
JSON

{"timestamp": "2025-10-15T12:00:05.123456", "message_id": "0x0A0", "signal": "ETS_VCU_imuProc_xaccel", "value": -0.05}
{"timestamp": "2025-10-15T12:00:05.124890", "message_id": "0x30F", "signal": "ETS_VCU_VehSpeed_Act_kmph", "value": 45.7}
{"timestamp": "2025-10-15T12:00:05.133501", "message_id": "0x0A0", "signal": "ETS_VCU_imuProc_xaccel", "value": -0.06}