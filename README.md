High-Performance Real-Time CAN Signal Logger
This is a lightweight, command-line tool designed for high-performance, real-time logging of specific CAN bus signals. It connects to a Kvaser CAN hardware interface, decodes messages using a DBC file, and saves the desired signal data to a timestamped JSON Lines file. It is built for maximum efficiency and reliability by utilizing a multiprocessing, shared-memory pipeline to reliably log signals from high-speed (e.g., 10ms cycle time) and low-speed messages simultaneously without data loss.

Features
Extreme Performance: Utilizes a multiprocessing, shared-memory pipeline to reliably log signals from high-speed (e.g., 10ms cycle time) and low-speed messages simultaneously without data loss.

Selective Logging: Parses a user-defined list of signals to log only the data you need, reducing noise and file size.

DBC-Based Decoding: Uses an industry-standard .dbc file to decode raw CAN messages into human-readable physical values.

Robust JSON Output: Saves data in the JSON Lines (.json) format, where each line is a valid JSON object. This format is highly resilient to interruptions and easy to parse.

Timestamped Log Files: Automatically creates a new, uniquely named log file with a timestamp for every session.

Configuration-Driven: All settings (CAN parameters, file paths, debug flags) are managed in a simple config.py file.

Performance Analytics: Provides a detailed breakdown of the average processing time for each stage of the pipeline upon exit.

System Architecture
The application's architecture is designed to isolate I/O, maximize CPU usage, and minimize data transfer overhead. This multi-stage pipeline ensures that no single part of the system becomes a bottleneck.

The flow of data is as follows:

CAN Hardware -> CANReader (Thread): A dedicated thread in can_handler.py continuously polls the Kvaser hardware for new messages with a minimal timeout to prevent the hardware's internal buffer from overflowing.

CANReader -> Raw Message Queue: The CANReader places raw can.Message objects into a high-speed multiprocessing.Queue.

Raw Message Queue -> Worker Pool (Processes): A pool of worker processes (one less than the number of CPU cores) fetches raw messages from the queue. Each process runs in parallel on a different CPU core.

Worker Pool -> Shared Memory & Index Queue:

Inside data_processor.py, each worker uses pre-compiled decoding rules to perform fast, bitwise math to extract the physical value of the signal.

The worker then packs the timestamp, CAN ID, signal name, and physical value into a compact binary format directly into a shared multiprocessing.RawArray.

Finally, the worker places only a small integer (the index of the slot in the shared memory array) into a separate index queue.

Index Queue -> LogWriter (Thread): A dedicated thread in log_writer.py retrieves the integer index from the queue.

LogWriter -> JSON File:

The LogWriter uses the index to directly access the shared memory, unpack the binary data, and format it into a JSON string.

To maximize I/O efficiency, it collects log entries into batches before writing them to the disk in a single, efficient operation.

This design combines the reliability of direct hardware reading with the true parallelism required for a high-traffic CAN bus.

Project Structure
/
├── input/
│   ├── VCU.dbc              # Your CAN database file
│   └── master_sigList.txt   # The list of signals to monitor
├── output/
│   └── can_log_...json      # Generated log files appear here
├── main.py                  # Main application entry point and orchestrator
├── config.py                # Hardware and file path settings
├── utils.py                 # Helper functions (signal parsing, rule pre-compiling)
├── can_handler.py           # Reads from CAN and dispatches raw messages
├── data_processor.py        # Worker process for high-speed binary decoding
├── log_writer.py            # Thread for unpacking from shared memory and writing to disk
└── pyproject.toml           # Project definition and dependencies
Installation and Setup
1. Prerequisites
Python 3.10 or newer.

Kvaser Drivers: You must install the Kvaser CANlib SDK from the official Kvaser website for the python-can library to detect your hardware.

2. Create a Virtual Environment
It is highly recommended to use a virtual environment to manage dependencies.

Bash

# Create a new virtual environment
python -m venv .venv

# Activate it (Windows PowerShell)
.venv\Scripts\Activate.ps1

# On macOS/Linux:
# source .venv/bin/activate
3. Install Dependencies
The project dependencies are managed by pyproject.toml and include python-can and cantools.

Bash

# Install the packages listed in pyproject.toml
pip install -e .
Configuration
All settings are managed in the config.py file.

Hardware Settings:

CAN_INTERFACE: Set to "kvaser" for Kvaser hardware.

CAN_CHANNEL: Your device's channel number (usually 0).

CAN_BITRATE: The bitrate of your CAN bus (e.g., 500000).

General Settings:

DEBUG_PRINTING: Set to True to enable verbose diagnostic messages, or False for silent operation.

File Paths and Input Files:

Place your DBC file (e.g., VCU.dbc) and your signal list file (master_sigList.txt) in the input/ directory.

The signal list must be a text file with each line in the format: CAN_ID,Signal_Name,CycleTime.

Example master_sigList.txt:

0x09A,ETS_VCU_Gear_Engaged_St_enum,10
0x310,ETS_VCU_AccelPedal_Act_perc,100
Usage
Ensure your Kvaser hardware is connected and your virtual environment is activated. Execute the script from the project root directory:

Bash

python main.py
The logger will start and begin saving data to the output/ folder. To stop, press Ctrl+C. A performance and signal report will be displayed on exit.