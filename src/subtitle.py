# Project whispertxt
# src/pathwork.py
# Version 0.0.1 built 240821
# DOF Studio, 2024

# Import libraries
from datetime import timedelta

# Srt
# Converts timestamped transcription output to SRT format
def format_srt_timestamp(seconds):
    '''
    Converts seconds to SRT timestamp format.
    input: seconds (float)
    output: SRT timestamp (str)
    '''
    # Convert seconds to SRT timestamp format
    td = timedelta(seconds=seconds)
    return str(td).replace('.', ',')[:12]

# Srt
# Converts timestamped transcription output to a SRT format file
def convert_to_srt(transcriptions, output_file):
    '''
    Converts timestamped transcription output to a SRT format file.
    input: transcriptions (list of dicts), output_file (str)
    output: None
    '''
    with open(output_file, 'w', encoding='utf-8') as file:
        for i, entry in enumerate(transcriptions):
            start, end = entry['timestamp']
            start_time = format_srt_timestamp(start)
            end_time = format_srt_timestamp(end)
            text = entry['text']
            
            file.write(f"{i + 1}\n")
            file.write(f"{start_time} --> {end_time}\n")
            file.write(f"{text}\n")
            file.write("\n")

    return None

# ass
# Converts timestamped transcription output to ASS format
def format_ass_timestamp(seconds):
    '''
    Converts seconds to ASS timestamp format.
    input: seconds (float)
    output: ASS timestamp (str)
    '''
    # Convert seconds to ASS timestamp format
    td = timedelta(seconds=seconds)
    return str(td).split(".")[0].replace(":", ",", 2)

# ass
# Converts timestamped transcription output to a ASS format file
def convert_to_ass(transcriptions, output_file):
    '''
    Converts timestamped transcription output to a ASS format file.
    input: transcriptions (list of dicts), output_file (str)
    output: None
    '''
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write("[Script Info]\n")
        file.write("Title: Subtitle\n")
        file.write("Original Script: ChatGPT\n")
        file.write("ScriptType: v4.00\n")
        file.write("Collisions: Normal\n")
        file.write("PlayDepth: 0\n")
        file.write("\n")
        
        file.write("[Styles]\n")
        file.write("Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, TertiaryColour, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, AlphaLevel, Encoding\n")
        file.write("Style: Default,Arial,20,16777215,0,0,1,1,0,2,10,10,10,0,0\n")
        file.write("\n")
        
        file.write("[Events]\n")
        file.write("Format: Marked, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
        
        for entry in transcriptions:
            start, end = entry['timestamp']
            start_time = format_ass_timestamp(start)
            end_time = format_ass_timestamp(end)
            text = entry['text']
            
            file.write(f"Dialogue: Marked=0,0:{start_time},0:{end_time},Default,,0,0,0,,{text}\n")

    return None


########################################
# Test 

if __name__ == "__main__":
    
    # Example timestamped transcription output
    timestamped_output = [{'timestamp': (0.0, 1.24), 'text': "Hey buddy, I'm good."}]

    # Convert to .srt format
    convert_to_srt(timestamped_output, 'output.srt')
    # Convert to .ass format
    convert_to_ass(timestamped_output, 'output.ass')
