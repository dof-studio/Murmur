# 1. Murmur
Murmur is an AI Assistant who can generate subtitles for any kind of audio streams/files. Everything built in Python and easy to run.

Its backend transcription model may be customizable, but we recommend `whisper` series from OpenAI.

# 2. Srouce code? Release?
We super-strongly recommend users to use the `release` stable versions for the following reasons:
* 1. They have included inclusive models fine-tuned on multi-language datasets
* 2. They have installed ffmpeg and other required env related tools
* 3. When Python and Modules are ready, they are simply ready to use
 
You can also build from source code, which will give you more freedom to do adjustments, including switching to other models and so. 
But one thing to be kindly noted: please use numba<=0.58.0, otherwise a LLVM error may be raised.

# 3. How to use it?
* Step 1) Install Python 3.7 and pip
(find here https://www.python.org/downloads/)

* Step 2) Install essential dependence
(the `requirements.txt` can be found at the `src` folder)

* Step 3) Install ffmpeg, models | or | Download our stable release version
(you may need: ffmpeg, whisper models to be installed, see subfolder `.md` files)

* Step 4) Run pipeline script | or | Batch files

# 4. Arguments of the command line system
This command-line tool converts audio files to text and generates subtitle files in srt or ass format. The tool supports noise reduction and allows specifying different models for audio-to-text conversion.

## Usage
To run the pipeline, use the following command:
```shell
python pipeline.py <audio_file> <subtitle_file> [--model <model>] [--noise_reduction] [--nr_prop_decrease <prop_decrease>] [--nr_stationary] [--subtitle_format <format>]
```

## Arguments
* `audio_file`: Path to the audio or multitask file.
* `subtitle_file`: Path to the subtitle file.
* `--model`: (Optional) Specify the model to use for audio-to-text conversion. You can choose from `medium`, `base`, or `tiny`. Default is `medium`.
* `--noise_reduction`: (Optional) Apply noise reduction to the audio file.
* `--nr_prop_decrease`: (Optional) Set the proportion of noise to be reduced. Default is `0.5`.
* `--nr_stationary`: (Optional) Apply stationary noise reduction to the audio file.
* `--subtitle_format`: (Optional) Specify the format of the subtitle file. Choose between `srt` and `ass`. Default is `srt`.

## Example Command
```shell
python pipeline.py "..\\test\\test.wav" "..\\output\\test.srt" --model medium --noise_reduction --nr_prop_decrease 0.9 --nr_stationary --subtitle_format srt
```

## Input File Details
#### 1. Audio File
The `audio_file` can be either a direct path to a single audio or video file or a `.txt` file containing multiple tasks. The `.txt` file can have the following formats:

1) File Path Only: Each line points to an audio or video file, with or without quotes.
```text
"C:\path\to\audio1.wav"
C:\path\to\audio2.mp3
```

2) Tuple Format: Each line can be a tuple with an input file and an output file, separated by |, with or without quotes.
```text
"C:\path\to\audio3.ogg" | "C:\path\to\output3.srt"
C:\path\to\audio4.m4a | C:\path\to\output4.ass
```

3) Comment Lines: Lines starting with # will be ignored.

#### 2. Subtitle File
The `subtitle_file` can be a file path or a folder.
If the `subtitle_file` is a folder, the output subtitles will be saved in this folder using the input file's name as the base name.

#### 3. Output
The script will generate subtitle files based on the audio input, applying noise reduction if specified. The subtitles will be in the format specified by the --subtitle_format argument.

#### 4. Example Output
If the input is a single audio file: The generated subtitle file will be saved in the location specified by subtitle_file.

If the input is a multitask .txt file: Multiple subtitle files will be generated according to the output paths specified in the .txt file.


# 5. Unfixed bugs
* B060040: Bash Filepaths do NOT support non-ASCII characters

# 6. About the author
Nathmath from DOF Studio, on Aug 22, 2024.

Nathmath is/was a Master's student of NYU MSFE program.

