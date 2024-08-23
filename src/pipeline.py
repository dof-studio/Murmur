# Project whispertxt
# src/pipeline.py
# Version 0.0.1 built 240821
# DOF Studio, 2024

# Import libraries
import os
import sys
import time
import numpy as np
import argparse

# Import custom libraries
import whisper
import noise_reduction
import subtitle
import extract_audio
import pathwork
import multiinput
from whisper import whisper_inference as whi_api
from whisper import local_model_path
from whisper import local_tokenizer_path
from whisper import local_feature_extractor_path
from noise_reduction import reduce_noise_io as rn_io
from subtitle import convert_to_srt as to_srt
from subtitle import convert_to_ass as to_ass
from extract_audio import extract_audio_adjusted as extract_au
from extract_audio import convert_to_wav as to_wav
from pathwork import to_absolute_path as abs
from multiinput import process_file_paths as pfp

# Setting IO filepaths
temp_audio_path = "..\\tmp\\" # not full
dll_extension_path = "..\\env\\dll\\"
ffmpeg_path = "..\\env\\ffmpeg\\bin\\"

# Working pipeline to convert audio to text
def working_pipeline(audio_file, subtitle_file, model_type = ["medium", "base", "tiny"], noise_reduction = True, subtitle_format = "srt", *,
                nr_prop_decrease = 1.0, nr_stationary = False):
    
    # Set the python env path to the place where this file exists
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print("Current working directory: " + os.getcwd())

    # Set another env path: the dll extensions, ffmpeg temporarily
    os.environ['PATH'] = os.environ['PATH'] + ";" + dll_extension_path
    os.environ['PATH'] = os.environ['PATH'] + ";" + ffmpeg_path

    # Check audio_file's existance
    if not os.path.exists(audio_file):
        print("Input file does not exist.")
        raise FileNotFoundError("Input file: " + audio_file + " does not exist.")
    
    # Note
    # The input: audio_file can be a .txt file, with the following format:
    # 1) each line points to an audio or video file, with filepath only (can either have " or not)
    # 2) each line can be a tuple, with an input file and an output file (can either have " or not), while there is a : seperator
    # 3) each line can have a comment, starting with "#", which will be ignored
    # In this case, subtitle_file can be a path or anything. Output filepath in tuples will first be used,
    # and if only input paths, the folder of the subtitle_file will be used

    # Let's check if it is a txt file (for multitasks)
    if audio_file.endswith(".txt") == True:

        # parse the multitasks
        audio_file, subtitle_file = pfp(audio_file, subtitle_file)

    # If only a string now, make it into a list
    if isinstance(audio_file, str) == True:

        # Make it into a list
        audio_file = [audio_file]
        subtitle_file = [subtitle_file]
    
    # Iterate to do the work
    for i in range(len(audio_file)):

        audio_each = audio_file[i]
        subtitle_each = subtitle_file[i]

        # Print
        print("-> Working on " + str(i+1) + "/" + str(len(audio_file)) + " file: " + audio_each)

        # Extract audio from video file
        audio_extracted = abs(temp_audio_path) + "\\" + "_extracted_" + time.strftime("%Y%m%d-%H%M%S") + str(np.random.randint(0, 1000000)) + os.path.basename(audio_each)
        audio_extracted = extract_au(audio_each, audio_extracted) # need to receive the return value

        # Convert extracted audio to WAV
        audio_wav = abs(temp_audio_path) + "\\" + "_extracted_wav_" + time.strftime("%Y%m%d-%H%M%S") + str(np.random.randint(0, 1000000)) + os.path.basename(audio_each) + ".wav"
        to_wav(audio_extracted, audio_wav)
        os.remove(audio_extracted)

        # Reduce noise from audio file
        audio_reduced = abs(temp_audio_path) + "\\" + "_reduced_wav_" + time.strftime("%Y%m%d-%H%M%S") + str(np.random.randint(0, 1000000)) + os.path.basename(audio_each) + ".wav"
        if noise_reduction:
            rn_io(audio_wav, audio_reduced, prop_decrease=nr_prop_decrease, stationary=nr_stationary)
            os.remove(audio_wav)
        else:
            os.rename(audio_wav, audio_reduced)

        # Convert audio to text
        text = []
        subtitle = []
        if isinstance(model_type, str):
            text, subtitle = whi_api(audio_reduced, 
                                    model_path=local_model_path[model_type], 
                                    tokenizer_path=local_tokenizer_path[model_type], 
                                    feature_extractor_path=local_feature_extractor_path[model_type])
        elif isinstance(model_type, list):
            text, subtitle = whi_api(audio_reduced, 
                                    model_path=local_model_path[model_type[0]], 
                                    tokenizer_path=local_tokenizer_path[model_type[0]], 
                                    feature_extractor_path=local_feature_extractor_path[model_type[0]])
        else:
            raise TypeError("Model must be a string or a list of strings specifying the model type.")
        
        # Remove the reduced audio file
        os.remove(audio_reduced)

        # Convert text to subtitle
        if subtitle_format == "srt":
            if subtitle_each.endswith(".srt"):
                to_srt(subtitle, subtitle_each)
            else:
                to_srt(subtitle, subtitle_each + '.srt')
        elif subtitle_format == "ass":
            if subtitle_each.endswith(".ass"):
                to_ass(subtitle, subtitle_each)
            else:
                to_ass(subtitle, subtitle_each + '.ass')

    return None
               

# Command Line
if __name__ == "__main__":

    # Check if the script is being run directly
    if len(sys.argv) < 3:
        print("Usage: python pipeline.py <audio_file> <subtitle_file> [--model <model>] [--noise_reduction] [--nr_prop_decrease <prop_decrease>] [--nr_stationary] [--subtitle_format <format>]")
        sys.exit(1)
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Convert audio to text and generate subtitles.")
    parser.add_argument("audio_file", help="Path to the audio/multitask file.")
    parser.add_argument("subtitle_file", help="Path to the subtitle file.")
    parser.add_argument("--model", nargs="+", default=["medium"], help="Model to use for audio-to-text conversion. Default is 'medium'.")
    parser.add_argument("--noise_reduction", action="store_true", help="Apply noise reduction to the audio file.")
    parser.add_argument("--nr_prop_decrease", type=float, default=0.5, help="Proportion of noise to be reduced. Default is 0.5.")
    parser.add_argument("--nr_stationary", action="store_true", help="Apply stationary noise reduction to the audio file.")
    parser.add_argument("--subtitle_format", choices=["srt", "ass"], default="srt", help="Format of the subtitle file. Default is 'srt'.")
    args = parser.parse_args()
    working_pipeline(args.audio_file, args.subtitle_file, model_type=args.model, noise_reduction=args.noise_reduction, nr_prop_decrease=args.nr_prop_decrease, nr_stationary=args.nr_stationary, subtitle_format=args.subtitle_format)
    print("## Finished! Subtitle file generated successfully.")

    # Example command

    # python pipeline.py ..\\test\\test.wav ..\\output\\test_srt.srt --model medium --noise_reduction
    #  --nr_prop_decrease 0.50 --subtitle_format srt

    # python pipeline.py .\\tasklist.txt ..\\output\\ --model medium --noise_reduction
    #  --nr_prop_decrease 0.50 --subtitle_format srt

