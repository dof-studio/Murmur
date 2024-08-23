# Project whispertxt
# src/whisper.py
# Version 0.0.1 built 240821
# DOF Studio, 2024

# Import libraries
import os
import time
import torch
import transformers
from transformers import pipeline, AutoProcessor, AutoModelForSpeechSeq2Seq, AutoTokenizer, AutoFeatureExtractor
if "is_torch_sdpa_available" in dir(transformers.utils):
    from transformers.utils import is_torch_sdpa_available
else:
    is_torch_sdpa_available = None
import numpy as np
import librosa
import warnings
import soundfile as sf

# Import custom libraries
from pathwork import *
from rmtmp import *

# Suppress specific warnings
warnings.filterwarnings("ignore", category=UserWarning, module='transformers')

# Setting relative filepaths
local_model_types = ['tiny', 'base', 'medium']
local_model_path = {"tiny": "..\\model\\whisper-tiny-dof\\",
                    "base": "..\\model\\whisper-base-dof\\",
                    "medium": "..\\model\\whisper-medium-dof\\"}
local_tokenizer_path = {"tiny": "..\\model\\whisper-tiny-dof\\",
                        "base": "..\\model\\whisper-base-dof\\",
                        "medium": "..\\model\\whisper-medium-dof\\"}
local_feature_extractor_path = {"tiny": "..\\model\\whisper-tiny-dof\\",
                                "base": "..\\model\\whisper-base-dof\\",
                                "medium": "..\\model\\whisper-medium-dof\\"}
local_tools_ffmpeg = "..\\env\\ffmpeg\\bin\\"
local_dll_extension = "..\\env\\dll\\"

# Setting IO filepaths
audio_input_path = "..\\test\\test.wav"
temp_audio_path = "..\\tmp\\" # not full

# Global Variables
language = '' # leave blank for auto-detect
gl_sample_rate = 16000
whisper_env_ready = False
pipe = []
model = []
tokenizer = []
feature_extractor = []

# Get the current folder
current_folder = os.path.dirname(os.path.abspath(__file__))

# Set the path to ffmpeg and dlls manually
os.environ["PATH"] += os.pathsep + to_absolute_path(local_tools_ffmpeg)
os.environ["PATH"] += os.pathsep + to_absolute_path(local_dll_extension)

# Set the device to use CUDA if available
device = "cuda:0" if torch.cuda.is_available() else "cpu"

# Function to load and resample the audio file to 16kHz
def load_and_resample_audio(file_path, target_sr=gl_sample_rate):
    audio, sr = librosa.load(file_path, sr=None)
    if sr != target_sr:
        audio = librosa.resample(audio, orig_sr=sr, target_sr=target_sr)
    return audio, target_sr

# Function to set up the whisper environment
def whisper_setup(model_path = local_model_path["medium"], 
                      tokenizer_path = local_tokenizer_path["medium"],
                      feature_extractor_path = local_feature_extractor_path["medium"]):
    
    # Use global variables
    global pipe, model, tokenizer, feature_extractor, whisper_env_ready

    # Check if the environment is already set up
    print("Using whisper model: " + model_path)
    if whisper_env_ready:
        return None

    # Load the model, tokenizer, and feature extractor
    if is_torch_sdpa_available is not None:
        if is_torch_sdpa_available():
            model = AutoModelForSpeechSeq2Seq.from_pretrained(to_absolute_path(model_path), attn_implementation="sdpa").to(device)
        else:
            model = AutoModelForSpeechSeq2Seq.from_pretrained(to_absolute_path(model_path)).to(device)
    else:
        model = AutoModelForSpeechSeq2Seq.from_pretrained(to_absolute_path(model_path)).to(device)
    tokenizer = AutoTokenizer.from_pretrained(to_absolute_path(tokenizer_path))
    feature_extractor = AutoFeatureExtractor.from_pretrained(to_absolute_path(feature_extractor_path))

    # Create the pipeline with your custom model, processor, and tokenizer
    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=tokenizer,
        feature_extractor=feature_extractor,
        chunk_length_s=30,
        device=device,
    )

    # Set the environment as ready
    whisper_env_ready = True

    return None

# Function to perform inference on a audio file
def whisper_inference(audio_input, *, 
                      temp_audio = temp_audio_path,
                      model_path = local_model_path["medium"], 
                      tokenizer_path = local_tokenizer_path["medium"],
                      feature_extractor_path = local_feature_extractor_path["medium"],
                      batch_size = 8):

    # Set up the whisper environment
    whisper_setup(model_path, tokenizer_path, feature_extractor_path)

    # Remove temporary files
    remove_old_wav_files(to_absolute_path(temp_audio))

    # Load and resample your local audio file
    audio, sr = load_and_resample_audio(to_absolute_path(audio_input))

    # Regarding to timestamp, create a new tmpfile
    abs_temp_audio_file = to_absolute_path(temp_audio) + "\\" + "tmp_" + time.strftime("%Y%m%d-%H%M%S") + str(np.random.randint(0, 1000000)) + ".wav"

    # Save the resampled audio as a temporary file for inference
    sf.write(abs_temp_audio_file, audio, sr)

    # Perform inference using the pipeline
    prediction = []
    if len(language) == 0:
        prediction = pipe(abs_temp_audio_file, batch_size=batch_size)["text"]
    else:
        prediction = pipe(abs_temp_audio_file, batch_size=batch_size, language=language)["text"]

    # Perform inference with timestamps
    prediction_with_timestamps = []
    if len(language) == 0:
        prediction_with_timestamps = pipe(abs_temp_audio_file, batch_size=batch_size, return_timestamps=True)["chunks"]
    else:
        prediction_with_timestamps = pipe(abs_temp_audio_file, batch_size=batch_size, language=language, return_timestamps=True)["chunks"]

    # return the results in a tuple
    return prediction, prediction_with_timestamps


########################################
# Test 

if __name__ == "__main__":

    # Set up the whisper environment
    whisper_setup()

    # Load and infer the audio
    prediction, prediction_with_timestamps = whisper_inference(audio_input_path)

    # Print the results
    print("Prediction: ", prediction)
    print("Prediction with timestamps: ", prediction_with_timestamps)
