# main.py

import cantools
import os
import queue
from datetime import datetime

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

    # --- 1. Load and Separate Signals by Frequency ---
    print("\n[+] Loading configuration...")

    dbc_path = os.path.join(config.INPUT_DIRECTORY, config.DBC_FILE)
    signal_list_path = os.path.join(config.INPUT_DIRECTORY, config.SIGNAL_LIST_FILE)

    try:
        db = cantools.database.load_file(dbc_path)
        print(f" -> DBC file loaded: '{config.DBC_FILE}'")
    except Exception as e:
        print(f"Error: Failed to parse DBC file '{dbc_path}': {e}. Exiting.")
        return

    # Load signals and separate them based on the new format
    high_freq_signals, low_freq_signals, id_to_queue_map = utils.load_signals_to_monitor(signal_list_path)
    if id_to_queue_map is None:
        return

    # Combine all signals for the final report
    all_monitoring_signals = {s for group in (high_freq_signals, low_freq_signals) for sig_set in group.values() for s in sig_set}
    total_signals = len(all_monitoring_signals)
    print(f" -> Signal list loaded. Monitoring {total_signals} signals ({len(high_freq_signals)} high-freq IDs, {len(low_freq_signals)} low-freq IDs).")

    os.makedirs(config.OUTPUT_DIRECTORY, exist_ok=True)
    timestamp_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_filename = f"can_log_{timestamp_str}.json"
    output_filepath = os.path.join(config.OUTPUT_DIRECTORY, output_filename)
    print(f" -> Output will be saved to: '{output_filepath}'")

    # --- 2. Initialize Parallel Pipelines ---
    print("\n[+] Initializing worker threads...")
    
    # Create separate raw message queues for each frequency
    raw_queues = {
        'high': queue.Queue(maxsize=1000),
        'low': queue.Queue(maxsize=500)
    }
    # Create a single queue for the final JSON strings
    processed_log_queue = queue.Queue(maxsize=2000)

    data_tracker = {'successfully_logged_signals': set(), 'decode_errors_printed': set()}

    # Thread 1: The dispatcher reading from hardware
    dispatcher_thread = CANReader(
        interface=config.CAN_INTERFACE,
        channel=config.CAN_CHANNEL,
        bitrate=config.CAN_BITRATE,
        data_queues=raw_queues,
        id_to_queue_map=id_to_queue_map
    )
    dispatcher_thread.start()

    # Wait for the connection to be confirmed
    try:
        # The success message is always sent to the 'low' queue
        status = raw_queues['low'].get(timeout=5)
        if status != "CONNECTION_SUCCESS":
            print(status)
            dispatcher_thread.stop(); dispatcher_thread.join()
            return
    except queue.Empty:
        print("\nError: Connection to CAN hardware timed out.")
        dispatcher_thread.stop(); dispatcher_thread.join()
        return

    print(f" -> Connection successful on '{config.CAN_INTERFACE}' channel {config.CAN_CHANNEL}.")

    # Thread 2: Processor for high-frequency (10ms) signals
    high_freq_processor = DataProcessor(
        db=db, signals_to_monitor=high_freq_signals, raw_queue=raw_queues['high'],
        log_queue=processed_log_queue, data_tracker=data_tracker
    )
    
    # Thread 3: Processor for low-frequency (100ms) signals
    low_freq_processor = DataProcessor(
        db=db, signals_to_monitor=low_freq_signals, raw_queue=raw_queues['low'],
        log_queue=processed_log_queue, data_tracker=data_tracker
    )

    high_freq_processor.start()
    low_freq_processor.start()

    print("\n[+] Logging data... Press Ctrl+C to stop.")

    # --- 3. Main Logging Loop (File I/O) ---
    try:
        with open(output_filepath, 'a') as log_file:
            while True:
                try:
                    log_line = processed_log_queue.get(timeout=3.0)
                    log_file.write(log_line)
                except queue.Empty:
                    print(" -> Waiting for processed data...")
                    continue

    except KeyboardInterrupt:
        print("\n\n[+] Ctrl+C detected. Shutting down gracefully...")

    finally:
        # --- 4. Cleanup and Shutdown ---
        print(" -> Stopping worker threads...")
        dispatcher_thread.stop()
        high_freq_processor.stop()
        low_freq_processor.stop()
        
        dispatcher_thread.join(timeout=2)
        high_freq_processor.join(timeout=2)
        low_freq_processor.join(timeout=2)
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