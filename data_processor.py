# data_processor.py

import can
import time
import struct
import queue

LOG_ENTRY_FORMAT = struct.Struct('=dI32sd')

def processing_worker(decoding_rules, raw_queue, index_queue, shared_mem_array, results_queue, perf_tracker):
    """
    Worker that decodes signals, writes to shared memory, and reports
    processed signals via a dedicated results queue.
    """
    mem_view = memoryview(shared_mem_array)
    num_slots = len(shared_mem_array) // LOG_ENTRY_FORMAT.size
    current_slot = 0
    local_logged_signals = set()

    while True:
        try:
            msg = raw_queue.get()

            if msg is None:
                # --- FIXED: Report results to the dedicated queue ---
                results_queue.put(local_logged_signals)
                raw_queue.task_done()
                break

            if not isinstance(msg, can.Message):
                raw_queue.task_done()
                continue
            
            start_time = time.perf_counter()

            if msg.arbitration_id in decoding_rules:
                rules = decoding_rules[msg.arbitration_id]
                data_int = int.from_bytes(msg.data, byteorder='little')

                for name, is_signed, start, length, scale, offset in rules:
                    # ... (binary packing logic remains the same) ...
                    physical_value = (raw_value * scale) + offset
                    
                    offset = (current_slot % num_slots) * LOG_ENTRY_FORMAT.size
                    
                    LOG_ENTRY_FORMAT.pack_into(
                        mem_view, offset, msg.timestamp, msg.arbitration_id,
                        name.encode('utf-8'), physical_value
                    )
                    index_queue.put(current_slot % num_slots)
                    current_slot += 1
                    local_logged_signals.add(name)
                
                end_time = time.perf_counter()
                duration = (end_time - start_time)
                perf_tracker['processing_total_time'] = perf_tracker.get('processing_total_time', 0) + duration
                perf_tracker['processing_msg_count'] = perf_tracker.get('processing_msg_count', 0) + 1

            raw_queue.task_done()

        except (KeyboardInterrupt, EOFError):
            break
        except Exception:
            # On any other error, still try to report what was logged
            results_queue.put(local_logged_signals)
            if 'raw_queue' in locals() and not raw_queue.empty():
                raw_queue.task_done()