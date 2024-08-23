@echo off
echo Starting the Murmur Assistant...

python "pipeline.py" "..\\test\\test.wav" "..\\output\\test.srt" --model medium --noise_reduction --nr_prop_decrease 0.5 --nr_stationary --subtitle_format srt

pause
