FROM python:3.7-alpine

WORKDIR /app

USER root

RUN apk update && apk upgrade && apk add curl bash
RUN apk add build-base

# install build deps for bjoern
RUN apk add --no-cache --virtual .build-deps gcc musl-dev make
RUN apk add --no-cache libressl-dev
# need keep libev-dev
RUN apk add --no-cache libev-dev libffi-dev

COPY requirements.txt requirements.txt

ADD . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]
