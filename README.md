# High-Performance Real-Time CAN Signal Logger

A lightweight, command-line tool designed for high-performance, real-time logging of specific CAN bus signals, even on buses with mixed high- and low-frequency messages. This application connects to a Kvaser CAN hardware interface, decodes messages using a DBC file, and saves the desired signal data to a timestamped JSON Lines file.

It is built for efficiency and reliability, making it ideal for demanding data acquisition tasks where capturing every message is critical.

## Features

-   **High-Frequency Data Capture**: Utilizes a high-performance C extension to read directly from the hardware driver, ensuring no data loss even with 1ms cycle times.
-   **Parallel Processing**: A multi-threaded Python architecture decodes and logs messages in the background without blocking the critical data acquisition thread.
-   **Selective Logging**: Parses a user-defined list of signals to log only the data you need, reducing noise and file size.
-   **DBC-Based Decoding**: Uses an industry-standard `.dbc` file to decode raw CAN messages into human-readable physical values.
-   **Robust JSON Output**: Saves data in the JSON Lines (`.jsonl` or `.json`) format, where each line is a valid JSON object. This format is highly resilient to interruptions and easy to parse.
-   **Configuration-Driven**: All settings (CAN parameters, file paths) are managed in a simple `config.py` file for easy setup.

## High-Performance Architecture

To reliably capture data from a high-traffic CAN bus, this logger uses a hybrid C-and-Python architecture. This design leverages the raw performance of C for the time-critical task of data acquisition and the flexibility of Python for data processing and file management.

The system is composed of:

-   **C Reader Thread (`fast_reader.c`)**: A dedicated, high-performance thread written in C that interfaces directly with the Kvaser CANlib SDK. It runs a tight, blocking loop (`canReadWait`) that consumes zero CPU while waiting for messages. Upon message arrival, it instantly reads the data and places it onto a thread-safe queue leading back to the Python application. This C-level implementation bypasses Python's Global Interpreter Lock (GIL) and scheduling overhead, preventing hardware buffer overruns.

-   **Python Dispatcher (Main Thread)**: The main Python thread waits for raw message data to appear on the queue from the C thread. It quickly dispatches these messages to the appropriate high- or low-frequency Python processing queues.

-   **Python Processor Threads (`data_processor.py`)**: Background threads that handle the CPU-intensive work of decoding CAN messages using the DBC file and formatting the results.

-   **Python Logging (Main Thread)**: The main thread also handles the slow, blocking I/O task of writing the final processed data to the output JSON file.

This separation of concerns ensures that no single part of the system becomes a bottleneck.

## Installation and Setup

### 1. Prerequisites

-   **Python 3.12 or newer**.
-   **Kvaser Drivers**: You must install the Kvaser CANlib SDK from the official Kvaser website.
-   **MSYS2 & MinGW Compiler**: You must install MSYS2 with the UCRT64 toolchain to compile the C extension.
    1.  Install MSYS2 from [msys2.org](https://www.msys2.org/).
    2.  Open the **MSYS2 UCRT64** terminal and install the required compiler toolchain and CMake:
        ```bash
        pacman -S mingw-w64-ucrt-x86_64-toolchain mingw-w64-ucrt-x86_64-cmake
        ```

### 2. Create a Virtual Environment

It is highly recommended to use a virtual environment.

1.  From a standard terminal (PowerShell, CMD), create the environment:
    ```bash
    python -m venv .venv
    ```
2.  Activate the virtual environment:
    ```powershell
    # On Windows (PowerShell):
    .venv\Scripts\Activate.ps1
    ```

### 3. Install Python Dependencies

With the virtual environment activated, install the required packages using `uv` (or `pip`). We install packages directly instead of using `pip install -e .` to avoid trying to compile the C extension with the wrong compiler.

```bash
uv pip install python-can cantools
4. Configure the Project
Hardware Settings: Open config.py and set your CAN_CHANNEL and CAN_BITRATE to match your hardware and network.

Input Files: Place your DBC file (VCU.dbc) and signal list (master_sigList.txt) in the input/ directory. Update config.py with the correct filenames if they differ.

Build and Run
This project requires a two-step process: building the C extension in its specific environment, and then running the Python application from your standard terminal.

1. Build the C Extension (One-Time Step)
This must be performed from the MSYS2 UCRT64 terminal.

Open the MSYS2 UCRT64 terminal and navigate to your project folder.

Create a build directory (or clean the existing one):

Bash

rm -rf build
mkdir build
cd build
Configure the project with CMake, specifying the MinGW generator:

Bash

cmake .. -G "MinGW Makefiles"
Compile the extension:

Bash

cmake --build .
This will create a fast_reader.pyd file inside the build directory.

2. Prepare Runtime Dependencies
Before running, you must copy several essential files into your project's root directory (the same folder as main.py).

Copy the Compiled Module: Copy fast_reader.pyd from the build/ directory.

Copy Kvaser DLL: Copy canlib32.dll from C:\Windows\System32.

Copy Python DLL: Copy libpython3.12.dll (or your specific version) from C:\msys64\ucrt64\bin.

Copy MinGW Runtime DLLs: Copy the following two files from C:\msys64\ucrt64\bin. These are required because our C extension was built with the GCC compiler.

libgcc_s_seh-1.dll

libwinpthread-1.dll

3. Run the Logger
You can now run the application from your regular VS Code terminal (PowerShell or CMD).

Make sure your virtual environment is activated.

Run the main script:

Bash

python main.py
The logger will start and begin saving data to the output/ folder once it detects CAN traffic. To stop, press Ctrl+C.

Troubleshooting Journey & Key Findings
This project underwent a rigorous debugging process. This section documents the key issues and their resolutions.

The Core Problem: A Python-only implementation was silently dropping high-frequency CAN messages due to Python's Global Interpreter Lock (GIL) and scheduling overhead. The hardware's receive buffer was overrunning before the Python reader thread could empty it. This proved a C extension was necessary.

Compilation Challenges:

Compiler Mismatch: The initial build process failed because standard Python tools on Windows default to the MSVC compiler, whereas this project is configured for MinGW GCC. The solution is to build the C extension manually using CMake in the MSYS2 environment.

Library Pathing: CMake requires precise paths to the Kvaser SDK, which are configured in CMakeLists.txt.

Misleading Library Name: The 64-bit Kvaser library required for a 64-bit build is counter-intuitively named canlib32.lib.

Runtime ImportError: DLL load failed:

Symptom: The Python script fails immediately with an error that fast_reader cannot be found or loaded.

Cause: This error indicates that fast_reader.pyd or one of its dependencies is missing. Because it was compiled with MinGW, it depends on the MinGW runtime libraries (libgcc_s_seh-1.dll, libwinpthread-1.dll) and the MSYS2 version of the Python library (libpython3.12.dll).

Solution: Copy all required DLLs into the project's root directory, as detailed in the "Prepare Runtime Dependencies" step. The Dependencies tool (https://github.com/lucasg/Dependencies) is excellent for diagnosing which specific DLL is missing.

Program Runs but Produces No Output:

Symptom: The script starts, prints its initial setup messages, and then appears to hang with no further output and no errors.

Cause: This is the expected behavior when the Kvaser hardware is not connected to a live CAN bus. The C thread is blocked in the canReadWait() function, waiting for messages that will never arrive. The main Python script is similarly blocked, waiting for data from the C thread's queue.

Solution: Connect the hardware to an active CAN bus. If the problem persists, double-check that the CAN_CHANNEL and CAN_BITRATE in config.py are correct for your network. A bitrate mismatch is a common reason for not "hearing" any messages.