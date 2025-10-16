# High-Performance Real-Time CAN Signal Logger

A lightweight, command-line tool designed for high-performance, real-time logging of specific CAN bus signals, even on buses with mixed high- and low-frequency messages. This application connects to a Kvaser CAN hardware interface, decodes messages using a DBC file, and saves the desired signal data to a timestamped JSON Lines file.

It is built for maximum efficiency and reliability, making it ideal for demanding data acquisition tasks where capturing every message from a high-traffic bus is critical.

## Features

-   **Extreme Performance**: Utilizes a multiprocessing, shared-memory pipeline to reliably log signals from high-speed (e.g., 10ms cycle time) and low-speed messages simultaneously without data loss.
-   **Selective Logging**: Parses a user-defined list of signals to log only the data you need, reducing noise and file size.
-   **DBC-Based Decoding**: Uses an industry-standard `.dbc` file to decode raw CAN messages into human-readable physical values.
-   **Robust JSON Output**: Saves data in the JSON Lines (.json) format, where each line is a valid JSON object. This format is highly resilient to interruptions and easy to parse.
-   **Timestamped Log Files**: Automatically creates a new, uniquely named log file with a timestamp for every session.
-   **Configuration-Driven**: All settings (CAN parameters, file paths) are managed in a simple `config.py` file.
-   **Performance Analytics**: Provides a detailed breakdown of the average processing time for each stage of the pipeline upon exit.

## The Troubleshooting Journey: A Deep Dive into High-Performance Python

This project underwent a rigorous debugging process to solve a critical issue where high-frequency (10ms) signals were not being logged. This section documents the evolution of the architecture and the key findings.

#### The Core Problem: Silently Dropped Messages

The application was silently dropping all high-frequency CAN messages. The final report consistently showed these signals as "never logged," even though they were confirmed to be present on the bus using other tools like the included `can_sniffer.py`.

### Architectural Evolution

The final, robust architecture was the result of systematically identifying and eliminating a series of bottlenecks.

#### 1. Initial Architecture: The I/O Bottleneck

-   **Finding**: The initial multi-threaded design failed because the main thread was responsible for both decoding messages and writing them to a file. The slow disk I/O operations blocked the entire pipeline, causing the hardware's input buffer to overflow.
-   **Solution**: We isolated the I/O operations into a dedicated **`LogWriter` thread**. We also implemented **batch writing**—collecting many log entries in memory and writing them to the disk in a single, efficient operation. This dramatically reduced the number of slow `write()` calls.

#### 2. The CPU Bottleneck: `cantools` Decoding

-   **Finding**: With I/O optimized, performance metrics revealed that the `cantools.db.decode_message()` function was too slow for real-time use, taking dozens of milliseconds per message.
-   **Solution**: We **pre-compiled the decoding rules** at startup. A new function, `precompile_decoding_rules`, extracts all necessary bitwise information (start bit, length, scale, offset) from the DBC file ahead of time. The real-time processing loop was rewritten to perform only simple, lightning-fast bitwise math, removing the expensive `cantools` dependency from the hot path.

#### 3. The Final Frontier: Python's GIL and IPC Overhead

-   **Finding**: Even with a highly optimized processing function, the application still dropped messages. The root cause was Python's **Global Interpreter Lock (GIL)**, which prevents multiple threads from executing Python code simultaneously. The CPU-intensive decoding thread was fighting with other threads for CPU time, starving the critical `CANReader` thread.
-   **Solution 1: Multiprocessing**: We replaced the decoding threads with a pool of **worker processes**. Unlike threads, processes have their own GIL and can run in true parallel on different CPU cores, bypassing the GIL bottleneck.

-   **Finding 2: Inter-Process Communication (IPC) Overhead**: The performance report from the multiprocessing version showed that the processing time was still too high (~27ms). The bottleneck had shifted to the enormous overhead of serializing (pickling) Python dictionaries to send them from the worker processes to the logger thread.
-   **Solution 2: Shared Memory Pipeline**: This was the final and most critical optimization. We eliminated the expensive object serialization entirely by using a **`multiprocessing.RawArray`**, a raw block of memory shared between all processes.
    -   The worker processes now decode signals and pack them into a compact binary format directly into this shared memory array.
    -   They then send only a tiny integer (the index of the data's location) to the logger via a high-speed queue.
    -   The `LogWriter` thread reads the index, accesses the shared memory directly, unpacks the binary data, and creates the final dictionary at the last possible moment.

### Final Architecture

This iterative process resulted in a highly efficient, multi-stage pipeline:

`CAN Hardware` -> `CANReader (Thread)` -> `Raw Message Queue` -> `Worker Pool (Processes)` -> `Shared Memory & Index Queue` -> `LogWriter (Thread)` -> `JSON File`

This design ensures that no single part of the system becomes a bottleneck, combining the reliability of direct hardware reading with the true parallelism required for a high-traffic CAN bus.

## Project Structure

/ ├── input/ │ ├── VCU.dbc # Your CAN database file │ └── master_sigList.txt # The list of signals to monitor ├── output/ │ └── can_log_...json # Generated log files appear here ├── main.py # Main application entry point and orchestrator ├── config.py # Hardware and file path settings ├── utils.py # Helper functions (signal parsing, rule pre-compiling) ├── can_handler.py # Reads from CAN and dispatches raw messages ├── data_processor.py # Worker process for high-speed binary decoding ├── log_writer.py # Thread for unpacking from shared memory and writing to disk └── pyproject.toml # Project definition and dependencies


## Installation and Setup

#### 1. Prerequisites
-   Python 3.10 or newer.
-   **Kvaser Drivers**: You must install the Kvaser CANlib SDK from the official Kvaser website.

#### 2. Create a Virtual Environment
```bash
# Create a new virtual environment
python -m venv .venv

# Activate it (Windows PowerShell)
.venv\Scripts\Activate.ps1
# On macOS/Linux:
source .venv/bin/activate
3. Install Dependencies
Bash

# Install the packages listed in pyproject.toml
pip install -e .
Configuration
Open config.py and modify the constants for your setup:

CAN_INTERFACE: Set to "kvaser".

CAN_CHANNEL: Your device's channel number (usually 0).

CAN_BITRATE: The bitrate of your CAN bus (e.g., 500000).

Place your VCU.dbc and master_sigList.txt files in the input/ directory. The signal list format must be CAN_ID,Signal_Name,CycleTime (e.g., 0x123,EngineSpeed,10).

Usage
Ensure your Kvaser hardware is connected and your virtual environment is activated. Execute the script:

Bash

python main.py
The logger will start and begin saving data to the output/ folder. To stop, press Ctrl+C. A performance and signal report will be displayed on exit.