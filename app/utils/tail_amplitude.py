def get_tail_beat_amplitude(data: dict) -> str:
    """
    Calculate the tail beat amplitude from data containing x/y coordinates
    
    Args:
        data: Dictionary with keys like "60x", "60y", "70x", "70y", etc.
    
    Returns:
        Amplitude rounded to 3 decimal places (as string)
    """
    # ✅ Check if data exists and is not empty
    if not data:
        print("No data or joints available")
        return "0.000"
    
    # ✅ Get frame numbers from x keys (only half the array)
    frames = []
    for key in data.keys():
        if "x" in key:
            try:
                frames.append(int(key.replace("x", "").replace("_", "")))
            except ValueError:
                continue
    
    if len(frames) == 0:
        return "0.000"
    
    # ✅ Get min and max y values (single pass)
    min_y = float('inf')
    max_y = float('-inf')
    
    for frame in frames:
        y_key = f"{frame}y"
        if y_key in data:
            y_val = data[y_key]
            if y_val < min_y:
                min_y = y_val
            if y_val > max_y:
                max_y = y_val
    
    # ✅ If no valid y values found
    if min_y == float('inf'):
        return "0.000"
    
    # ✅ Calculate amplitude
    amplitude = (max_y - min_y) / 2
    
    # ✅ Return rounded to 3 decimal places
    return f"{amplitude:.3f}"