### Docker Image (experimental)

The __Dockerfile__ contains the information needed to build a basic environment that has all the
tools and libs required to run ytmp3, e.g. python 3.6, ffmpeg, etc. To build the image you must
have docker available, and then execute:

```
$ docker build -t ytmp3 .
```

To drop into the shell to run the program:

```
$ docker run -it ytmp3
```

