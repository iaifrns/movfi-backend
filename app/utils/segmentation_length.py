import math
from typing import List, Dict, Any, Optional

def distance(x1: float, y1: float, x2: float, y2: float) -> float:
    """Calculate Euclidean distance between two points"""
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def get_segmentation_length(
    data: List[Dict[str, Any]], 
    joints: List[int],
    key: Optional[str] = None
) -> float:
    """
    Calculate the total length of a segmented path through data points
    
    Args:
        data: List of dictionaries containing x/y coordinates
        joints: List of indices marking segment boundaries
        key: Optional key prefix (e.g., "60" from "60x"). If not provided,
             it will be auto-detected from the first key.
    
    Returns:
        Total length rounded to 4 decimal places
    """

    if len(data) < 2 or len(joints) == 0:
        return 0.0
    
    # Auto-detect key if not provided
    if key is None:
        first_key = list(data[0].keys())[0]
        # Remove suffix: "60x" -> "60", "60_x" -> "60", "60x_y" -> "60x"
        if first_key.endswith('x'):
            key = first_key[:-1]
        elif first_key.endswith('_x'):
            key = first_key[:-2]
        else:
            # Fallback: assume format is "{key}x"
            key = first_key[:-1]
    
    total_length = 0.0
    
    # Create list of all points: start (0), joints, end (last)
    points_to_visit = [0] + joints + [len(data) - 1]
    
    # Iterate through segments
    for i in range(len(points_to_visit) - 1):
        idx1 = points_to_visit[i]
        idx2 = points_to_visit[i + 1]
        
        try:
            # Get coordinates with safe access
            x1 = data[idx1].get(f"{key}x")
            y1 = data[idx1].get(f"{key}y")
            x2 = data[idx2].get(f"{key}x")
            y2 = data[idx2].get(f"{key}y")
            
            # Check if any coordinate is missing
            if None in (x1, y1, x2, y2):
                print(f"Missing coordinates for points {idx1} or {idx2}")
                continue
            
            total_length += distance(x1, y1, x2, y2)
            
        except (IndexError, KeyError) as e:
            print(f"Error processing segment {i}: {e}")
            continue
    
    # Return rounded to 4 decimal places
    return round(total_length, 4)