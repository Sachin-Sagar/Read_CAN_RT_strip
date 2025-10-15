# High-Performance Real-Time CAN Signal Logger

A lightweight, command-line tool designed for high-performance, real-time logging of specific CAN bus signals, even on buses with mixed high- and low-frequency messages. This application connects to a Kvaser CAN hardware interface, decodes messages using a DBC file, and saves the desired signal data to a timestamped JSON Lines file.

It is built for efficiency and reliability, making it ideal for demanding data acquisition tasks where capturing every message is critical.

## Features

-   **High-Frequency Data Capture**: Utilizes a parallel processing pipeline to reliably log signals from high-speed (e.g., 10ms cycle time) and low-speed (e.g., 100ms cycle time) messages simultaneously without data loss.
-   **Selective Logging**: Parses a user-defined list of signals to log only the data you need, reducing noise and file size.
-   **DBC-Based Decoding**: Uses an industry-standard `.dbc` file to decode raw CAN messages into human-readable physical values.
-   **Robust JSON Output**: Saves data in the JSON Lines (.json) format, where each line is a valid JSON object. This format is highly resilient to interruptions and easy to parse.
-   **Timestamped Log Files**: Automatically creates a new, uniquely named log file with a timestamp for every session, preventing data from being overwritten.
-   **Configuration-Driven**: All settings (CAN parameters, file paths) are managed in a simple `config.py` file for easy setup.

## High-Performance Architecture

To reliably capture data from a mixed-frequency CAN bus, this logger uses a multi-threaded, dual-pipeline architecture. This design prevents high-frequency messages from overwhelming the system and causing data loss.

The system is composed of four main threads:

1.  **Dispatcher Thread (`can_handler.py`)**:
    -   This is the only thread that communicates directly with the CAN hardware.
    -   It runs a high-performance, non-blocking loop that constantly reads messages from the hardware's buffer.
    -   It instantly checks the ID of each message and dispatches it to one of two dedicated queues: a high-frequency queue or a low-frequency queue.
    -   This ensures that the hardware buffer is read as quickly as possible, preventing overflows.

2.  **High-Frequency Processor Thread (`data_processor.py`)**:
    -   Runs in parallel, dedicated solely to processing messages from the high-frequency queue.
    -   Its only job is to decode the raw messages and place the resulting Python dictionary into a final logging queue.

3.  **Low-Frequency Processor Thread (`data_processor.py`)**:
    -   A second instance of the same processor class, running in parallel.
    -   It works with the low-frequency queue, decoding and formatting the slower messages.

4.  **Main Thread (Logging Thread)**:
    -   The main application thread has the simplest and fastest job: it pulls fully-formed Python dictionaries from the final logging queue, converts them to JSON, and writes them directly to the output file.

This separation of concerns ensures that no single part of the system becomes a bottleneck. The time-consuming tasks of decoding and file writing do not block the critical task of reading data from the hardware.

## Project Structure

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


## Installation and Setup

#### 1. Prerequisites
-   Python 3.10 or newer.
-   **Kvaser Drivers**: You must install the Kvaser CANlib SDK from the official Kvaser website for the script to communicate with the hardware.

#### 2. Create a Virtual Environment
It is highly recommended to use a virtual environment.

```bash
# Create a new virtual environment
python -m venv .venv

# Activate the virtual environment
# On Windows (PowerShell):
.venv\Scripts\Activate.ps1
# On macOS/Linux:
source .venv/bin/activate
3. Install Dependencies
With the virtual environment activated, install the required packages:

Bash

# Install the packages listed in pyproject.toml
pip install -e .
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

Signal List: Create or edit the master_sigList.txt file. The format must be CAN_ID,Signal_Name,CycleTime, with one signal per line. The cycle time must be either 10 or 100.

Example master_sigList.txt:

Plaintext

# Format: CAN_ID,Signal_Name,CycleTime

# High-frequency signals (10ms)
0x0A0,ETS_VCU_imuProc_xaccel,10
0x0A0,ETS_VCU_imuProc_yaccel,10

# Low-frequency signals (100ms)
0x310,ETS_VCU_AccelPedal_Act_perc,100
Usage
Once configured, run the logger from your terminal.

Make sure your virtual environment is activated.

Ensure your Kvaser CAN hardware is connected.

Execute the script:

Bash

python main.py
The logger will start and begin saving data to the output/ folder. To stop, press Ctrl+C.

Troubleshooting Journey & Key Findings
This project underwent a rigorous debugging process to solve a critical issue where high-frequency (10ms) signals were not being logged, while low-frequency (100ms) signals were captured perfectly. This section documents the findings for future reference.

The Core Problem
The application was silently dropping all high-frequency CAN messages. The final report consistently showed these signals as "never logged," even though they were confirmed to be present on the bus using other tools.

Diagnostic Steps and Evolution of the Solution
Initial Architecture (Blocking Reader): The first design used a simple bus.recv(timeout) call in a single thread. This was not performant enough and dropped messages immediately.

First Multi-threaded Approach (can.Notifier): To improve performance, the architecture was changed to use python-can's built-in Notifier and Listener system. The theory was that this would provide a highly-optimized, background thread for reading messages.

Result: This approach still failed to capture any high-frequency messages. The on_message_received callback in the listener was never being triggered for the 10ms message IDs.

Isolating the Fault (can_sniffer.py): To determine if the problem was in our application logic or the python-can library itself, a minimal diagnostic script was created. This "sniffer" used a direct, simple bus.recv() loop.

Result: The sniffer script successfully captured all messages, including the high-frequency ones. This was the critical breakthrough. It proved that the Kvaser hardware, the drivers, and the low-level python-can interface were all working correctly.

The Final Diagnosis and Solution
The diagnostic test proved that on this specific combination of hardware (Kvaser), drivers, and Python environment, the can.Notifier mechanism was not reliable for very high-frequency bus traffic. The messages were being dropped at a low level before they could be dispatched to the listener.

The solution was to revert to a manual dispatcher thread but to architect it for maximum performance, mirroring the successful approach of the sniffer script.

The final, robust architecture in can_handler.py uses a threading.Thread that runs a while loop with a non-blocking bus.recv(timeout=0) call. A tiny time.sleep(0.001) is used when the buffer is empty to prevent the loop from consuming 100% CPU. This approach ensures the hardware's receive buffer is serviced as fast as possible, combining the reliability of direct reading with the performance required for a high-traffic CAN bus.