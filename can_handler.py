# can_handler.py

import can
import queue
import threading

class CANReader(threading.Thread):
    """
    A class for reading CAN messages from a specified interface in a separate thread.
    """
    def __init__(self, interface, channel, bitrate, data_queue):
        """
        Initializes the CANReader thread.

        Args:
            interface (str): The CAN interface to use (e.g., 'kvaser').
            channel (int): The channel of the CAN interface.
            bitrate (int): The bitrate for the CAN bus.
            data_queue (queue.Queue): A queue to put received CAN messages into.
        """
        super().__init__(daemon=True)
        self.interface = interface
        self.channel = channel
        self.bitrate = bitrate
        self.data_queue = data_queue
        self.bus = None
        self._is_running = threading.Event()

    def run(self):
        """
        The main method of the thread. Connects to the CAN bus and continuously
        reads messages, putting them into the data queue.
        """
        try:
            # Attempt to initialize the CAN bus interface
            self.bus = can.interface.Bus(
                interface=self.interface,
                channel=self.channel,
                bitrate=self.bitrate,
                fd=False
            )
            # Signal to the main thread that the connection was successful
            self.data_queue.put("CONNECTION_SUCCESS")
            self._is_running.set()

            # Main loop to read messages
            while self._is_running.is_set():
                msg = self.bus.recv(timeout=0.1)  # Use a timeout to allow checking the stop flag
                if msg:
                    self.data_queue.put(msg)

        except can.CanError as e:
            # Put a detailed error message in the queue for the main thread
            error_msg = f"ERROR: Failed to connect to CAN bus. Details: {e}"
            self.data_queue.put(error_msg)
        finally:
            if self.bus:
                self.bus.shutdown()

    def stop(self):
        """Signals the thread to stop running."""
        self._is_running.clear()