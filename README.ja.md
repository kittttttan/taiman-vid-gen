# タイマン動画ジェネレーター

[タイマン動画](https://twitter.com/NM_NANAPARTY/status/1248551793258139648)
の作成をスクリプト化できるか検証

目標:
提供素材動画に対して、自前の動画を横に並べて同時再生する
自前動画の音声は左をミュート、右のみ有効にする

PythonのMoviePyを利用してみた

検証環境： windows10, Python 3.7.4(miniconda), MoviePy==1.0.1

TODO: 自前動画の音声処理


# 準備
## MoviePyのインストール
condaかpipでインストール
```
# https://zulko.github.io/moviepy/
conda install -c conda-forge moviepy
# or pip install moviepy
```

もしくはDocker
(libav-tools→ffmpegなど一部修正が必要そう)
```
# https://zulko.github.io/moviepy/docker.html
# Dockerfile取得 https://github.com/Zulko/moviepy/blob/master/Dockerfile
docker build -t moviepy -f Dockerfile .
docker run -it moviepy bash
docker run -v /local/path/to/taiman-vid-gen:/data/taiman-vid-gen moviepy bash
```

## 修正 (1.0.1向け)
サブプロセスが処理中にクローズされるっぽいので応急処置
[AttributeError: 'NoneType' object has no attribute 'stdout' #938](https://github.com/Zulko/moviepy/issues/938)
```
# Lib\site-packages\moviepy\audio\io\readers.py
# FFMPEG_AudioReader#close_proc
def close_proc(self):
    return
```

# 使用例
```
# MoviePyの動作確認用
python test.py input.flv test.mp4

# デフォルト動作
python main.py nana.mp4 my-vid.mp4 taiman.mp4
# オプションの使用
python main.py nana.mp4 my-vid.mp4 taiman.mp4 -t "sample text" -p 1 -f -d
```
