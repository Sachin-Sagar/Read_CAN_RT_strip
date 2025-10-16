# main.py

import os
import time
from datetime import datetime
import multiprocessing
import can
import cantools
import struct

# Import custom modules and configuration
import config
import utils
from can_handler import CANReader
from data_processor import processing_worker, LOG_ENTRY_FORMAT
from log_writer import LogWriter

def main():
    """
    Main function using a shared memory pipeline and a high-performance queue.
    """
    print("--- Real-Time CAN Logger ---")

    # --- 1. Load Configuration ---
    print("\n[+] Loading configuration...")
    dbc_path = os.path.join(config.INPUT_DIRECTORY, config.DBC_FILE)
    signal_list_path = os.path.join(config.INPUT_DIRECTORY, config.SIGNAL_LIST_FILE)

    try:
        db = cantools.database.load_file(dbc_path)
    except Exception as e:
        print(f"Error: Failed to parse DBC file '{dbc_path}': {e}. Exiting.")
        return

    high_freq_signals, low_freq_signals, id_to_queue_map = utils.load_signals_to_monitor(signal_list_path)
    if id_to_queue_map is None: return

    all_monitoring_signals = {s for group in (high_freq_signals, low_freq_signals) for sig_set in group.values() for s in sig_set}
    
    print(" -> Pre-compiling decoding rules...")
    decoding_rules = utils.precompile_decoding_rules(db, {**high_freq_signals, **low_freq_signals})
    
    output_filepath = os.path.join(config.OUTPUT_DIRECTORY, f"can_log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json")
    os.makedirs(config.OUTPUT_DIRECTORY, exist_ok=True)
    print(f" -> Output will be saved to: '{output_filepath}'")

    # --- 2. Initialize Multiprocessing Components ---
    print("\n[+] Initializing worker processes...")
    manager = multiprocessing.Manager()
    
    raw_mp_queue = multiprocessing.JoinableQueue(maxsize=4000)
    index_mp_queue = manager.Queue(maxsize=16384) 
    
    # --- NEW: Dedicated queue for collecting results from workers ---
    results_queue = manager.Queue()

    buffer_size = 16384 * LOG_ENTRY_FORMAT.size
    shared_mem_array = multiprocessing.RawArray('c', buffer_size)
    
    perf_tracker = manager.dict()
    bus = None
    processes = []

    try:
        print(" -> Connecting to CAN hardware...")
        bus = can.interface.Bus(interface=config.CAN_INTERFACE, channel=config.CAN_CHANNEL, bitrate=config.CAN_BITRATE, receive_own_messages=False)
        print(f" -> Connection successful on '{config.CAN_INTERFACE}' channel {config.CAN_CHANNEL}.")

        dispatcher_thread = CANReader(bus=bus, data_queues={'high': raw_mp_queue, 'low': raw_mp_queue}, id_to_queue_map=id_to_queue_map, perf_tracker=perf_tracker)
        dispatcher_thread.start()

        log_writer_thread = LogWriter(index_queue=index_mp_queue, shared_mem_array=shared_mem_array, filepath=output_filepath, perf_tracker=perf_tracker)
        log_writer_thread.start()

        num_processes = (os.cpu_count() or 2) - 1
        print(f" -> Starting {num_processes} decoding processes...")
        for _ in range(num_processes):
            p = multiprocessing.Process(
                target=processing_worker,
                args=(decoding_rules, raw_mp_queue, index_mp_queue, shared_mem_array, results_queue, perf_tracker),
                daemon=True
            )
            processes.append(p)
            p.start()

        print("\n[+] Logging data... Press Ctrl+C to stop.")
        while all(p.is_alive() for p in processes):
            time.sleep(1)

    except (KeyboardInterrupt, SystemExit):
        print("\n\n[+] Ctrl+C detected. Shutting down gracefully...")
    except can.CanError as e:
        print(f"\nFATAL ERROR: {e}")
    finally:
        print(" -> Stopping worker threads and processes...")
        
        if 'dispatcher_thread' in locals() and dispatcher_thread.is_alive():
            dispatcher_thread.stop()
            dispatcher_thread.join(timeout=1)

        for _ in processes:
            raw_mp_queue.put(None)
        
        raw_mp_queue.join()

        for p in processes:
            p.join(timeout=2)
        
        for p in processes:
            if p.is_alive():
                p.terminate()
                p.join()

        if 'log_writer_thread' in locals() and log_writer_thread.is_alive():
            log_writer_thread.stop()
            log_writer_thread.join(timeout=2)
        
        if bus:
            bus.shutdown()
        
        print(" -> Workers stopped.")
        
        # --- FIXED: Drain the results queue to build the final report ---
        logged_signals_set = set()
        while not results_queue.empty():
            try:
                signal_set = results_queue.get_nowait()
                logged_signals_set.update(signal_set)
            except Exception:
                break
        
        unseen_signals = all_monitoring_signals - logged_signals_set

        if unseen_signals:
            print("\nWarning: The following signals were never logged:")
            for signal in sorted(list(unseen_signals)):
                print(f" - {signal}")
        elif logged_signals_set:
            print("\n -> All signals in the monitoring list were logged at least once.")
        
        print(" -> Logging complete.")
        
        print("\n--- Performance Report ---")
        # ... (performance report logic remains the same) ...

if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()