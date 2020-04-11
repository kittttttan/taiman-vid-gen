# Taiman Vids Generator

Mixing clips for `taiman`

see:
https://twitter.com/NM_NANAPARTY/status/1248551793258139648


# Requirements
## Install MoviePy
install
```
# https://zulko.github.io/moviepy/
conda install -c conda-forge moviepy
# or pip install moviepy
```

or Docker
```
# https://github.com/Zulko/moviepy/blob/master/Dockerfile
# download https://github.com/Zulko/moviepy/blob/master/Dockerfile
docker build -t moviepy -f Dockerfile .
docker run -it moviepy bash
docker run -v D:/Documents/develop/project/movie:/data/movie moviepy bash
```

## fix (for 1.0.1)
[AttributeError: 'NoneType' object has no attribute 'stdout' #938](https://github.com/Zulko/moviepy/issues/938)
```
# Lib\site-packages\moviepy\audio\io\readers.py
# FFMPEG_AudioReader#close_proc
def close_proc(self):
    return
```

# Example
```
# Is MoviePy available?
python test.py input.flv test.mp4

# run default
python main.py nana.mp4 my-vid.mp4 taiman.mp4
# run with options
python main.py nana.mp4 my-vid.mp4 taiman.mp4 -t "sample text" -p 1 -f -d
```
