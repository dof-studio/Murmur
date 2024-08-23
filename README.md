# Murmur
Murmur is an AI Assistant who can generate subtitles for any kind of audio streams/files. Everything built in Python and easy to run.

Its backend transcription model may be customizable, but we recommend `whisper` series from OpenAI.

# Srouce code? Release?
We super-strongly recommend users to use the `release` stable versions for the following reasons:
* 1. They have included inclusive models fine-tuned on multi-language datasets
* 2. They have installed ffmpeg and other required env related tools
* 3. When Python and Modules are ready, they are simply ready to use
 
You can also build from source code, which will give you more freedom to do adjustments, including switching to other models and so. 
But one thing to be kindly noted: please use numba<=0.58.0, otherwise a LLVM error may be raised.

# How to use it?
* Step 1) Install Python 3.7 and pip
(find here https://www.python.org/downloads/)

* Step 2) Install essential dependence
(the `requirements.txt` can be found at the `src` folder)

* Step 3) Install ffmpeg, models | or | Download our stable release version
(you may need: ffmpeg, whisper models to be installed, see subfolder `.md` files)

* Step 4) Run pipeline script | or | Batch files

# Arguments of the command line system

# About the author
Nathmath from DOF Studio, on Aug 22, 2024.

Nathmath is/was a Master's student of NYU MSFE program.

