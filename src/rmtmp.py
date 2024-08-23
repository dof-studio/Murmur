# Project whispertxt
# src/rmtmp.py
# Version 0.0.1 built 240821
# DOF Studio, 2024

# Import libraries
import os
import re
from datetime import datetime, timedelta

# Import custom libraries
from pathwork import *

# Setting IO filepaths
temp_audio_path = "..\\tmp\\" # not full

# Global Variables
remove_days = 7

# Function to remove files that match the pattern tmp_YYYYMMDD-randomdigits.wav having old dates
def remove_old_wav_files(folder_path, *, days_old = remove_days, verbose=False):
    """
    Remove files in the specified folder that match the pattern tmp_YYYYMMDD-randomdigits.wav
    and were created X days ago.

    :param folder_path: Path to the folder containing the files.
    :param days_old: Number of days to consider a file as old.
    :param verbose: If True, print information about the files being removed.
    
    :return: None
    """
    # Calculate the cutoff time
    cutoff_date = datetime.now() - timedelta(days=days_old)
    
    # Define the regex pattern to match files
    pattern = re.compile(r'[^0-9]*(\d{8})-[^.]+\.[^.]+')
    
    for filename in os.listdir(folder_path):
        match = pattern.match(filename)
        if match:
            # Extract the date part from the filename
            file_date_str = match.group(1)
            file_date = datetime.strptime(file_date_str, '%Y%m%d')
            
            # Compare file date with cutoff date
            if file_date < cutoff_date:
                file_path = os.path.join(folder_path, filename)
                try:
                    os.remove(file_path)
                    if verbose:
                        print(f"Removed: {file_path}")
                except Exception as e:
                    print(f"Error in removing {file_path}: {e}")

    return None


########################################
# Test 

if __name__ == "__main__":

    # Example usage:
    remove_old_wav_files(to_absolute_path(temp_audio_path), days_old = remove_days)
    # This will remove all files in the specified folder that match the pattern tmp_YYYYMMDD-randomdigits.wav
