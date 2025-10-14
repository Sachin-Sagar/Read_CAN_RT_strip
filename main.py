# main.py

import cantools
import os
import json
import queue
from datetime import datetime

# Import custom modules and configuration
import config
import utils
from can_handler import CANReader

def main():
    """
    The main function to orchestrate the CAN logger.
    """
    print("--- Real-Time CAN Logger ---")

    # --- 1. Load Configuration and Prepare Files ---
    print("\n[+] Loading configuration...")

    # Construct full paths from the configuration file
    dbc_path = os.path.join(config.INPUT_DIRECTORY, config.DBC_FILE)
    signal_list_path = os.path.join(config.INPUT_DIRECTORY, config.SIGNAL_LIST_FILE)

    # Load the DBC file using cantools
    try:
        db = cantools.database.load_file(dbc_path)
        print(f" -> DBC file loaded: '{config.DBC_FILE}'")
    except FileNotFoundError:
        print(f"Error: DBC file not found at '{dbc_path}'. Please check your config.py. Exiting.")
        return
    except Exception as e:
        print(f"Error: Failed to parse DBC file '{dbc_path}': {e}. Exiting.")
        return

    # Load the list of signals to monitor using our utility function
    signals_to_monitor = utils.load_signals_to_monitor(signal_list_path)
    if signals_to_monitor is None:
        return  # Exit if the signal file was not found

    total_signals = sum(len(s) for s in signals_to_monitor.values())
    print(f" -> Signal list loaded. Monitoring {total_signals} signals.")

    # Create the output directory if it doesn't exist
    os.makedirs(config.OUTPUT_DIRECTORY, exist_ok=True)

    # Generate a unique, timestamped filename for the log
    timestamp_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_filename = f"can_log_{timestamp_str}.json"
    output_filepath = os.path.join(config.OUTPUT_DIRECTORY, output_filename)

    print(f" -> Output will be saved to: '{output_filepath}'")

    # --- 2. Initialize CAN Hardware Connection ---
    print("\n[+] Initializing CAN connection...")
    can_data_queue = queue.Queue()

    # Create and start the CAN reader thread
    can_reader_thread = CANReader(
        interface=config.CAN_INTERFACE,
        channel=config.CAN_CHANNEL,
        bitrate=config.CAN_BITRATE,
        data_queue=can_data_queue
    )
    can_reader_thread.start()

    # Wait for a connection status message from the thread
    try:
        status = can_data_queue.get(timeout=5)  # Wait up to 5 seconds for a response
        if status != "CONNECTION_SUCCESS":
            print(status)  # This will print the detailed error message from the thread
            return
    except queue.Empty:
        print("Error: Connection to CAN hardware timed out. Please check hardware and drivers.")
        return

    print(f" -> Connection successful on '{config.CAN_INTERFACE}' channel {config.CAN_CHANNEL}.")
    print("\n[+] Logging data... Press Ctrl+C to stop.")

    # --- 3. Main Logging Loop ---
    try:
        with open(output_filepath, 'a') as log_file:
            while True:
                try:
                    # Retrieve a message from the queue, waiting if necessary
                    msg = can_data_queue.get(timeout=1.0)

                    # Format the message's arbitration ID as a hex string (e.g., '0x123')
                    msg_id_hex = f"0x{msg.arbitration_id:X}"

                    # Check if the message ID is one we need to log
                    if msg_id_hex in signals_to_monitor:
                        try:
                            # Decode the raw CAN message into physical signals
                            decoded_signals = db.decode_message(msg.arbitration_id, msg.data)

                            # Iterate through the decoded signals
                            for signal_name, value in decoded_signals.items():
                                # Check if this specific signal is in our monitoring list
                                if signal_name in signals_to_monitor[msg_id_hex]:
                                    # Create the data packet for JSON logging
                                    log_entry = {
                                        "timestamp": datetime.fromtimestamp(msg.timestamp).isoformat(),
                                        "message_id": msg_id_hex,
                                        "signal": signal_name,
                                        "value": value
                                    }
                                    # Write the JSON object to the file, followed by a newline
                                    log_file.write(json.dumps(log_entry) + '\n')

                        except Exception:
                            # This catches potential errors during decoding (e.g., from a malformed
                            # message) and allows the logger to continue running without crashing.
                            pass

                except queue.Empty:
                    # This is expected if no messages arrive within the timeout period.
                    # The loop continues, waiting for the next message.
                    continue

    except KeyboardInterrupt:
        # This block executes when the user presses Ctrl+C
        print("\n\n[+] Ctrl+C detected. Shutting down gracefully...")

    finally:
        # --- 4. Cleanup and Shutdown ---
        print(" -> Stopping CAN reader thread...")
        can_reader_thread.stop()
        can_reader_thread.join(timeout=2)  # Wait for the thread to terminate
        print(" -> CAN reader thread stopped.")
        print(" -> Logging complete.")
        print("\n--- Logger has finished ---")

if __name__ == "__main__":
    main()