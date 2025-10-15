# can_sniffer.py
# A minimal script to diagnose message reception issues with python-can.

import can
import time

# --- Use the exact same settings as your main application ---
CAN_INTERFACE = "kvaser"
CAN_CHANNEL = 0
CAN_BITRATE = 500000

def main():
    """Connects to the CAN bus and prints every message received."""
    
    print("--- CAN Bus Sniffer ---")
    print(f"Attempting to connect to {CAN_INTERFACE} channel {CAN_CHANNEL} at {CAN_BITRATE} bps...")
    
    bus = None
    try:
        # We use a simple blocking reader here for simplicity.
        # This is the most direct way to read from the bus.
        bus = can.interface.Bus(
            interface=CAN_INTERFACE,
            channel=CAN_CHANNEL,
            bitrate=CAN_BITRATE,
            receive_own_messages=False
        )
        
        print("Connection successful. Listening for messages...")
        print("Press Ctrl+C to stop.")
        
        start_time = time.time()
        msg_count = 0
        
        while True:
            msg = bus.recv(timeout=1.0) # Wait up to 1 second for a message
            if msg:
                msg_count += 1
                # Print the ID in both decimal and hex for clarity
                print(f"Received: ID=0x{msg.arbitration_id:03x} ({msg.arbitration_id:4d}) | Timestamp={msg.timestamp:.4f}")
            else:
                print(" -> No messages received in the last second.")

    except can.CanError as e:
        print(f"Error connecting to or reading from CAN bus: {e}")
    except KeyboardInterrupt:
        print("\n\n--- Sniffer stopped ---")
    finally:
        if bus:
            bus.shutdown()
        
        end_time = time.time()
        duration = end_time - start_time
        if duration > 0:
            rate = msg_count / duration
            print(f"Received {msg_count} messages in {duration:.2f} seconds ({rate:.2f} msg/s).")

if __name__ == "__main__":
    main()