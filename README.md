# videoAudio_Spliter_Exporter
Python CMD Application to split video into chucnk based on the time interval and conver video to audio.
Convert single audio to video either based on the time stamps or full length. 
Converted video contains logo image at the beginning.

Time file as follows, (Assume that vedio file last long than 32 mins)

0:03:13-0:07:33

0:08:35-0:15:43

0:16:33-0:23:36

0:24:13-0:32:07

Program will split the video into provided time intervals. Here it will be 4 chunks.

-------------------------------------------------
Single audio to video option
Time file as follows,

0:00:13-0:07:33-01.file name 1

0:0:0-0:02:43-02.file name 2

03.file name 3


Program will convert to audio into video based on provided time intervals. 
It can be specified to convert in full length (without time interval). 