# log_writer.py

import threading
import queue
import json
import time
import struct

# Must match the format in data_processor.py
LOG_ENTRY_FORMAT = struct.Struct('=dI32sd')

class LogWriter(threading.Thread):
    """
    A dedicated thread that reads data indices from a queue, unpacks
    binary data from a shared memory array, and writes it to a file.
    """
    def __init__(self, index_queue, shared_mem_array, filepath, perf_tracker, batch_size=1000):
        super().__init__(daemon=True)
        self.index_queue = index_queue
        self.shared_mem_array = shared_mem_array
        self.filepath = filepath
        self.perf_tracker = perf_tracker
        self.batch_size = batch_size
        self._is_running = threading.Event()

    def run(self):
        self._is_running.set()
        
        with open(self.filepath, 'a') as log_file:
            while self._is_running.is_set() or not self.index_queue.empty():
                write_batch = []
                while len(write_batch) < self.batch_size:
                    try:
                        slot_index = self.index_queue.get(timeout=0.01)
                        
                        # --- High-Performance Binary Unpacking ---
                        offset = slot_index * LOG_ENTRY_FORMAT.size
                        
                        # Unpack the raw bytes from shared memory
                        ts, can_id, sig_name_bytes, value = LOG_ENTRY_FORMAT.unpack_from(
                            self.shared_mem_array, offset
                        )

                        # Decode the signal name, removing null padding
                        sig_name = sig_name_bytes.strip(b'\x00').decode('utf-8')
                        
                        # Create the dictionary at the last possible moment
                        log_entry = {
                            "timestamp": time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(ts)) + f".{int((ts % 1) * 1e6):06d}",
                            "message_id": f"0x{can_id:x}",
                            "signal": sig_name,
                            "value": value
                        }
                        write_batch.append(log_entry)

                    except queue.Empty:
                        break
                
                if write_batch:
                    start_time = time.perf_counter()
                    log_lines = [json.dumps(entry) + '\n' for entry in write_batch]
                    log_file.writelines(log_lines)
                    end_time = time.perf_counter()
                    
                    duration = end_time - start_time
                    self.perf_tracker['log_write_total_time'] = self.perf_tracker.get('log_write_total_time', 0) + duration
                    self.perf_tracker['log_write_batch_count'] = self.perf_tracker.get('log_write_batch_count', 0) + 1

    def stop(self):
        """Signals the thread to stop running."""
        self._is_running.clear()