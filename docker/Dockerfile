ARG YTMVER=0.1.2
FROM ubuntu:bionic
ARG YTMVER
LABEL maintainer="Foo Jacksonian" \
      version="${YTMVER}" \
      description="This image definition is used to build a simple ytmp3 \
                  image that contains all the required stuff to run correctly."

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y python3 python3-pip \
            wget ffmpeg libavcodec-extra

RUN wget https://github.com/foojacksonian/yt-mp3/archive/refs/tags/v${YTMVER}.tar.gz && \
    tar xzvf v${YTMVER}.tar.gz && \
    cd yt-mp3-${YTMVER} && \
    pip3 install . && \
    cd ../ && \
    rm -rf yt-mp3-${YTMVER} && \
    rm -f v${YTMVER}.tar.gz

RUN useradd -c "yt user" -m ytusr
WORKDIR /home/ytusr
USER ytusr

CMD ["bash"]
