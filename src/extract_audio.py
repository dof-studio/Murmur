# Project whispertxt
# src/extract_audio.py
# Version 0.0.1 built 240821
# DOF Studio, 2024

# Import libraries
import ffmpeg
import os
import subprocess
import json

# Import custom libraries
from pathwork import *

# Setting relative filepaths
local_tools_ffmpeg = "..\\env\\ffmpeg\\bin\\"

# Set the path to ffmpeg manually
os.environ["PATH"] += os.pathsep + to_absolute_path(local_tools_ffmpeg)

import subprocess
import os

# Function to run commands in the shell
def run_command(command):
    """
    Run a command in the shell and return the output.
    
    Args:
        command (list): Command to run as a list of arguments.
    
    Returns:
        str: Output of the command.
    """
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Command failed with error: {e.stderr}")

# Function to run the ffprobe executable file
def run_ffprobe(input_file):
    """
    Run ffprobe to get media stream information.
    
    Args:
        input_file (str): Path to the input file.
    
    Returns:
        dict: JSON output from ffprobe.
    """
    command = ['ffprobe', '-v', 'error', '-show_entries', 'stream=index', '-of', 'json', input_file]
    output = run_command(command)
    return json.loads(output)

# Function to extract audio from a video file
def detect_audio_format(input_file):
    """
    Detect the audio format of the input file and generate a possible file extension.
    
    Args:
        input_file (str): Path to the input file.
    
    Returns:
        str: Suggested file extension based on the audio codec.
    """
    def run_ffprobe(input_file):
        """
        Run ffprobe to get media stream information.
        
        Args:
            input_file (str): Path to the input file.
        
        Returns:
            dict: JSON output from ffprobe.
        """
        try:
            result = subprocess.run(
                ['ffprobe', '-v', 'error', '-show_entries', 'stream=codec_name', '-of', 'json', input_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            return json.loads(result.stdout)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"ffprobe error: {e.stderr}")
        except FileNotFoundError:
            raise RuntimeError("ffprobe is not installed or not found in PATH.")
    
    # Define mapping from audio codec to file extension
    codec_to_extension = {
        'aac': 'aac',
        'mp3': 'mp3',
        'opus': 'opus',
        'vorbis': 'ogg',
        'pcm_s16le': 'wav',
        'pcm_s32le': 'wav',
        'flac': 'flac',
        'alac': 'm4a'
    }
    
    # Run ffprobe to get audio stream codec
    probe_data = run_ffprobe(input_file)
    codecs = [stream['codec_name'] for stream in probe_data.get('streams', []) if stream.get('codec_name') in codec_to_extension.keys()]
    
    if not codecs:
        raise ValueError("No audio streams found in the input file.")
    
    # Choose the first codec (you could enhance this to handle multiple codecs)
    codec = codecs[0]
    
    # Get file extension based on codec
    file_extension = codec_to_extension.get(codec, 'unknown')
    
    return file_extension

# ExAu
# Function to extract audio from any file
def extract_audio_from_file(input_file, output_file):
    """
    Extract audio from a given file and save it to the disk, handling format conversion.
    
    Args:
        input_file (str): Path to the input file (audio or video).
        output_file (str): Path to save the extracted audio file (with desired format).
    
    Returns:
        None
    """
    if not os.path.isfile(input_file):
        raise FileNotFoundError(f"The file {input_file} does not exist.")
    
    command = ['ffmpeg', '-i', input_file, output_file, '-y']
    run_command(command)
    print(f"Audio extracted and saved to {output_file}")

# ExAu
# Function to extract the first audio track from a file with multiple audio tracks
def extract_first_audio_track(input_file, output_file):
    """
    Extract the first audio track from a file with multiple audio tracks, and save it to the disk.
    
    Args:
        input_file (str): Path to the input file (audio or video with multiple audio tracks).
        output_file (str): Path to save the extracted audio file (with desired format).
    
    Returns:
        None
    """
    if not os.path.isfile(input_file):
        raise FileNotFoundError(f"The file {input_file} does not exist.")
    
    probe_data = run_ffprobe(input_file)
    audio_streams = [stream['index'] for stream in probe_data.get('streams', []) if stream.get('codec_type') == 'audio']
    
    if not audio_streams:
        raise ValueError("No audio streams found in the input file.")
    
    audio_stream_index = audio_streams[0]
    command = ['ffmpeg', '-i', input_file, '-map', f'0:{audio_stream_index}', output_file, '-y']
    run_command(command)
    print(f"Audio track {audio_stream_index} extracted and saved to {output_file}")

# ExAu
# Function to extract audio from a video file
def extract_audio_from_video_or_audio(input_file, output_file):
    """
    Extract audio from a file, handling pure audio files, video files, and video containers with audio tracks.
    
    Args:
        input_file (str): Path to the input file (audio or video).
        output_file (str): Path to save the extracted audio file (with desired format).
    
    Returns:
        None
    """
    if not os.path.isfile(input_file):
        raise FileNotFoundError(f"The file {input_file} does not exist.")
    
    probe_data = run_ffprobe(input_file)
    audio_streams = [stream['index'] for stream in probe_data.get('streams', []) if stream.get('codec_type') == 'audio']
    
    if audio_streams:
        audio_stream_index = audio_streams[0]
        command = ['ffmpeg', '-i', input_file, '-map', f'0:{audio_stream_index}', output_file, '-y']
        run_command(command)
        print(f"Audio track {audio_stream_index} extracted and saved to {output_file}")
    else:
        command = ['ffmpeg', '-i', input_file, output_file, '-y']
        run_command(command)
        print(f"Audio extracted and saved to {output_file}")

# General - ExAu
# Function to extract audio from a file and save it with the detected format
def extract_audio_adjusted(input_file, output_file):
    """
    Extract audio from a file and adjust the output file extension based on detected audio format.
    
    Args:
        input_file (str): Path to the input file (audio or video).
        output_file (str): Path to save the extracted audio file (with any format specified).
    
    Returns:
        New Filepath (str)
    """
    detected_extension = detect_audio_format(input_file)
    
    # Construct the new output file name with the detected extension
    base_name, _ = os.path.splitext(output_file)
    new_output_file = f"{base_name}.{detected_extension}"
    
    print(f"Detected audio format: {detected_extension}")
    print(f"Saving to: {new_output_file}")
    
    extract_audio_from_file(input_file, new_output_file)

    return new_output_file

# Convert to .wav
# Function to convert an audio file to WAV format
def convert_to_wav(input_file, output_file):
    """
    Convert any audio format to .wav using ffmpeg.
    
    Args:
        input_file (str): Path to the input audio file (in any format).
        output_file (str): Path to save the converted .wav file.
    
    Returns:
        None
    """
    command = ['ffmpeg', '-i', input_file, '-acodec', 'pcm_s16le', '-ar', '44100', output_file]
    print(f"Converting to .wav: {input_file} -> {output_file}")

    try:
        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        print(f"Audio converted to {output_file}")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Error converting to .wav: {e.stderr}")
    
    return None


########################################
# Test 

if __name__ == "__main__":

    # Example usage:
    input_file = r'C:\\Users\\T15P\\Desktop\\ssgh-mv\\nankai-edition-reaudio.mkv'
    output_file = r'output_audio.flac'

    # Extract audio
    output_file = extract_audio_adjusted(input_file, output_file)

    # Convert to .wav and delete the original file
    convert_to_wav(output_file, 'output_audio.wav')
    os.remove(output_file)
