# Project whispertxt
# src/multiinput.py
# Version 0.0.1 built 240821
# DOF Studio, 2024

# Import libraries
import os

# Function to process the audio_file and subtitle_file to get the output folder path and lists of audio and subtitle file paths
def process_file_paths(audio_file, subtitle_file, *, subtitle_type=".srt"):

    '''
    Process the audio_file and subtitle_file to get the output folder path and lists of audio and subtitle file paths.

    Args:
        audio_file (str): Path to the audio file or directory containing audio files.
        subtitle_file (str): Path to the subtitle file or directory containing subtitle files.
        subtitle_type (str): File extension of the subtitle files (default: ".srt").

    Returns:
        output_folder (str): Path to the output folder. Will all be absolute paths.

    Notes:
        # The input: audio_file can be a .txt file, with the following format:
        # 1) each line points to an audio or video file, with filepath only (can either have " or not)
        # 2) each line can be a tuple, with an input file and an output file (can either have " or not), while there is a : seperator
        # 3) each line can have a comment, starting with "#", which will be ignored
        # In this case, subtitle_file can be a path or anything. Output filepath in tuples will first be used,
        # and if only input paths, the folder of the subtitle_file will be used

    '''

    # Initialize lists to hold audio and subtitle file paths
    audio_files = []
    subtitle_files = []

    # Convert into absolute path
    audio_file = os.path.abspath(audio_file)
    subtitle_file = os.path.abspath(subtitle_file)

    # Check if audio_file is a directory
    if os.path.isdir(subtitle_file):
        subtitle_dir = subtitle_file
        os.makedirs(subtitle_dir, exist_ok=True)
    else:
        subtitle_dir = os.path.dirname(subtitle_file)
        os.makedirs(subtitle_dir, exist_ok=True)

    with open(audio_file, 'r') as f:
        for line in f:

            # Strip leading/trailing whitespace
            line = line.strip()

            # Ignore comment lines
            if line.startswith("#") or not line:
                continue

            # Ignore empty lines
            if len(line) == 0:
                continue

            # Create tmp names
            input_path = ""
            output_path = ""

            # Check if line contains a separator (therefore a tuple contained)
            if '|' in line:
                input_path, output_path = map(str.strip, line.split('|', 1))
            else:
                input_path = line
                # Construct output path based on input path and subtitle_dir
                base_name = os.path.splitext(os.path.basename(input_path))[0]
                output_path = os.path.join(subtitle_dir, f"{base_name}" + subtitle_type)
            
            # Remove quotes if any
            input_path = input_path.strip('"').strip("'")
            output_path = output_path.strip('"').strip("'")
            
            audio_files.append(os.path.abspath(input_path))
            subtitle_files.append(os.path.abspath(output_path))
    
    return audio_files, subtitle_files

########################################
# Test 

if __name__ == "__main__":

    # Example usage
    audio_file = 'tasklist.txt'
    subtitle_file = 'output_folder_or_file_path'
    audio_files, subtitle_files = process_file_paths(audio_file, subtitle_file)

    print()
    print(audio_files)
    print(subtitle_files)
