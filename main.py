# main.py
import cantools
import os
import queue
import json
from datetime import datetime
import can
import fast_reader  # Import our new C module
import config
import utils
from data_processor import DataProcessor # We can reuse the existing data_processor

def main():
    print("--- Real-Time CAN Logger (CMake/C-Extension Version) ---")
    print("\n[+] Loading configuration...")
    dbc_path = os.path.join(config.INPUT_DIRECTORY, config.DBC_FILE)
    signal_list_path = os.path.join(config.INPUT_DIRECTORY, config.SIGNAL_LIST_FILE)

    db = cantools.database.load_file(dbc_path)
    high_freq_signals, low_freq_signals, id_to_queue_map = utils.load_signals_to_monitor(signal_list_path)
    if id_to_queue_map is None: return
    
    all_monitoring_signals = {s for group in (high_freq_signals, low_freq_signals) for sig_set in group.values() for s in sig_set}
    print(f" -> Monitoring {len(all_monitoring_signals)} signals.")

    os.makedirs(config.OUTPUT_DIRECTORY, exist_ok=True)
    timestamp_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_filepath = os.path.join(config.OUTPUT_DIRECTORY, output_filename)
    print(f" -> Output will be saved to: '{output_filepath}'")

    print("\n[+] Initializing worker threads...")
    raw_queues = {'high': queue.Queue(maxsize=5000), 'low': queue.Queue(maxsize=1000)}
    processed_log_queue = queue.Queue(maxsize=10000)
    data_tracker = {'successfully_logged_signals': set(), 'decode_errors_printed': set()}
    
    # This is the queue our C thread will push messages into
    c_to_py_queue = queue.Queue(maxsize=5000)

    try:
        print(" -> Starting high-performance C reader thread...")
        fast_reader.start(config.CAN_CHANNEL, config.CAN_BITRATE, c_to_py_queue)
        print(f" -> C reader is running on channel {config.CAN_CHANNEL}.")

        # Start the Python data processor threads
        high_freq_processor = DataProcessor(db, high_freq_signals, raw_queues['high'], processed_log_queue, data_tracker)
        low_freq_processor = DataProcessor(db, low_freq_signals, raw_queues['low'], processed_log_queue, data_tracker)
        high_freq_processor.start()
        low_freq_processor.start()

        print("\n[+] Logging data... Press Ctrl+C to stop.")

        # Main loop: Move messages from C queue to Python processor queues
        dispatcher_is_running = True
        while dispatcher_is_running:
            try:
                # This loop is now the dispatcher, running in the main thread
                c_msg = c_to_py_queue.get(timeout=1.0)
                arb_id, data, ts_ms = c_msg
                
                msg = can.Message(
                    arbitration_id=arb_id,
                    data=data,
                    timestamp=ts_ms / 1000.0, # Convert Kvaser ms timestamp to seconds
                )

                msg_id_hex = f"0x{msg.arbitration_id:x}"
                queue_name = id_to_queue_map.get(msg_id_hex)
                if queue_name:
                    raw_queues[queue_name].put_nowait(msg)

            except queue.Empty:
                continue # No messages from C thread, just wait again
            except queue.Full:
                print(f"Warning: Python processing queue '{queue_name}' is full. Message dropped.")
            except KeyboardInterrupt:
                # Catch Ctrl+C here to break the loop
                dispatcher_is_running = False
                print("\n\n[+] Ctrl+C detected. Shutting down gracefully...")

    finally:
        print(" -> Stopping C reader and worker threads...")
        fast_reader.stop() # Signal the C thread to stop
        if 'high_freq_processor' in locals(): high_freq_processor.stop()
        if 'low_freq_processor' in locals(): low_freq_processor.stop()
        if 'high_freq_processor' in locals(): high_freq_processor.join(timeout=1)
        if 'low_freq_processor' in locals(): low_freq_processor.join(timeout=1)
        
        # Drain the final queue and write remaining logs
        print(" -> Writing remaining logs to file...")
        with open(output_filepath, 'a') as log_file:
            while not processed_log_queue.empty():
                log_entry = processed_log_queue.get_nowait()
                log_file.write(json.dumps(log_entry) + '\n')

        print(" -> Worker threads stopped.")
        # Final report... (Same as before)