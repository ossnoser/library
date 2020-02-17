FROM python:3.6-alpine

RUN adduser -D library

WORKDIR /home/library

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn pymysql

COPY app app
COPY migrations migrations
COPY library.py config.py boot.sh ./
RUN chmod a+x boot.sh

ENV FLASK_APP library.py

RUN chown -R library:library ./
USER library

RUN ls

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]