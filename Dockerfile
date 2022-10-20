FROM python:3.10-alpine as builder

RUN apk update && apk add --no-cache tzdata alpine-sdk openjpeg-dev zlib-dev jpeg-dev libffi-dev
ADD requirements.txt /tmp/
RUN pip3 install --user -r /tmp/requirements.txt && rm /tmp/requirements.txt


FROM python:3.10-alpine
WORKDIR /stickers
ENV TZ=Asia/Shanghai

RUN apk update && apk add  --no-cache ffmpeg
COPY --from=builder /root/.local /usr/local
COPY --from=builder /usr/share/zoneinfo /usr/share/zoneinfo
COPY . /stickers

CMD ["/usr/local/bin/python","/stickers/main.py"]



