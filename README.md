High-Performance Real-Time CAN Signal Logger
A lightweight, command-line tool designed for high-performance, real-time logging of specific CAN bus signals, even on buses with mixed high- and low-frequency messages. This application connects to a Kvaser CAN hardware interface, decodes messages using a DBC file, and saves the desired signal data to a timestamped JSON Lines file.

It is built for efficiency and reliability, making it ideal for demanding data acquisition tasks where capturing every message is critical.

Features
High-Frequency Data Capture: Utilizes a high-performance C extension to read directly from the hardware driver, ensuring no data loss even with 1ms cycle times.

Parallel Processing: A multi-threaded Python architecture decodes and logs messages in the background without blocking the critical data acquisition thread.

Selective Logging: Parses a user-defined list of signals to log only the data you need, reducing noise and file size.

DBC-Based Decoding: Uses an industry-standard .dbc file to decode raw CAN messages into human-readable physical values.

Robust JSON Output: Saves data in the JSON Lines (.json) format, where each line is a valid JSON object. This format is highly resilient to interruptions and easy to parse.

Configuration-Driven: All settings (CAN parameters, file paths) are managed in a simple config.py file for easy setup.

High-Performance Architecture
To reliably capture data from a high-traffic CAN bus, this logger uses a hybrid C-and-Python architecture. This design leverages the raw performance of C for the time-critical task of data acquisition and the flexibility of Python for data processing and file management.

The system is composed of:

C Reader Thread (fast_reader.c):

A dedicated, high-performance thread written in C that interfaces directly with the Kvaser CANlib SDK.

It runs a tight, blocking loop (canReadWait) that consumes zero CPU while waiting for messages.

Upon message arrival, it instantly reads the data from the hardware buffer and places it onto a thread-safe queue leading back to the Python application.

This C-level implementation completely bypasses Python's Global Interpreter Lock (GIL) and scheduling overhead, preventing hardware buffer overruns and ensuring no messages are dropped.

Python Dispatcher (Main Thread):

The main Python thread waits for raw message data to appear on the queue from the C thread.

It quickly dispatches these messages to the appropriate high- or low-frequency Python processing queues.

Python Processor Threads (data_processor.py):

One or more background threads that pull raw messages from their dedicated queues.

They handle the CPU-intensive work of decoding the CAN messages using the DBC file and formatting the results into Python dictionaries.

Python Logging (in Main Thread):

The main thread also pulls the fully-processed dictionaries from the final log queue.

It handles the slow, blocking I/O task of converting the data to JSON and writing it to the output file.

This separation of concerns ensures that no single part of the system becomes a bottleneck. The time-consuming tasks of decoding and file writing do not block the critical task of reading data from the hardware.

Project Structure
/
├── input/
│   ├── VCU.dbc                 # Your CAN database file
│   └── master_sigList.txt      # The list of signals to monitor
├── output/
│   └── can_log_YYYY-MM-DD.json # Generated log files appear here
├── build/                      # Build artifacts from CMake appear here
├── main.py                     # Main application entry point and orchestrator
├── config.py                   # Hardware and file path settings
├── fast_reader.c               # The C source for the high-performance reader
├── CMakeLists.txt              # The build script for the C extension
├── data_processor.py           # Decodes and formats messages in parallel
├── utils.py                    # Helper function for parsing the signal list
└── pyproject.toml              # Project definition and Python dependencies
Installation and Setup
1. Prerequisites
Python 3.10 or newer.

Kvaser Drivers: You must install the Kvaser CANlib SDK from the official Kvaser website.

MSYS2 & MinGW Compiler: You must install MSYS2 with the UCRT64 toolchain to compile the C extension.

Install MSYS2 from msys2.org.

Open the MSYS2 UCRT64 terminal and install the compiler toolchain and CMake:

Bash

pacman -S mingw-w64-ucrt-x86_64-toolchain mingw-w64-ucrt-x86_64-cmake
2. Create a Virtual Environment
It is highly recommended to use a virtual environment.

Bash

# Create a new virtual environment
python -m venv .venv

# Activate the virtual environment
# On Windows (PowerShell):
.venv\Scripts\Activate.ps1
3. Install Python Dependencies
With the virtual environment activated, install the required packages using uv (or pip):

Bash

# Install the packages listed in pyproject.toml
uv pip install -r requirements.txt
(Note: If pyproject.toml is set up for it, uv pip install -e . can be used, but a requirements.txt is often simpler for projects with C extensions).

4. Configure the Project
Hardware Settings: Open config.py and set your CAN_INTERFACE, CAN_CHANNEL, and CAN_BITRATE.

Input Files: Place your DBC file and signal list (master_sigList.txt) in the input/ directory. Update config.py with the correct filenames.

Build and Run
1. Build the C Extension
This is a one-time step that must be performed from the MSYS2 UCRT64 terminal.

Bash

# 1. Open the MSYS2 UCRT64 terminal and navigate to your project folder
# cd /d/path/to/your/project

# 2. Create a build directory and enter it
mkdir build
cd build

# 3. Configure the project with CMake
cmake .. -G "MinGW Makefiles"

# 4. Compile the extension
cmake --build .
This will create a fast_reader.pyd file inside the build directory.

2. Prepare for Execution
Before running, you must copy the necessary dependency files into your project's root directory.

Copy the Compiled Module: Copy fast_reader.pyd from the build/ directory to your project's root folder.

Copy Kvaser DLL: Copy canlib32.dll from C:\Windows\System32 to your project's root folder. (Note: this is the 64-bit version, despite the name).

Copy Python DLL: Copy libpython3.12.dll (or your specific version) from C:\msys64\ucrt64\bin to your project's root folder.

Your project root should now contain fast_reader.pyd, canlib32.dll, and libpython3.12.dll.

3. Run the Logger
You can now run the application from your regular VS Code terminal (PowerShell or CMD).

Bash

# 1. Make sure your virtual environment is activated
# .venv\Scripts\Activate.ps1

# 2. Run the main script
python main.py
The logger will start and begin saving data to the output/ folder. To stop, press Ctrl+C.

Troubleshooting Journey & Key Findings
This project underwent a rigorous debugging process to solve a critical issue where high-frequency (10ms) signals were not being logged. This section documents the findings for future reference.

The Core Problem: The Python-only multi-threaded application was silently dropping all high-frequency CAN messages due to a combination of Python's Global Interpreter Lock (GIL) and thread scheduling overhead. The hardware's receive buffer was overrunning before the Python reader thread had a chance to empty it.

Critical Insight: A minimal can_sniffer.py script using a simple, blocking bus.recv() loop successfully captured all messages. This proved that the Kvaser hardware, drivers, and the low-level python-can library were all working correctly. The fault lay in the performance limitations of handling high-frequency I/O purely within Python's threading model.

The C-Extension Solution: The only way to guarantee that the hardware buffer is serviced in time was to move the reading logic out of Python and into a compiled C extension. The C thread interfaces directly with the Kvaser canlib.dll, reads messages with a blocking canReadWait() call, and passes the data efficiently to the main Python process via a queue.

Compilation Challenges: The build process for the C module revealed several environment-specific issues:

Compiler Mismatch: The initial C module was built with MSYS2/GCC, but the Python virtual environment used an interpreter built with MSVC, causing a runtime conflict.

Library Pathing: CMake required precise, case-sensitive paths to the Kvaser SDK's Lib/x64 directory.

Misleading Library Name: The 64-bit Kvaser library required for the 64-bit build is counter-intuitively named canlib32.lib.

Final Runtime Dependency: The final ImportError was traced using the Dependencies tool. It revealed that the GCC-compiled fast_reader.pyd had a dependency on the MSYS2 Python library (libpython3.12.dll). The solution was to ship this DLL alongside the .pyd module and the 64-bit Kvaser DLL.