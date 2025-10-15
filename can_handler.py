# can_handler.py

import can
import queue
import threading

class CANReader(threading.Thread):
    """
    A class for reading CAN messages and dispatching them to the correct
    processing queue based on their cycle time.
    """
    def __init__(self, interface, channel, bitrate, data_queues, id_to_queue_map):
        """
        Initializes the CANReader (Dispatcher) thread.

        Args:
            interface (str): The CAN interface to use (e.g., 'kvaser').
            channel (int): The channel of the CAN interface.
            bitrate (int): The bitrate for the CAN bus.
            data_queues (dict): A dictionary of queues, e.g., {'high': Queue(), 'low': Queue()}.
            id_to_queue_map (dict): A map from CAN ID (str) to queue name ('high' or 'low').
        """
        super().__init__(daemon=True)
        self.interface = interface
        self.channel = channel
        self.bitrate = bitrate
        self.data_queues = data_queues
        self.id_to_queue_map = id_to_queue_map
        self.bus = None
        self._is_running = threading.Event()

    def run(self):
        """
        The main method of the thread. Connects to the CAN bus and continuously
        reads messages, dispatching them to the appropriate queue.
        """
        try:
            # --- THIS IS THE FIX ---
            # Increase the size of the driver's internal receive buffer to prevent
            # high-frequency messages from being dropped before processing.
            kvaser_config = {
                "receive_own_messages": False,
                "receive_buffer_size": 65536  # Default is often small (e.g., 2048)
            }

            # Attempt to initialize the CAN bus interface with the new config
            self.bus = can.interface.Bus(
                interface=self.interface,
                channel=self.channel,
                bitrate=self.bitrate,
                fd=False,
                **kvaser_config # Pass the configuration dictionary here
            )
            
            # Signal success to the main thread
            if 'low' in self.data_queues:
                self.data_queues['low'].put("CONNECTION_SUCCESS")
            else:
                self.data_queues['high'].put("CONNECTION_SUCCESS")
            
            self._is_running.set()

            # Main loop to read and dispatch messages
            while self._is_running.is_set():
                msg = self.bus.recv(timeout=0.1)
                if msg:
                    msg_id_hex = f"0x{msg.arbitration_id:X}"
                    queue_name = self.id_to_queue_map.get(msg_id_hex)
                    
                    if queue_name:
                        try:
                            self.data_queues[queue_name].put_nowait(msg)
                        except queue.Full:
                            print(f"Warning: Python queue '{queue_name}' is full. Message dropped.")

        except can.CanError as e:
            error_msg = f"ERROR: Failed to connect to CAN bus. Details: {e}"
            if 'low' in self.data_queues:
                self.data_queues['low'].put(error_msg)
            else:
                self.data_queues['high'].put(error_msg)
        finally:
            if self.bus:
                self.bus.shutdown()

    def stop(self):
        """Signals the thread to stop running."""
        self._is_running.clear()