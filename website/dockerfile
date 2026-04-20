# syntax=docker/dockerfile:1

FROM python:3.10


COPY app/ .

#COPY requirements.txt requirements.txt
#RUN apt-get update && apt-get install ffmpeg -y
RUN pip3 install -r requirements.txt

CMD ["python", "app.py"]
#CMD ["gunicorn"  , "-b", "0.0.0.0:8000" , "app:app"]