# utils.py

import os
import cantools
import bitstruct

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

def precompile_decoding_rules(db, signals_to_monitor):
    """
    Pre-compiles the decoding rules for faster processing.

    This function iterates through the messages and signals we need to monitor
    and extracts their decoding parameters (bit start, length, scale, offset)
    into a simple dictionary that can be used for high-speed decoding without
    relying on the slower, general-purpose cantools methods in the real-time loop.

    Returns a dictionary structured like:
    {
        message_id (int): [
            (signal_name, is_signed, start, length, scale, offset),
            ...
        ]
    }
    """
    rules = {}
    for msg_id_hex, signal_names in signals_to_monitor.items():
        try:
            msg_id_int = int(msg_id_hex, 16)
            message = db.get_message_by_frame_id(msg_id_int)
            
            rule_list = []
            for signal_name in signal_names:
                signal = message.get_signal_by_name(signal_name)
                
                # Create a tuple with all info needed for manual decoding.
                rule = (
                    signal.name,
                    signal.is_signed,
                    signal.start,
                    signal.length,
                    signal.scale,
                    signal.offset
                )
                rule_list.append(rule)
            
            if rule_list:
                rules[msg_id_int] = rule_list

        except KeyError:
            print(f"Warning: Message ID {msg_id_hex} from signal list not found in DBC file.")
            continue
            
    return rules