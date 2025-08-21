FROM python:3.11.13-alpine

COPY ./requirements.txt /tmp/requirements.txt

RUN pip3 install -r /tmp/requirements.txt

COPY ./app/ /app/

ENTRYPOINT [ "/usr/local/bin/python3", "/app/" ]
