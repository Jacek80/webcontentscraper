FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /webcontentscraper
WORKDIR /webcontentscraper
ADD requirements.txt /webcontentscraper/
RUN pip install -r requirements.txt
ADD . /webcontentscraper/
