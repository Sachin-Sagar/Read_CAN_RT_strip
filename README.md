# High-Performance Real-Time CAN Signal Logger

This is a lightweight, command-line tool designed for high-performance, real-time logging of specific CAN bus signals. It connects to a CAN hardware interface, decodes messages using a DBC file, and saves the desired signal data to a timestamped JSON Lines file. It is built for maximum efficiency by utilizing a multiprocessing, shared-memory pipeline to reliably log signals without data loss.

## Features

* **Extreme Performance:** Utilizes a multiprocessing, shared-memory pipeline to reliably log signals from high-speed (e.g., 10ms cycle time) and low-speed messages simultaneously without data loss.
* **Cross-Platform:** Automatically detects the host operating system (Windows or Linux) and selects the correct CAN backend (`pcan` or `socketcan`).
* **Selective Logging:** Parses a user-defined list of signals to log only the data you need, reducing noise and file size.
* **DBC-Based Decoding:** Uses an industry-standard .dbc file to decode raw CAN messages into human-readable physical values.
* **Robust JSON Output:** Saves data in the JSON Lines (.json) format, where each line is a valid JSON object.
* **Performance Analytics:** Provides a detailed breakdown of the average processing time for each stage of the pipeline upon exit.

## System Architecture

The application's architecture is designed to isolate I/O, maximize CPU usage, and minimize data transfer overhead.

1.  **CAN Hardware -> CANReader (Thread)**: A dedicated thread (`can_handler.py`) continuously polls the hardware for new messages.
2.  **CANReader -> Raw Message Queue**: Raw `can.Message` objects are placed into a `multiprocessing.Queue`.
3.  **Raw Message Queue -> Worker Pool (Processes)**: A pool of worker processes (`data_processor.py`) fetches messages, decodes them using pre-compiled rules, and packs the results into shared memory.
4.  **Worker Pool -> Shared Memory & Index Queue**: Workers place only a small integer index (pointing to the data in a `multiprocessing.RawArray`) into a separate queue.
5.  **Index Queue -> LogWriter (Thread)**: A final thread (`log_writer.py`) retrieves the indices, unpacks the data from shared memory, and writes it to the JSON file in batches.



## Project Structure

/ ├── input/ │ ├── VCU.dbc # Your CAN database file │ └── master_sigList.txt # The list of signals to monitor ├── output/ │ └── can_log_...json # Generated log files appear here ├── main.py # Main application entry point ├── config.py # Hardware and file path settings ├── utils.py # Signal parsing and rule pre-compiling ├── can_handler.py # Reads from CAN and dispatches messages ├── data_processor.py # Worker process for high-speed decoding ├── log_writer.py # Thread for writing to disk └── pyproject.toml # Project definition and dependencies


## Installation and Setup

### 1. Prerequisites

* Python 3.10 or newer.
* **Hardware:** A **PCAN-USB** adapter is recommended.
* **Drivers (Windows):** Install the [PCAN-Basic drivers](https://www.peak-system.com/PCAN-Basic.239.0.html?&L=1) for the `python-can` library to detect your hardware.
* **Drivers (Linux):** Install `can-utils` for system-level CAN management.
    ```bash
    sudo apt update
    sudo apt install can-utils
    ```

### 2. Create a Virtual Environment

It is highly recommended to use a virtual environment.

```bash
# Create a new virtual environment
python -m venv .venv

# Activate it (Windows PowerShell)
.venv\Scripts\Activate.ps1

# On macOS/Linux:
source .venv/bin/activate

3. Install Dependencies

The project dependencies are managed by pyproject.toml.
Bash

# Install the packages listed in pyproject.toml
pip install -e .

Configuration

Hardware (Automatic)

The script now auto-detects your OS and configures the CAN hardware settings.

    On Windows: It selects the pcan interface.

    On Linux: It selects the socketcan interface with channel can0.

If you need to change the bitrate or PCAN channel name, you can edit the config.py file directly.

Files and Signals

    Place your DBC file (e.g., VCU.dbc) in the input/ directory.

    Place your signal list (master_sigList.txt) in the input/ directory.

    The signal list must be a text file with each line in the format: CAN_ID,Signal_Name,CycleTime.

Example master_sigList.txt:

0x09A,ETS_VCU_Gear_Engaged_St_enum,10
0x310,ETS_VCU_AccelPedal_Act_perc,100

Usage

Ensure your PCAN hardware is connected and your virtual environment is activated.

On Linux (Raspberry Pi)

You must bring the CAN interface up manually before running the script.

    Bring the interface up:
    Bash

sudo ip link set can0 up type can bitrate 500000

Run the logger:
Bash

    python main.py

On Windows

    Run the logger:
    Bash

    python main.py

The logger will start and begin saving data to the output/ folder. To stop, press Ctrl+C. A performance and signal report will be displayed on exit.

Troubleshooting (Linux / SocketCAN)

    Error: OSError: [Errno 100] Network is down

        Cause: You did not bring the can0 interface up before running the script.

        Solution: Run sudo ip link set can0 up type can bitrate 500000 (or your required bitrate).

    Error: Cannot find device "can0"

        Cause: The kernel driver for your PCAN adapter (peak_usb) is not loaded or the hardware is not detected.

        Solution: Unplug and replug the adapter. Run lsmod | grep peak_usb to verify the driver is loaded.

    Error: TypeError: expected str, bytes or os.PathLike object, not int

        Cause: Your config.py is misconfigured. CAN_CHANNEL is set to an integer (like 0) instead of a string (like "can0").

        Solution: Edit config.py and ensure CAN_CHANNEL = "can0" for the Linux/SocketCAN configuration.


---

### **Updated `GEMINI.md`**

Here is the updated `GEMINI.md`. This file now tells the complete story of our debugging and migration process.

```markdown
# GEMINI.md

## Project Overview

This project is a high-performance, real-time CAN signal logger. It's a command-line tool written in Python that connects to a CAN hardware interface, decodes messages using a DBC file, and saves specific signal data to a timestamped JSON Lines file.

The architecture is designed for high performance and reliability, using a multiprocessing, shared-memory pipeline to log signals from high-speed and low-speed messages simultaneously without data loss.

## Building and Running (PCAN / SocketCAN)

### 1. Prerequisites

* Python 3.10 or newer.
* **Hardware:** A **PCAN-USB** adapter.
* **Drivers (Windows):** Install the [PCAN-Basic drivers](https://www.peak-system.com/PCAN-Basic.239.0.html?&L=1).
* **Drivers (Linux):** Install `can-utils` (`sudo apt install can-utils`).

### 2. Setup

It is recommended to use a virtual environment.

```bash
# Create a new virtual environment
python -m venv .venv

# Activate it (Windows PowerShell)
.venv\Scripts\Activate.ps1

# On macOS/Linux:
source .venv/bin/activate

3. Install Dependencies

The project dependencies are managed by pyproject.toml.
Bash

# Install the packages listed in pyproject.toml
pip install -e .

4. Configuration

All hardware settings are now auto-configured in config.py and can_sniffer.py.

    The script detects the OS (Windows or Linux).

    On Windows, it uses the pcan interface.

    On Linux, it uses the socketcan interface with channel "can0".

Place your DBC file and signal list file in the input/ directory.

5. Running the Application

On Linux (e.g., Raspberry Pi)

You must bring the CAN interface up manually first.
Bash

sudo ip link set can0 up type can bitrate 500000
python main.py

On Windows

Bash

python main.py

The logger will start and save data to the output/ folder. To stop, press Ctrl+C.

The Debugging Journey: From Kvaser Failure to PCAN Success

This project was originally developed for Kvaser hardware, but significant issues were encountered when migrating to a Linux (Raspberry Pi) environment. This document outlines the debugging process that led to a successful hardware migration.

Part 1: Failure of the Kvaser Proprietary Driver

The initial attempt to run the Kvaser-configured application on a Raspberry Pi failed, even after the Kvaser linuxcan drivers (mhydra v8.50.312) and canlib (v5.50) were installed.

    Initial Error: The application immediately crashed with FATAL ERROR: Function canIoCtl failed - Error in parameter [Error Code -1].

    Core Diagnosis: We ran two key tests:

        Kvaser's listChannels Tool: This C-based example program succeeded, proving the hardware, kernel driver (mhydra), and canlib library were installed correctly.

        Minimal Python Script: A simple can.interface.Bus(...) script failed with the same canIoCtl error.

    Conclusion: The problem was not the application code or the drivers themselves, but a low-level incompatibility between the python-can (v4.6.1) library's kvaser backend and the specific canlib version on the Pi.

Part 2: Successful Migration to PCAN/SocketCAN

With the Kvaser proprietary stack deemed unworkable, we migrated to the standard Linux SocketCAN interface.

    Hypothesis 1: Use Kvaser with SocketCAN.

        Test: We checked if the standard kvaser_usb SocketCAN driver was available.

        Result: modprobe: FATAL: Module kvaser_usb not found. This path was a dead end. The Pi's kernel did not include this driver.

    Hypothesis 2: Change hardware to one with known, working SocketCAN drivers.

        Test: We checked if the standard driver for PCAN (peak_usb) was available.

        Result: lsmod | grep peak_usb succeeded, showing the driver was already loaded in the kernel. This confirmed PCAN was a viable path.

    Implementation: The code was modified to support PCAN.

        config.py and can_sniffer.py were updated to use platform.system() to auto-detect the OS.

        Windows: Uses CAN_INTERFACE = "pcan".

        Linux: Uses CAN_INTERFACE = "socketcan".

    Final Errors & Solutions:

        Error: TypeError: expected str, bytes or os.PathLike object, not int

            Fix: Changed CAN_CHANNEL in config.py from 0 to "can0" for the Linux/SocketCAN configuration.

        Error: OSError: [Errno 100] Network is down

            Fix: Added a mandatory step for Linux users to run sudo ip link set can0 up type can bitrate 500000 before starting the script.

Final Conclusion

The migration was 100% successful. The application is now fully functional on both Windows and Raspberry Pi (Linux) using PCAN hardware. The original driver incompatibility was completely bypassed by moving to the stable, kernel-integrated SocketCAN interface (peak_usb).

Development Conventions

    The project uses a modular structure, with clear separation of concerns between the different components of the pipeline.

    Configuration is centralized in config.py.

    The main.py script orchestrates the entire pipeline.

    The project uses multiprocessing to take advantage of multiple CPU cores.

    Shared memory is used to efficiently transfer data between processes.

    The pyproject.toml file defines the project dependencies.