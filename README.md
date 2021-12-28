# yt-mp3

The ytmp3 program downloads, trims, encodes and tags songs from YouTube.
The program relies on [pytube](https://github.com/pytube/pytube),
a modern [ffmpeg](https://ffmpeg.org/), and [mutagen](https://mutagen.readthedocs.io/en/latest/#)
to work. Python 3.6 or greater is required.

### Installation

Currently, the simplest way to install the uiltity is to download a
[release from GitHub](https://github.com/foojacksonian/yt-mp3/releases) and:

```
$ tar xzvf yt-mp3-0.1.0.tar.gz
$ cd yt-mp3-0.1.0
$ pip3 install .
```

from within the unpacked package. Pip will attempt to install the python dependencies.
Note, ffmpeg must be installed and in the user's path before using ytmp3.


### Usage

See the help message for more invocation details:

```
$ ytmp3.py -h
usage: ytmp3.py [-h] [-s S] [--verbose] [--song SONG] [--artist ARTIST]
                [--album ALBUM] [--year YEAR] [--odir ODIR] [--clean]
                [--gain GAIN]
                uri

Downloads, trims, encodes and tags songs from YouTube.

positional arguments:
  uri              The path or YouTube URL of the song

optional arguments:
  -h, --help       show this help message and exit
  -s S             Start time (second) of song
  --verbose, -v    Run in verbose mode
  --song SONG      Song ID3 metadata name
  --artist ARTIST  Artist ID3 metadata name
  --album ALBUM    Album ID3 metadata name
  --year YEAR      Year ID3 metadata tag
  --odir ODIR      The output directory
  --clean          Clean up the downloaded intermediate file
  --gain GAIN      Apply audio gain (units are dB)
```

Example invocations:

```
$ ytmp3.py -v -s 6 --song "Shadows"  \
                   --artist "Astrix & Simon Patterson" \
                   --year 2014 \
                   --clean \
                   --odir tmp \
                   "https://www.youtube.com/watch?v=d19CLhpmmXg"

```

Applying gain:

```
$ ytmp3.py -v --song "No Good (Start the Dance)" \
              --artist "Prodigy" \
              --album "No Good (Start the Dance)" \
              --year 1994 \
              --odir tmp \
              --gain 10 \
              "https://www.youtube.com/watch?v=svJvT6ruolA"
```

