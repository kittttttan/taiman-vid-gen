"""
Test for moviepy

python test.py src dest
"""
from sys import argv, exit
from os import path
from moviepy.editor import VideoFileClip

def test(src, dest):
  clip = VideoFileClip(src).subclip(0,7).resize(width=120)
  clip.write_videofile(dest, audio=True, remove_temp=False)
  # clip.write_videofile(dest)

if __name__ == '__main__':
  args = argv
  if len(args) < 3:
    print(__doc__)
  else:
    src, dest = args[1:3]
    # if path.exists(dest):
    #   print('already exists: {}'.format(dest))
    #   confirm = input('Continue? - [y/n]')
    #   if not (confirm.upper() in ['Y', 'YES']):
    #     print('canceled')
    #     exit(0)
    test(src, dest)
