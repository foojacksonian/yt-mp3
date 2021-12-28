FROM ubuntu:bionic
LABEL maintainer="Foo Jacksonian" \
      version="0.1.1" \
      description="This image definition is used to build a simple ytmp3 \
                  image that contains all the required stuff to run correctly."

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y python3 python3-pip \
            wget ffmpeg libavcodec-extra

RUN wget https://github.com/foojacksonian/yt-mp3/archive/refs/tags/v0.1.1.tar.gz && \
    tar xzvf v0.1.1.tar.gz && \
    cd yt-mp3-0.1.1 && \
    pip3 install . && \
    cd ../ && \
    rm -rf yt-mp3-0.1.1 && \
    rm -f v0.1.1.tar.gz

RUN useradd -c "yt user" -m ytusr
WORKDIR /home/ytusr
USER ytusr

CMD ["bash"]
