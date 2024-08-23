# Project whispertxt
# src/whisper.py
# Version 0.0.1 built 240821
# DOF Studio, 2024

# Import libraries
import os

# Convert any path to absolute
def to_absolute_path(path):
    """
    Convert a relative or absolute path to an absolute path.
    
    Args:
        path (str): The path to convert, either relative or absolute.
    
    Returns:
        str: The absolute path.
    """
    # Get the absolute path
    absolute_path = os.path.abspath(path)
    return absolute_path


########################################
# Test 

if __name__ == "__main__":
    
    relative_path = "example/relative/path.txt"
    absolute_path = "C:/Users/Example/absolute/path.txt"

    print("Relative Path:", relative_path)
    print("Absolute Path:", to_absolute_path(relative_path))

    print("Absolute Path:", absolute_path)
    print("Absolute Path:", to_absolute_path(absolute_path))
