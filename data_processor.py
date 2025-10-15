# data_processor.py

import threading
import json
import queue
import can
from datetime import datetime
from cantools.database.namedsignalvalue import NamedSignalValue

class DataProcessor(threading.Thread):
    """
    A class for processing raw CAN messages in a dedicated thread.
    It decodes messages, formats them into Python dictionaries, and passes
    them to a logging queue.
    """
    def __init__(self, db, signals_to_monitor, raw_queue, log_queue, data_tracker):
        super().__init__(daemon=True)
        self.db = db
        self.signals_to_monitor = signals_to_monitor
        self.raw_queue = raw_queue
        self.log_queue = log_queue
        self.data_tracker = data_tracker
        self._is_running = threading.Event()

    def run(self):
        self._is_running.set()
        while self._is_running.is_set():
            try:
                msg = self.raw_queue.get(timeout=0.1)
                
                if not isinstance(msg, can.Message):
                    continue

                msg_id_hex = f"0x{msg.arbitration_id:x}" # Use lowercase for consistency
                if msg_id_hex in self.signals_to_monitor:
                    try:
                        decoded_signals = self.db.decode_message(msg.arbitration_id, msg.data)
                        for signal_name, value in decoded_signals.items():
                            if signal_name in self.signals_to_monitor[msg_id_hex]:
                                log_value = value.value if isinstance(value, NamedSignalValue) else value
                                
                                log_entry = {
                                    "timestamp": datetime.fromtimestamp(msg.timestamp).isoformat(),
                                    "message_id": msg_id_hex,
                                    "signal": signal_name,
                                    "value": log_value
                                }
                                
                                try:
                                    self.log_queue.put(log_entry, timeout=0.01)
                                except queue.Full:
                                    print(f"Warning: Final log queue is full. Log entry for '{signal_name}' dropped.")
                                self.data_tracker['successfully_logged_signals'].add(signal_name)

                    except KeyError:
                        if msg_id_hex not in self.data_tracker['decode_errors_printed']:
                            print(f"\nWarning: ProcThread failed to decode {msg_id_hex}. Possible DBC mismatch.")
                            self.data_tracker['decode_errors_printed'].add(msg_id_hex)
                    except Exception as e:
                        if msg_id_hex not in self.data_tracker['decode_errors_printed']:
                            print(f"\nWarning: ProcThread encountered an error on {msg_id_hex}: {e}")
                            self.data_tracker['decode_errors_printed'].add(msg_id_hex)
            
            except queue.Empty:
                continue
    
    def stop(self):
        self._is_running.clear()