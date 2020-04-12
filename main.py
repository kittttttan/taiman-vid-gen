"""
Mixing clips by moviepy
"""

__author__ = 'kittttttan'
__version__ = '0.1.0'
__license__ = 'MIT'

import argparse
from os import path
import subprocess
from sys import exit, stdout

from moviepy.config import get_setting
from moviepy.editor import *

from logging import basicConfig, getLogger, DEBUG, INFO
logger = getLogger(__name__)

def main(args):
  logger.debug('args={}'.format(args))
  clips = []
  size = (0, 0)
  duration = 0
  pattern = args.pattern
  if pattern == 1:
    clips, size, duration = wipe(args)
  elif pattern == 2:
    clips, size, duration = horizon_crop(args)
  elif pattern == 3:
    clips, size, duration = vertical(args)
  else:
    clips, size, duration = horizon(args)

  text = args.text
  if text:
    logger.debug('show text: {}'.format(text))
    text_clip = (TextClip(text, color='white', fontsize=12)
        .set_duration(duration)
        .set_position(('right','bottom'))
    )
    clips.append(text_clip)

  video = CompositeVideoClip(clips, size)

  if args.debug:
    video = video.subclip(0,10)
  # video.write_videofile(dest)
  video.write_videofile(args.dest, remove_temp=False)

def pan(args):
  src = args.src
  if not args.pan:
    return src
  split = path.splitext(src)
  panned = split[0] + '-panned' + split[1]
  cmd = [
    get_setting('FFMPEG_BINARY'),
    '-i', src,
    '-af', 'pan=stereo|c1=c0',
    '-c:v', 'copy', panned,
  ]
  logger.debug(cmd)
  res = subprocess.run(cmd, stdout=subprocess.PIPE)
  stdout.buffer.write(res.stdout)
  return panned

def horizon(args):
  logger.debug('horizon')
  clips = []
  frame_width, frame_height = (int(s) for s in args.size.split('x'))

  src = pan(args)
  clip = VideoFileClip(src).resize(width=frame_width//2).set_pos('right')
  clips.append(clip)
  width, height = clip.size
  duration = clip.duration

  nana_clip = VideoFileClip(args.nana).resize(width=frame_width//2)
  nana_clip = nana_clip.set_pos('left')
  clips.append(nana_clip)

  return clips, (frame_width, frame_height), duration

def vertical(args):
  logger.debug('vertical')
  clips = []
  frame_width, frame_height = (int(s) for s in args.size.split('x'))

  src = pan(args)
  clip = VideoFileClip(src).resize(height=frame_height//2).set_pos('bottom')
  clips.append(clip)
  width, height = clip.size
  duration = clip.duration

  nana_clip = VideoFileClip(args.nana).resize(height=frame_height//2)
  nana_clip = nana_clip.set_pos('top')
  clips.append(nana_clip)

  return clips, (frame_width, frame_height), duration

def horizon_crop(args):
  logger.debug('horizon_crop')
  clips = []
  frame_width, frame_height = (int(s) for s in args.size.split('x'))

  src = pan(args)
  clip = VideoFileClip(src).resize(width=frame_width).set_pos('right')
  width, _ = clip.size
  clip = clip.crop(x1 = width // 4, width = width // 2)
  clips.append(clip)
  width, height = clip.size
  duration = clip.duration

  nana_clip = VideoFileClip(args.nana).resize(width=frame_width)
  nana_clip = nana_clip.set_pos('left')
  width, _ = nana_clip.size
  nana_clip = nana_clip.crop(x1 = width // 4, width = width // 2)
  clips.append(nana_clip)

  return clips, (frame_width, frame_height), duration


def wipe(args):
  logger.debug('wipe')
  clips = []
  frame_width, frame_height = (int(s) for s in args.size.split('x'))

  src = pan(args)
  clip = VideoFileClip(src).resize(width=frame_width).set_position(('right','bottom'))
  clips.append(clip)
  width, height = clip.size
  duration = clip.duration

  nana_clip = VideoFileClip(args.nana).resize(width=120).set_position((10,10))
  clips.append(nana_clip)

  return clips, clip.size, duration


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('nana', help='path to nana')
  parser.add_argument('src', help='path to source')
  parser.add_argument('dest', help='path to destination')
  parser.add_argument('-p', '--pattern', type=int, default=0, help='1:wipe, 2:horizon_crop, 3:vertical, other:horizon')
  parser.add_argument('-t', '--text', default='', help='show text (required ImageMagick)')
  parser.add_argument('-s', '--size', default='320x240', help='size of video frame: ex. 320x240')
  parser.add_argument('-f', '--force', action='store_true', help='no confirm')
  parser.add_argument('-d', '--debug', action='store_true', help='for debug')
  parser.add_argument('-P', '--pan', action='store_true', help='panning')
  args = parser.parse_args()

  basicConfig(level=DEBUG if args.debug else INFO)

  dest = args.dest
  if not args.force and path.exists(dest):
    print('already exists: {}'.format(dest))
    confirm = input('Continue? - [y/n]')
    if not (confirm.upper() in ['Y', 'YES']):
      print('canceled')
      exit(0)

  main(args)
