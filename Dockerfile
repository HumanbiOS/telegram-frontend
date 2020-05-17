FROM docker.io/alpine:3.11

RUN apk add --no-cache \
      py3-aiohttp \
      py3-magic \
      #hbmqtt
          py3-yaml \
      py3-idna \
      py3-cffi \
      su-exec

COPY . app/
WORKDIR /app
# Bulk install build deps
RUN apk --no-cache add lapack libstdc++ libressl-dev musl-dev libffi-dev\
 && apk add --virtual .build-deps python3-dev libffi-dev build-base g++ gcc gfortran musl-dev lapack-dev \
 && pip3 install --upgrade pip wheel \
 && pip3 install -r requirements.txt \
 && apk del .build-deps
# Launch
CMD python3 ./interface.py
