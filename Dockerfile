FROM python:3.11

ENV PYTHONUNBUFFERED True

COPY requirements.txt ./

RUN pip install -r requirements.txt

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY src/ ./src/

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 src.main:app