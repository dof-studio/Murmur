# Project whispertxt
# src/noise_reduction.py
# Version 0.0.1 built 240821
# DOF Studio, 2024

# Import libraries
import os
import noisereduce as nr
import librosa
import soundfile as sf

# Import custom libraries
from pathwork import *

# Function to reduce noise in an audio file and keep speech only but returns the audio data
def reduce_noise(input_file, output_file, *,
                 prop_decrease=1.0, stationary=True, verbose=False):
    """
    Conduct noise reduction on an audio file using noisereduce with additional parameters.
    
    Args:
        input_file (str): Path to the input audio file (must be .wav).
        output_file (str): Path to save the noise-reduced audio file.

    Optional Args:
        prop_decrease (float): Proportion of noise to be reduced. Ranges from 0 to 1.
        stationary (bool): Whether the noise is stationary (constant over time) or not.
        use_tensorflow (bool): Whether to use TensorFlow-based denoising. Set to True if TensorFlow is installed.
        verbose (bool): Whether to print verbose output. Defaults to False.
    
    Returns:
        Audio data
    """
    # Load the audio file
    audio, sr = librosa.load(input_file, sr=None)
    
    # Apply noise reduction
    reduced_noise_audio = nr.reduce_noise(
        y=audio,
        sr=sr,
        prop_decrease=prop_decrease,
        stationary=stationary
    )
    
    return reduced_noise_audio

# Function to reduce noise in an audio file and keep speech only
def reduce_noise_io(input_file, output_file, *,
                 prop_decrease=1.0, stationary=True, verbose=False):
    """
    Conduct noise reduction on an audio file using noisereduce with additional parameters.
    
    Args:
        input_file (str): Path to the input audio file (must be .wav).
        output_file (str): Path to save the noise-reduced audio file.

    Optional Args:
        prop_decrease (float): Proportion of noise to be reduced. Ranges from 0 to 1.
        stationary (bool): Whether the noise is stationary (constant over time) or not.
        use_tensorflow (bool): Whether to use TensorFlow-based denoising. Set to True if TensorFlow is installed.
        verbose (bool): Whether to print verbose output. Defaults to False.
    
    Returns:
        None
    """
    # Load the audio file
    audio, sr = librosa.load(input_file, sr=None)
    
    # Apply noise reduction
    reduced_noise_audio = nr.reduce_noise(
        y=audio,
        sr=sr,
        prop_decrease=prop_decrease,
        stationary=stationary
    )

    # If output_file exists, delete it
    if os.path.exists(output_file):
        os.remove(output_file)
    
    # Save the noise-reduced audio
    sf.write(output_file, reduced_noise_audio, sr)

    # Print a message
    if verbose:
        print(f"Noise reduction applied and saved to {output_file}")

    return None


########################################
# Test 

if __name__ == "__main__":

    # Example usage
    input_wav = r'output_audio.wav.wav'  # Replace with your input .wav file path
    output_wav = r'output_audio.wav.wav.reduced.wav'

    reduce_noise_io(
        input_file=input_wav,
        output_file=output_wav,
        prop_decrease=0.9,  # Full noise reduction
        stationary=False,  # Assume noise is stationary
    )
