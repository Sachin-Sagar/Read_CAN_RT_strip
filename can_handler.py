# can_handler.py

import can
import queue
import threading
import time

class CANReader(threading.Thread):
    """
    A class for reading CAN messages in a dedicated, high-priority thread
    and dispatching them to the correct processing queue.
    """
    def __init__(self, bus, data_queues, id_to_queue_map, perf_tracker):
        super().__init__(daemon=True)
        self.bus = bus
        self.data_queues = data_queues
        self.id_to_queue_map = id_to_queue_map
        self.perf_tracker = perf_tracker # Performance tracker
        self._is_running = threading.Event()

    def run(self):
        """
        The main method of the thread. Continuously reads messages from the
        bus using a blocking call and dispatches them.
        """
        self._is_running.set()
        
        while self._is_running.is_set():
            start_time = time.perf_counter()
            msg = self.bus.recv(timeout=0.1)
            
            if msg:
                msg_id_hex = f"0x{msg.arbitration_id:x}"
                queue_name = self.id_to_queue_map.get(msg_id_hex)
                
                if queue_name:
                    try:
                        self.data_queues[queue_name].put_nowait(msg)
                        
                        # --- Performance Tracking ---
                        end_time = time.perf_counter()
                        duration = (end_time - start_time)
                        self.perf_tracker['dispatch_total_time'] = self.perf_tracker.get('dispatch_total_time', 0) + duration
                        self.perf_tracker['dispatch_count'] = self.perf_tracker.get('dispatch_count', 0) + 1
                        # --------------------------

                    except queue.Full:
                        print(f"Warning: Python processing queue '{queue_name}' is full. Message dropped.")

    def stop(self):
        """Signals the thread to stop running."""
        self._is_running.clear()