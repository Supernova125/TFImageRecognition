from moviepy.editor import VideoFileClip
import PIL
import sys
import time
from os.path import basename
from os import makedirs
from toml import load as tload

config = tload('config.toml')

file_name = basename(sys.argv[1])
target_folder = ""
if "valorant" in file_name:
    target_folder = "valorant"
elif "minecraft" in file_name:
    target_folder = "minecraft"
else:
    target_folder = config["splitter"]["default_name"]
if len(sys.argv) > 2:
    target_folder = sys.argv[2]

makedirs(f"game_images/{target_folder}", exist_ok=True)

frame_output = f"game_images/{target_folder}/{file_name.removesuffix('.'+file_name.split('.')[-1])}-output-"

vid = VideoFileClip(sys.argv[1])
vid = vid.set_fps(config["splitter"]["fps"])
if vid.duration > 60*config["splitter"]["max_minutes"]:
    vid = vid.subclip(0,60*config["splitter"]["max_minutes"])

vid = vid.resize((config["splitter"]["movie_width"],config["splitter"]["movie_height"]) if not config["splitter"]["use_training_dims"] else (config["training"]["img_width"],config["training"]["img_height"]))

frames = int(vid.duration*vid.fps)
print("Frames to save: " + str(frames))
print("Duration: " + str(vid.duration))
print("FPS: " + str(vid.fps))
print("Resolution: " + str(vid.size))

print("Splitting "+file_name+" into "+target_folder+"\nPress enter to start! (Outputs to "+frame_output+"{frame_number}.jpg)")
input()

print("Starting...")

frame_number = 0
starttime = time.time()
info_done = True
for frame in vid.iter_frames():
    if (time.time() - starttime) % 10 <= 1 and not info_done:
        # every 10 seconds
        elapsed = time.time() - starttime
        remaining = elapsed * (frames / frame_number) - elapsed
        frames_a_sec = frame_number / elapsed
        print(f"{frame_number}/{frames} ({frame_number/frames*100:.2f}%) eta: {remaining:.2f}s with {frames_a_sec:.2f}fps")
        info_done = True
    elif (time.time() - starttime) % 10 > 1 and info_done:
        info_done = False
    frame_image = PIL.Image.fromarray(frame)
    frame_image.save(frame_output+f"{frame_number}.jpg")
    frame_number += 1

print("Done!")