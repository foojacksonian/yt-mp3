# yt-mp3

The ytmp3 program downloads, trims, encodes and tags songs from YouTube.
The program relies on [pytube](https://github.com/pytube/pytube),
[ffmpeg](https://ffmpeg.org/), and [mutagen](https://mutagen.readthedocs.io/en/latest/#)
to work.


### Usage

See the help message for more detailed invocation details:

```
$ ytmp3.py -h
```

Example invocation:

```
$ ytmp3.py -v -s 6 --song "Shadows"  \
                   --artist "Astrix & Simon Patterson" \
                   --year 2014 \
                   --clean \
                   --odir tmp \
                   https://www.youtube.com/watch?v=d19CLhpmmXg

```

