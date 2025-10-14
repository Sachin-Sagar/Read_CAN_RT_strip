# utils.py

import os

def load_signals_to_monitor(file_path):
    """
    Parses the signal list file and creates a dictionary for quick lookups.

    The dictionary maps a CAN ID (as a string, e.g., '0x123') to a set of
    signal names that should be monitored for that specific ID. Using a set
    provides fast membership checking.

    Args:
        file_path (str): The full path to the signal list text file.

    Returns:
        dict: A dictionary where keys are CAN IDs and values are sets of signal names.
              Returns None if the file is not found.
    """
    signals = {}
    try:
        with open(file_path, 'r') as f:
            for line_num, line in enumerate(f, 1):
                # Skip empty lines or lines that are just comments
                if not line.strip() or line.strip().startswith('#'):
                    continue

                # Split by comma and strip whitespace from parts
                parts = [p.strip() for p in line.split(',')]
                
                if len(parts) == 2:
                    can_id, signal_name = parts
                    # Add the CAN ID to the dictionary if it's not already there
                    if can_id not in signals:
                        signals[can_id] = set()
                    # Add the signal name to the set for that ID
                    signals[can_id].add(signal_name)
                else:
                    print(f"Warning: Skipping malformed line {line_num} in '{file_path}': {line.strip()}")

    except FileNotFoundError:
        print(f"Error: Signal list file not found at '{file_path}'.")
        return None
    
    if not signals:
        print(f"Warning: No valid signals were loaded from '{file_path}'. The logger will not record any data.")
        
    return signals