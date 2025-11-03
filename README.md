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

```
/
├── input/
│   ├── VCU.dbc             # Your CAN database file
│   └── master_sigList.txt  # The list of signals to monitor
├── output/
│   └── can_log_...json     # Generated log files appear here
├── main.py                 # Main application entry point
├── config.py               # Hardware and file path settings
├── utils.py                # Signal parsing and rule pre-compiling
├── can_handler.py          # Reads from CAN and dispatches messages
├── data_processor.py       # Worker process for high-speed decoding
├── log_writer.py           # Thread for writing to disk
└── pyproject.toml          # Project definition and dependencies
```

## Installation and Setup

### 1. Prerequisites

*   Python 3.10 or newer.
*   **Hardware:** A **PCAN-USB** adapter is recommended.
*   **Drivers (Windows):** Install the [PCAN-Basic drivers](https://www.peak-system.com/PCAN-Basic.239.0.html?&L=1) for the `python-can` library to detect your hardware.
*   **Drivers (Linux):** Install `can-utils` for system-level CAN management.
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
```

### 3. Install Dependencies

The project dependencies are managed by `pyproject.toml`.

```bash
# Install the packages listed in pyproject.toml
pip install -e .
```

### 4. Configuration

*   **Hardware (Automatic):** The script now auto-detects your OS and configures the CAN hardware settings.
    *   On **Windows**, it selects the `pcan` interface.
    *   On **Linux**, it selects the `socketcan` interface with channel `can0`.
    *   If you need to change the bitrate or PCAN channel name, you can edit the `config.py` file directly.
*   **Files and Signals:**
    *   Place your DBC file (e.g., `VCU.dbc`) in the `input/` directory.
    *   Place your signal list (`master_sigList.txt`) in the `input/` directory.
    *   The signal list must be a text file with each line in the format: `CAN_ID,Signal_Name,CycleTime`.

**Example `master_sigList.txt`:**

```
0x09A,ETS_VCU_Gear_Engaged_St_enum,10
0x310,ETS_VCU_AccelPedal_Act_perc,100
```

## Usage

Ensure your PCAN hardware is connected and your virtual environment is activated.

### On Linux (e.g., Raspberry Pi)

You **must** bring the CAN interface up manually before running the script.

1.  **Bring the interface up:**
    ```bash
    sudo ip link set can0 up type can bitrate 500000
    ```
2.  **Run the logger:**
    ```bash
    python main.py
    ```

### On Windows

1.  **Run the logger:**
    ```bash
    python main.py
    ```

The logger will start and begin saving data to the `output/` folder. To stop, press `Ctrl+C`. A performance and signal report will be displayed on exit.

## Troubleshooting (Linux / SocketCAN)

*   **Error:** `OSError: [Errno 100] Network is down`
    *   **Cause:** You did not bring the `can0` interface up before running the script.
    *   **Solution:** Run `sudo ip link set can0 up type can bitrate 500000` (or your required bitrate).
*   **Error:** `Cannot find device "can0"`
    *   **Cause:** The kernel driver for your PCAN adapter (`peak_usb`) is not loaded or the hardware is not detected.
    *   **Solution:** Unplug and replug the adapter. Run `lsmod | grep peak_usb` to verify the driver is loaded.
*   **Error:** `TypeError: expected str, bytes or os.PathLike object, not int`
    *   **Cause:** Your `config.py` is misconfigured. `CAN_CHANNEL` is set to an integer (like `0`) instead of a string (like `"can0"`).
    *   **Solution:** Edit `config.py` and ensure `CAN_CHANNEL = "can0"` for the Linux/SocketCAN configuration.

## Development Conventions

*   The project uses a modular structure, with clear separation of concerns between the different components of the pipeline.
*   Configuration is centralized in `config.py`.
*   The `main.py` script orchestrates the entire pipeline.
*   The project uses `multiprocessing` to take advantage of multiple CPU cores.
*   Shared memory is used to efficiently transfer data between processes.
*   The `pyproject.toml` file defines the project dependencies.
*   The code is well-commented, and the `README.md` file provides a good overview of the project.