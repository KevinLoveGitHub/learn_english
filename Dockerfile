FROM python:3

WORKDIR /root

RUN pip install scrapyd

EXPOSE 6800

USER root