# can_handler.py

import can
import queue
import threading

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
        bus using a blocking call and dispatches them.
        """
        self._is_running.set()
        
        while self._is_running.is_set():
            # Use a pure blocking read with no timeout. This is the most
            # efficient way to wait for a message. The thread will sleep
            # until a message is received, consuming no CPU.
            msg = self.bus.recv()
            
            if msg:
                # Format the ID to lowercase to match the normalized keys
                msg_id_hex = f"0x{msg.arbitration_id:x}"
                queue_name = self.id_to_queue_map.get(msg_id_hex)
                
                if queue_name:
                    try:
                        self.data_queues[queue_name].put_nowait(msg)
                    except queue.Full:
                        # This is a critical warning. If you see this, it means your
                        # data processor threads can't keep up with the dispatcher.
                        print(f"CRITICAL: Processing queue '{queue_name}' is full. DATA LOSS IS OCCURRING.")

    def stop(self):
        """Signals the thread to stop running."""
        self._is_running.clear()