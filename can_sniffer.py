# can_sniffer.py
# A minimal script to diagnose message reception issues with python-can.

import can
import time
import platform

import can
import time
import platform

# --- Configuration ---
CAN_BITRATE = 500000
OS_SYSTEM = platform.system()

def choose_can_interpreter():
    """Prompts the user to select a CAN interpreter."""
    while True:
        print("Please select your CAN interpreter:")
        print("  1: PCAN (Peak)")
        print("  2: Kvaser")
        choice = input("Enter your choice (1 or 2): ")
        if choice == '1':
            return "peak"
        elif choice == '2':
            return "kvaser"
        else:
            print("Invalid choice. Please try again.")

def get_can_config(interpreter):
    """Returns the CAN interface and channel for the given interpreter and OS."""
    if interpreter == "peak":
        if OS_SYSTEM == "Windows":
            return "pcan", "PCAN_USBBUS1"
        elif OS_SYSTEM == "Linux":
            return "socketcan", "can0"
    elif interpreter == "kvaser":
        if OS_SYSTEM == "Windows":
            return "kvaser", 0
        elif OS_SYSTEM == "Linux":
            return "kvaser", 0
    return None, None

# ----------------------------------------------------------------

def main():
    """Connects to the CAN bus and prints every message received."""
    
    print("--- CAN Bus Sniffer ---")

    # --- Get CAN Configuration ---
    interpreter = choose_can_interpreter()
    can_interface, can_channel = get_can_config(interpreter)

    if can_interface is None:
        print(f"Error: Unsupported OS '{OS_SYSTEM}' for interpreter '{interpreter}'")
        return

    print(f"Attempting to connect to {can_interface} channel {can_channel} at {CAN_BITRATE} bps...")
    
    bus = None
    # --- Performance Tracking Variables ---
    total_recv_time = 0
    total_print_time = 0
    msg_count = 0
    start_time = 0
    # ------------------------------------

    try:
        bus = can.interface.Bus(
            interface=CAN_INTERFACE,
            channel=CAN_CHANNEL,
            bitrate=CAN_BITRATE,
            receive_own_messages=False
        )
        
        print("Connection successful. Listening for messages...")
        print("Press Ctrl+C to stop.")
        
        start_time = time.time()
        
        while True:
            # --- Time the bus.recv() call ---
            recv_start = time.perf_counter()
            msg = bus.recv(timeout=1.0)
            recv_end = time.perf_counter()
            total_recv_time += (recv_end - recv_start)
            # ---------------------------------
            
            if msg:
                msg_count += 1
                
                # --- Time the print operation ---
                print_start = time.perf_counter()
                print(f"Received: ID=0x{msg.arbitration_id:03x} ({msg.arbitration_id:4d}) | Timestamp={msg.timestamp:.4f}")
                print_end = time.perf_counter()
                total_print_time += (print_end - print_start)
                # --------------------------------
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
        if duration > 0 and msg_count > 0:
            rate = msg_count / duration
            print(f"\nReceived {msg_count} messages in {duration:.2f} seconds ({rate:.2f} msg/s).")

            # --- Performance Report ---
            avg_recv = (total_recv_time / msg_count) * 1_000_000 # to microseconds
            avg_print = (total_print_time / msg_count) * 1_000_000 # to microseconds
            print("\n--- Performance Report ---")
            print(f"Avg. Receive Time: {avg_recv:.2f} µs/msg")
            print(f"Avg. Print Time  : {avg_print:.2f} µs/msg")
            print("--------------------------")


if __name__ == "__main__":
    main()
