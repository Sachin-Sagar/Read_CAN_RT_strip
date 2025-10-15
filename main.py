# main.py

import cantools
import os
import queue
import json
from datetime import datetime
import can

# Import custom modules and configuration
import config
import utils
from can_handler import CANReader
from data_processor import DataProcessor

def main():
    """
    The main function to orchestrate the CAN logger using parallel processing pipelines.
    """
    print("--- Real-Time CAN Logger ---")

    # --- 1. Load Configuration ---
    print("\n[+] Loading configuration...")
    dbc_path = os.path.join(config.INPUT_DIRECTORY, config.DBC_FILE)
    signal_list_path = os.path.join(config.INPUT_DIRECTORY, config.SIGNAL_LIST_FILE)

    try:
        db = cantools.database.load_file(dbc_path)
        print(f" -> DBC file loaded: '{config.DBC_FILE}'")
    except Exception as e:
        print(f"Error: Failed to parse DBC file '{dbc_path}': {e}. Exiting.")
        return

    high_freq_signals, low_freq_signals, id_to_queue_map = utils.load_signals_to_monitor(signal_list_path)
    if id_to_queue_map is None: return

    all_monitoring_signals = {s for group in (high_freq_signals, low_freq_signals) for sig_set in group.values() for s in sig_set}
    total_signals = len(all_monitoring_signals)
    print(f" -> Signal list loaded. Monitoring {total_signals} signals.")

    os.makedirs(config.OUTPUT_DIRECTORY, exist_ok=True)
    timestamp_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_filename = f"can_log_{timestamp_str}.json"
    output_filepath = os.path.join(config.OUTPUT_DIRECTORY, output_filename)
    print(f" -> Output will be saved to: '{output_filepath}'")

    # --- 2. Initialize Pipelines and Hardware ---
    print("\n[+] Initializing worker threads...")
    raw_queues = {'high': queue.Queue(maxsize=2000), 'low': queue.Queue(maxsize=500)}
    processed_log_queue = queue.Queue(maxsize=4000)
    data_tracker = {'successfully_logged_signals': set(), 'decode_errors_printed': set()}

    bus = None
    try:
        print(" -> Connecting to CAN hardware...")
        bus = can.interface.Bus(
            interface=config.CAN_INTERFACE, channel=config.CAN_CHANNEL,
            bitrate=config.CAN_BITRATE, receive_own_messages=False
        )
        print(f" -> Connection successful on '{config.CAN_INTERFACE}' channel {config.CAN_CHANNEL}.")

        # --- Initialize and start all threads ---
        dispatcher_thread = CANReader(bus=bus, data_queues=raw_queues, id_to_queue_map=id_to_queue_map)
        
        high_freq_processor = DataProcessor(
            db=db, signals_to_monitor=high_freq_signals, raw_queue=raw_queues['high'],
            log_queue=processed_log_queue, data_tracker=data_tracker
        )
        low_freq_processor = DataProcessor(
            db=db, signals_to_monitor=low_freq_signals, raw_queue=raw_queues['low'],
            log_queue=processed_log_queue, data_tracker=data_tracker
        )

        dispatcher_thread.start()
        high_freq_processor.start()
        low_freq_processor.start()

        print("\n[+] Logging data... Press Ctrl+C to stop.")

        # --- 3. Main Logging Loop (File I/O) ---
        with open(output_filepath, 'a') as log_file:
            while True:
                try:
                    log_entry_dict = processed_log_queue.get(timeout=3.0)
                    log_line = json.dumps(log_entry_dict) + '\n'
                    log_file.write(log_line)
                except queue.Empty:
                    if not dispatcher_thread.is_alive():
                        print(" -> Dispatcher thread has stopped. Exiting.")
                        break
                    continue

    except can.CanError as e:
        print(f"\nFATAL ERROR: Failed to connect to or read from the CAN bus: {e}")
    except KeyboardInterrupt:
        print("\n\n[+] Ctrl+C detected. Shutting down gracefully...")
    finally:
        # --- 4. Cleanup and Shutdown ---
        print(" -> Stopping worker threads...")
        if 'dispatcher_thread' in locals() and dispatcher_thread.is_alive(): dispatcher_thread.stop()
        if 'high_freq_processor' in locals() and high_freq_processor.is_alive(): high_freq_processor.stop()
        if 'low_freq_processor' in locals() and low_freq_processor.is_alive(): low_freq_processor.stop()

        if 'dispatcher_thread' in locals(): dispatcher_thread.join(timeout=1)
        if 'high_freq_processor' in locals(): high_freq_processor.join(timeout=1)
        if 'low_freq_processor' in locals(): low_freq_processor.join(timeout=1)
        
        if bus: bus.shutdown()
        print(" -> Worker threads stopped.")
        
        # --- 5. Final Report ---
        unseen_signals = all_monitoring_signals - data_tracker['successfully_logged_signals']
        if unseen_signals:
            print("\nWarning: The following signals were never logged:")
            for signal in sorted(list(unseen_signals)):
                print(f" - {signal}")
        elif data_tracker['successfully_logged_signals']:
            print("\n -> All signals in the monitoring list were logged at least once.")
            
        print(" -> Logging complete.")
        print("\n--- Logger has finished ---")

if __name__ == "__main__":
    main()