# This Python file uses the following encoding: utf-8
import sys, glob, os
import argparse
#from ProcessVedioOps import ProcessVedioOps, ProgressLogger
import moviepy.editor as mp
from moviepy.video.fx.all import loop as aloop
#from moviepy.video.VideoClip import ImageClip
#from moviepy.video.compositing import CompositeVideoClip
#import threading
import re
from moviepy.video.fx.resize import resize
from PIL import Image

##prevent sleep
import ctypes
import psutil
import time
from pydub import AudioSegment
from pathlib import Path


# Windows sleep prevention flags
ES_CONTINUOUS       = 0x80000000
ES_SYSTEM_REQUIRED  = 0x00000001

# Set your battery threshold (e.g., 30%)
BATTERY_THRESHOLD = 30	

def checkSleep():
	battery = psutil.sensors_battery()    
	print(f"Battery: {battery.percent}% | Plugged in: {battery.power_plugged}")

	if battery.power_plugged or battery.percent > BATTERY_THRESHOLD:
		ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)
		print("Sleep prevention active.")
	else:
		ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
		print("Battery low. Sleep prevention disabled.")

def splitVideoToChunck(timeFileName,videofilePath,targetN,videofileName):	

	if not os.path.exists(targetN):
		os.makedirs(targetN)

	with open(timeFileName) as f:
		times = f.readlines()
	times = [x.strip() for x in times]

	print('Progressing. Please wait...');
	
	if(len(times)<1):
		print("No time segments found!")
		exit(1);
		
	# loading video dsa gfg intro video
	clip = mp.VideoFileClip(videofilePath);
	print("Opened: "+videofilePath);
	
	for time1 in times:
		checkSleep()
		starttime = (time1.split("-")[0])
		endtime = (time1.split("-")[1])
		
		print(time1);

		# getting only  seconds
		clip2 = clip.subclip(starttime, endtime)
		clip2.audio.write_audiofile(targetN+"/"+videofileName+str(times.index(time1)+1)+".mp3");
		clip2.close();
		
	clip.close();
	print('Finished splitting....');

def splitVideoToAudioChunck(timeFileName,videofilePath,targetN,videofileName):
	
	targetN = targetN+"_audio"
	if not os.path.exists(targetN):
		os.makedirs(targetN)

	with open(timeFileName) as f:
		times = f.readlines()
	times = [x.strip() for x in times]

	print('Progressing. Please wait...');
	
	if(len(times)<1):
		print("No time segments found!")
		exit(1);
		
	# loading video dsa gfg intro video
	clip = mp.VideoFileClip(videofilePath);
	print("Opened: "+videofilePath);
	
	for time1 in times:
		checkSleep()
		starttime = (time1.split("-")[0])
		endtime = (time1.split("-")[1])

		print(time1);
		
		# getting only first 5 seconds
		clip2 = clip.subclip(starttime, endtime)
		clip2.audio.write_audiofile(targetN+"/"+videofileName+str(times.index(time1)+1)+".mp3");
		clip2.close();
		
	clip.close();
	print('Finished splitting....');

def splitCombineVideo(timeFileName,videofilePath,targetN,videofileName):
	
	if not os.path.exists(targetN):
		os.makedirs(targetN)

	with open(timeFileName) as f:
		times = f.readlines()
	times = [x.strip() for x in times]

	print('Progressing. Please wait...');
	
	if(len(times)<1):
		print("No time segments found!")
		exit(1);
		
	# loading video dsa gfg intro video
	clip = mp.VideoFileClip(videofilePath);
	print("Opened: "+videofilePath);
	i=0
	for time1 in times:
		checkSleep()
		starttime = (time1.split("-")[0])
		endtime = (time1.split("-")[1])
		
		fileWriteName = targetN+"/"+videofileName+str(times.index(time1)+1)+".mp4";
		
		if(len(time1.split("-"))==3):
			rFileName = (time1.split("-")[2])
			fileWriteName = targetN+"/"+rFileName+".mp4";

		videoClipName = "1_Audio_spectrum.mov";
		if i%3 == 1:
			videoClipName = "2_Audio_spectrum.mov";
		
		elif i%3 == 2:
			videoClipName = "3_Audio_spectrum.mov";
		
		
		videoClip = mp.VideoFileClip(videoClipName);

		clip2 = clip.subclip(starttime, endtime)
		audiotoWrite = clip2.audio
		totalTime = audiotoWrite.duration
		print("audio duration " , totalTime, videoClipName, i )
		videoClip = aloop(videoClip,duration=totalTime)
		print(videoClip.duration)
		videoClip = videoClip.set_audio(audiotoWrite)
		videoClip.write_videofile(fileWriteName);
		
		i += 1;
	clip.close();
	print('Finished splitting....');

		
def writeToMp3(pathtoRead,direct):
	print('Progressing. Please wait...');
	fileList = glob.glob(pathtoRead+"/*.mp4")

	if not os.path.exists(direct):
		# Create a new directory because it does not exist
		os.makedirs(direct)
		print("created directory")

	for fileName in fileList:
		checkSleep()
		# Insert Local Video File Path
		clip = mp.VideoFileClip(fileName)
		fileName = fileName.replace("\\","/");
		output =  ((fileName.split("/")[-1]).replace(" ","")).replace(".mp4",".mp3")
		print(fileName,output)
		# Insert Local Audio File Path
		clip.audio.write_audiofile(direct + "/" +output)
		clip.close();		

	print('Finished converting....');

def writeToNonstop(pathtoRead,direct):
	print('Progressing. Please wait...');
	fileList = glob.glob(pathtoRead+"/*.mp3")
	if not os.path.exists(direct):
		# Create a new directory because it does not exist
		os.makedirs(direct)
	audioArray = []	
	
	for fileName in fileList:
		# Insert Local Video File Path
		aClip = mp.AudioFileClip(fileName)
		audioArray.append(aClip)
		print(fileName)
	
	checkSleep()
	final_clip = mp.concatenate_audioclips(audioArray)
	totalTime = final_clip.duration
	print("audio duration " , totalTime)
	videoClip = mp.VideoFileClip("2_Audio_spectrum.mov");
	videoClip = aloop(videoClip,duration=totalTime)
	print(videoClip.duration)
	videoClip = videoClip.set_audio(final_clip)
	videoClip.write_videofile(direct + "/" +"Nonstop.mp4");
	videoClip.close();


def get_matching_strings(lst, pattern):
	regex = re.compile(pattern+"*",flags=re.IGNORECASE)
	return [s for s in lst if regex.search(s)]

'''
** Boost audio 
'''
def boostAudio(inputAudio):
	#inputAudio = Path(inputAudio).as_posix()
	# 1. Load the audio using Pydub (supports various formats with ffmpeg installed)
	audio = AudioSegment.from_file(inputAudio, format="mp3")
	# 2. Apply a bass boost effect using filtering
	# This example applies a low-pass filter to boost frequencies below a certain threshold (e.g., 200 Hz)
	# The gain_db can be adjusted to control the boost level
	boosted_audio = audio.low_pass_filter(300).apply_gain(10) # Boosts frequencies below 200Hz by 5 dB
	boosted_audio = audio.low_pass_filter(200).apply_gain(12) # Boosts frequencies below 200Hz by 5 dB
	boosted_audio = audio.low_pass_filter(150).apply_gain(6) # Boosts frequencies below 200Hz by 5 dB

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
		
	return audio_clip
	


'''
read the audio file from the provided audio file name
add audio to vedio and trim.
write to video
'''
def trimAudiotoVideo(timeFileName,pathtoRead):
	
	targetN = pathtoRead + "/processed";
	print("Write location: " +targetN)
	if not os.path.exists(targetN):
		os.makedirs(targetN)

	with open(timeFileName) as f:
		times = f.readlines()
	times = [x.strip() for x in times]

	print('Progressing. Please wait...');
	
	if(len(times)<1):
		print("No time segments found!")
		exit(1);
	
	fileList = glob.glob(pathtoRead+"/*.mp3")
	if(len(fileList)<1):
		print("No mp3 found!")
		exit(1);
	
	bandLogo = glob.glob(pathtoRead+"/bandlogo.jpg")
	if(len(bandLogo)<1):
		print("No logo found!")
		#exit(0)
		bandLogo = glob.glob("baseLogo.jpg")
		if(len(bandLogo)<1):
			print("No Base logo found!")
			exit(0)
	
	i=0
	endtime="";
	for time1 in times:
		checkSleep()
		starttime = ""
		endtime = ""
		if(len(time1.split("-"))==3):
			starttime = (time1.split("-")[0])
			endtime = (time1.split("-")[1])
			rFileName = (time1.split("-")[2])
		else:
			rFileName = time1;
			
		if(len(rFileName)>8):
			fileNameSplit = rFileName.split("~")[0];
			fileNameSplit = fileNameSplit.split(".")[1];
			#print(fileNameSplit)
			audioFile = get_matching_strings(fileList, fileNameSplit)[0]
			print("Opened: "+audioFile+""+fileNameSplit)

			#audioFile2 = pathtoRead +"/"+ rFileName + ".mp3"
			#print("Opened: "+audioFile+" - "+str(endtime));
	
			if (os.path.exists(audioFile)):				
				videoClipName = "1_Audio_spectrum.mov";
				if i%3 == 1:
					videoClipName = "2_Audio_spectrum.mov";				
				elif i%3 == 2:
					videoClipName = "3_Audio_spectrum.mov";
				
				fileWriteName = targetN+"/"+rFileName+".mp4";
				print(fileWriteName)
				# loading video dsa gfg intro video
				aClip = boostAudio(audioFile)
				totalTime = aClip.duration
					
				videoClip = mp.VideoFileClip(videoClipName);
				print("audio duration " , totalTime, videoClipName, i )
				videoClip = aloop(videoClip,duration=totalTime)
				print(videoClip.duration)
				videoClip = videoClip.set_audio(aClip)
				if(len(endtime)>1):
					print("Start: ",starttime," End: ",endtime)
					videoClip = videoClip.subclip(starttime, endtime)
				#add band logo
				
				title = mp.ImageClip(bandLogo[0]).set_start(0).set_duration(3).set_pos(("center","center"))
				title = title.resize((videoClip.w,videoClip.h),Image.LANCZOS)
				videoClip = mp.CompositeVideoClip([videoClip, title])
				videoClip.write_videofile(fileWriteName);
				title.close();
				videoClip.close();
				aClip.close();
				i += 1;
				
				# 5. Clean up the temporary file from bost
				temp_file_path = "temp_boosted_audio.wav"
				os.remove(temp_file_path)
				
	print('Finished splitting....');


parser = argparse.ArgumentParser("Video Splitter")
parser.add_argument("-t","--type", help="video split (1) or audio convert (2) or audio (3) or audio+video combine (4) or audios to nonstop(5) or audio trim and to video(6)", type=int,required = False, default = "")
parser.add_argument("-tf","--timefile", help="time file path (1)", type=str,required = False, default = "")
parser.add_argument("-vf","--videofile", help="video file path (1)", type=str,required = False, default = "")
parser.add_argument("-vd","--videodir", help="videos directory path (2)", type=str,required = False, default = "")
parser.add_argument("-ad","--audiodir", help="audios directory path (2)", type=str,required = False, default = "")

args = parser.parse_args()
type = args.type 


if (type == 2 or type == 5):
	#concat all files to one video 
	print("Run arg check")
	pathtoRead = args.videodir
	if(len(sys.argv) <3 or not pathtoRead):
		print("Run with -h to find arguments")
		exit(1)
	if not os.path.exists(pathtoRead):
		print("Directory not found!");
		exit(1);
		
	if(type == 2):
		
		direct = args.videodir + "/audiofiles"
		#check directory contains videos
		fileList = glob.glob(pathtoRead+"/*.mp4")		
	else:		
		direct = args.videodir + "/nonstop"
		#check directory contains videos
		fileList = glob.glob(pathtoRead+"/*.mp3")
		
		
	if(len(fileList)<1):
			print("No file found....");
			exit(1);
			
	if(type == 2):
		print("Run audio convert")
		writeToMp3(pathtoRead,direct)
	else:
		print("Run audio concat")
		writeToNonstop(pathtoRead,direct)

elif (type == 1 or type == 3 or type == 4):
	if(len(sys.argv) <6):
		print("Run with -h to find arguments")
		exit(1)
	tfname = args.timefile
	vfname=  args.videofile

	#check file exist
	if not os.path.exists(tfname):
		print("Time file not found!");
		exit(1);

	if not os.path.exists(vfname):
		print("Video file not found!");
		exit(1);
	#vedio split
	vfname = vfname.replace("\\","/")
	dirList = vfname.split("/");
	fileName = dirList[-1];
	fileName = fileName.removesuffix(".mp4");
	videofileName = fileName.replace(" ","");
	print(videofileName);
	dirList.remove(dirList[-1]);
	videoDir=""
	for t in dirList:
		videoDir+=t+"/";

	print(videoDir)	
	targetN = videoDir + videofileName;
	print(targetN)
	
	if(type == 1):
		splitVideoToChunck(tfname,vfname,targetN,videofileName)
	elif(type == 3):
		splitVideoToAudioChunck(tfname,vfname,targetN,videofileName)
	elif(type == 4):
		splitCombineVideo(tfname,vfname,targetN,videofileName)
	
elif(type == 6):
	#trim audio and write to video 
	print("Run audio trim and to video")
	if(len(sys.argv) <6):
		print("Run with -h to find arguments")
		exit(1)
	tfname = args.timefile
	pathtoRead = args.audiodir

	#check file exist
	if not os.path.exists(tfname):
		print("Time file not found!");
		exit(1);
	
	if not os.path.exists(pathtoRead):
		print("Directory not found!");
		exit(1);
			
	trimAudiotoVideo(tfname,pathtoRead)
	