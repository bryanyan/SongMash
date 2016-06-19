# Adds captions to the individual word clips.
# Overwrites the original un-captioned clips

import os
from moviepy.editor import *
    
    
current_path = os.path.dirname(os.path.abspath(__file__))
direct = os.path.join(current_path, "TED")
direct = os.path.join(direct, "word_clips")

for filename in os.listdir(direct):
    # if not filename == "lynne.mp4": continue
    if filename[0] == ".": continue
    full_file = os.path.join(direct, filename)
    print full_file
    video = VideoFileClip(full_file)
    text = (TextClip(filename[:len(filename)-4], fontsize=36, color="white")).set_position(("center", "bottom")).set_duration(video.duration)
    result = CompositeVideoClip([video, text])
    result.write_videofile(full_file, temp_audiofile="temp-audio.m4a", remove_temp=True, codec="libx264", audio_codec="aac")
