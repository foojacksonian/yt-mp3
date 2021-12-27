#!/usr/bin/env python3
"""
 Copyright 2021 Foo Jacksonian, Andrew Michaelis

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

 http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""
import sys
import os
import logging
import re
import argparse
import subprocess
from pathlib import Path
from pytube import YouTube
from pytube.exceptions import RegexMatchError as py_url_excpt
from mutagen.easyid3 import EasyID3


def get_audio_data(url, output_dir):
    """Routine attemps to get the 'best' audio from the url and downloads it.

       :param url: The YT url of interestk
       :param output_dir: The staging directory for the audio data.
       :returns:
            The path to the saved audio file
       :rtype: Path object
    """
    renum = re.compile(r'^(\d+)')
    # Get target stream, find max bits/sec
    try:
        yt_obj= YouTube(url)
        strms = yt_obj.streams.filter(only_audio=True, file_extension='mp4')
        bitrate, idx = -1, -1
        for i, strm in enumerate(strms):
            brate_grp = renum.search(strm.abr)
            if brate_grp and bitrate < int(brate_grp.group(1)):
                bitrate = int(brate_grp.group(1))
                idx = i
        if idx >= 0:
            # Now try to download the target stream
            logging.debug("Choosing stream %d (rate), %s", bitrate, strms[idx])
            dstream = yt_obj.streams.get_by_itag(strms[idx].itag)
            fpath = dstream.download(max_retries=4, output_path=output_dir)
            logging.debug("Downloaded \"%s\"", fpath)
            return Path(fpath)
        return None
    except py_url_excpt as pterr:
        logging.error("Bad URL %s : %s", url, str(pterr))
        sys.exit(1)
#get_audio_data


def convert(fpath, start=None):
    """Routine converts the audio data in fpath, usually mp4, to mp3.

       :param fpath: The input audio file to convert.
       :type fpath: Path Object
       :param start: The start offset, in seconds
       :type start: int
       :returns:
            The path to the saved mp3 audio file
       :rtype: Path object
    """
    # Clean up file name
    tpath = re.sub(r'&', 'and', re.sub(r'@', 'at', str(fpath.name)))
    astrans = str.maketrans(" (),", "____")
    tpath = tpath.translate(astrans)
    tpath = re.sub(r'(_)+', '_', tpath)
    m3_name = re.sub(r'\.mp4$', '.mp3', os.path.join(os.path.dirname(fpath), tpath))
    logging.debug("%s --> %s", fpath, m3_name)
    if not os.path.exists(fpath):
        logging.error("Unable to find input \"%s\"", fpath)
        sys.exit(1)
    # run ffmpeg, assume ffmpeg is in the user's path
    cmd = ['ffmpeg']
    if start is not None:
        cmd.extend(['-ss', str(start)])
    cmd.extend(['-i', str(fpath), '-vn', '-q:a', '0', '-y', '-acodec', 'mp3', m3_name])
    logging.debug("Converting via %s", " ".join(cmd))
    try:
        run_out = subprocess.run(cmd, capture_output=True, text=True, check=True)
        logging.debug("%s : %s", str(run_out.stdout), str(run_out.stderr))
        return Path(m3_name)
    except (subprocess.CalledProcessError, FileNotFoundError) as suberr:
        logging.error("%s", str(suberr))
        sys.exit(1)
#convert


def id3_update(fpath, song=None, artist=None, album=None, year=None):
    """Routine updates the ID3 mp3 metadata.

       :param song: The title
       :type song: str
       :param artist: The artist
       :type artist: str
       :param album: The album
       :type album: str
       :param year: The year. Must be YYYY
       :type year: str
    """
    au_file = EasyID3(fpath)
    if song:
        logging.debug("Adding title \"%s\"", song)
        au_file["title"] = song
    if artist:
        logging.debug("Adding artist \"%s\"", artist)
        au_file["artist"] = artist
    if album:
        logging.debug("Adding album \"%s\"", album)
        au_file["album"] = album
    if year and re.search(r'^(\d{4})$', year):
        logging.debug("Adding year \"%s\"", year)
        au_file["date"] = year
    au_file.save()
#id3_update


def main():
    """The main entry point."""
    parser = argparse.ArgumentParser(description='Trims and cleans up mp3 files')
    parser.add_argument('-s', default=0, type=int, help='Start time (second) of song')
    parser.add_argument('--verbose', '-v', default=False, action='store_true', \
                        help='Run in verbose mode')
    parser.add_argument('--song', default=None, type=str, help='Song ID3 metadata name')
    parser.add_argument('--artist', default=None, type=str, help='Artist ID3 metadata name')
    parser.add_argument('--album', default=None, type=str, help='Album ID3 metadata name')
    parser.add_argument('--year', default=None, type=str, help='Year ID3 metadata tag')
    parser.add_argument('--odir', default='.', type=str, help='The output directory')
    parser.add_argument('--clean', default=False, action='store_true', help='Clean up'+\
                        ' the downloaded intermediate file')
    parser.add_argument('uri', type=str, nargs=1, help='The path or YouTube URL of the song')
    args = parser.parse_args()

    if args.verbose is True:
        logr = logging.getLogger()
        logr.setLevel(logging.DEBUG)

    logging.debug("YT URI %s", args.uri[0])
    logging.debug("start time %d", args.s)
    logging.debug("ID3 metadata song \"%s\"", str(args.song))
    logging.debug("Output Directory \"%s\"", str(args.odir))

    if args.odir != '.' and not os.path.exists(args.odir):
        os.makedirs(args.odir)

    # get data
    path = get_audio_data(args.uri[0], args.odir)
    if path is None:
        logging.error("Unable to retrive required data from URL %s", args.uri[0])
        sys.exit(1)

    if args.s != 0:
        soffset = args.s
    else:
        soffset = None

    song_path = convert(path, soffset)

    # tag the output
    id3_update(song_path, song=args.song, artist=args.artist, album=args.album, year=args.year)

    if args.clean:
        os.unlink(path)
#main


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s:%(levelname)s - %(message)s')
    try:
        main()
    except KeyboardInterrupt as kyerr:
        logging.warning("Interrupted by user")
        sys.exit(1)
#__main__
