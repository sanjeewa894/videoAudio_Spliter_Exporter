from pydub import AudioSegment
import moviepy.editor as mp
import os

def boostAudio(inputAudio):
	# 1. Load the audio using Pydub (supports various formats with ffmpeg installed)
	audio = AudioSegment.from_file(input_video, format="mp3")

	# 2. Apply a bass boost effect using filtering
	# This example applies a low-pass filter to boost frequencies below a certain threshold (e.g., 200 Hz)
	# The gain_db can be adjusted to control the boost level
	boosted_audio = audio.low_pass_filter(300).apply_gain(10) # Boosts frequencies below 200Hz by 5 dB
	boosted_audio = audio.low_pass_filter(200).apply_gain(12) # Boosts frequencies below 200Hz by 5 dB
	boosted_audio = audio.low_pass_filter(120).apply_gain(6) # Boosts frequencies below 200Hz by 5 dB

	boosted_audio = audio.overlay(boosted_audio, position=0)

	# 2. Boost the volume by 10 dB (experiment with this value)
	# Positive numbers make it louder, negative quieter.
	volume_boost_db = 1.2
	boosted_audio = boosted_audio + volume_boost_db

	# 3. Export the boosted audio to a temporary WAV file (MoviePy works well with WAV)
	temp_file_path = "temp_boosted_audio.wav"
	boosted_audio.export(temp_file_path, format="wav")

	# 4. Use the boosted audio with MoviePy (optional, if you need to merge with a video)
	audio_clip = mp.AudioFileClip(temp_file_path)

	# Example of attaching to a video clip:
	# video_clip = mp.VideoFileClip("input_video.mp4")
	# final_clip = video_clip.set_audio(audio_clip)
	# final_clip.write_videofile("output_video_with_bass.mp4")

	# Or just save the audio file if needed
	audio_clip.write_audiofile("output_boosted_audio.mp3")

	# 5. Clean up the temporary file
	os.remove(temp_file_path)
	
	

# Example usage:
input_video = r"..\HALAWATHACIAO\02.WERALIYADDHA NONSTOP - www.kalumbro.lk - HALAWATHA CIAO.mp3"

print(f"inputAudio : {input_video}")
input_video = input_video.replace("\\","/")
print(f"inputAudio : {input_video}")
boostAudio(input_video)