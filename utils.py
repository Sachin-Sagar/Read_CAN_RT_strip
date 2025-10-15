# utils.py

import os

def load_signals_to_monitor(file_path):
    """
    Parses the signal list file (format: CAN_ID,Signal_Name,CycleTime) and
    creates dictionaries to separate high-frequency and low-frequency signals.
    """
    high_freq_signals = {}
    low_freq_signals = {}
    id_to_queue_map = {}

    try:
        with open(file_path, 'r') as f:
            for line_num, line in enumerate(f, 1):
                if not line.strip() or line.strip().startswith('#'):
                    continue

                parts = [p.strip() for p in line.split(',')]
                
                if len(parts) == 3:
                    can_id_raw, signal_name, cycle_time = parts
                    
                    # Normalize the CAN ID to lowercase to prevent case-sensitivity issues.
                    can_id = can_id_raw.lower()

                    try:
                        rate = int(cycle_time)
                        if rate == 10:
                            if can_id not in high_freq_signals:
                                high_freq_signals[can_id] = set()
                            high_freq_signals[can_id].add(signal_name)
                            id_to_queue_map[can_id] = 'high'
                        elif rate == 100:
                            if can_id not in low_freq_signals:
                                low_freq_signals[can_id] = set()
                            low_freq_signals[can_id].add(signal_name)
                            id_to_queue_map[can_id] = 'low'
                        else:
                            print(f"Warning: Skipping line {line_num}. Cycle time must be 10 or 100, but got {rate}.")
                            continue
                    except ValueError:
                        print(f"Warning: Skipping malformed line {line_num}. Cycle time '{cycle_time}' is not a valid integer.")
                        continue
                else:
                    print(f"Warning: Skipping malformed line {line_num} in '{file_path}'. Expected 3 parts, got {len(parts)}.")

    except FileNotFoundError:
        print(f"Error: Signal list file not found at '{file_path}'.")
        return None, None, None
    
    if not high_freq_signals and not low_freq_signals:
        print(f"Warning: No valid signals were loaded from '{file_path}'.")
        
    return high_freq_signals, low_freq_signals, id_to_queue_map