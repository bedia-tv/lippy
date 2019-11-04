import argparse
from moviepy.editor import *
import os
import json

base = os.path.dirname(__file__)

parser = argparse.ArgumentParser(description = 'make word gifs out of a video and its alignment')
parser.add_argument('video', type=str, help='location of video')
parser.add_argument('align', type=str, help='location of align')

args = parser.parse_args()

# Get video file and save it as moviepy clip
full_video = VideoFileClip(args.video)
print(full_video.duration)

# Load Gentle align into variable
align_text = open(args.align)
align = json.load(align_text)


# Where to store gifs?
folder_name = args.video.split('/')[-1]

folder_name = os.path.splitext(folder_name)[0]

if not os.path.exists('outputs'):
    os.mkdir('outputs')

gif_folder = os.path.join(base, 'outputs', folder_name)
os.mkdir(gif_folder)

for word in align['words']:
    start, end = word['start'], word['end']
    gif_fname = word['word'] + '-' + str(word['start']) + '.gif'
    print(gif_fname)
    gif_location = os.path.join(gif_folder, gif_fname)
    print(gif_location)

    word_gif = full_video.subclip(start, end)
    word_gif.write_gif(gif_location)




