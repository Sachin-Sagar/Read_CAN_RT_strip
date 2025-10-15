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
    def __init__(self, bus, data_queues, id_to_queue_map):
        """
        Initializes the CANReader (Dispatcher) thread.
        """
        super().__init__(daemon=True)
        self.bus = bus
        self.data_queues = data_queues
        self.id_to_queue_map = id_to_queue_map
        self._is_running = threading.Event()

    def run(self):
        """
        The main method of the thread. Continuously reads messages from the
        bus in a non-blocking loop and dispatches them.
        """
        self._is_running.set()
        
        while self._is_running.is_set():
            # Use a non-blocking read. If no message is available, it returns None instantly.
            msg = self.bus.recv(timeout=0)
            
            if msg:
                # Format the ID to lowercase to match the normalized keys
                msg_id_hex = f"0x{msg.arbitration_id:x}"
                queue_name = self.id_to_queue_map.get(msg_id_hex)
                
                if queue_name:
                    try:
                        self.data_queues[queue_name].put_nowait(msg)
                    except queue.Full:
                        print(f"Warning: Python processing queue '{queue_name}' is full. Message dropped.")
            else:
                # If the buffer is empty, sleep for a tiny duration (e.g., 1ms).
                # This prevents the loop from consuming 100% CPU while achieving
                # near-instant responsiveness.
                time.sleep(0.001)

    def stop(self):
        """Signals the thread to stop running."""
        self._is_running.clear()