FROM python:3.10-alpine as builder

RUN apk update && apk add --no-cache tzdata alpine-sdk openjpeg-dev zlib-dev jpeg-dev libffi-dev cairo-dev
ADD requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt && rm /tmp/requirements.txt

WORKDIR /stickers
ENV TZ=Asia/Shanghai

RUN apk update && apk add  --no-cache ffmpeg
COPY . /stickers

CMD ["/usr/local/bin/python","/stickers/main.py"]



