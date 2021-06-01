FROM python:3.9.2-slim-buster

WORKDIR /delete_video

COPY ../delete_video_worker.py /delete_video/delete_video_worker.py
COPY ../settings.py /delete_video/settings.py
COPY ../requirements/delete_video_requirements.txt /delete_video/delete_video_requirements.txt
COPY ../actors_interface.py /delete_video/actors_interface.py

COPY ../db/crud.py /delete_video/db/crud.py
COPY ../db/models.py /delete_video/db/models.py

RUN pip install --upgrade pip
RUN python -m pip install --no-cache-dir -U 'dramatiq[rabbitmq, redis]'==1.11.0
RUN python -m pip install -r delete_video_requirements.txt
RUN python -m pip install psycopg2-binary==2.8.6

CMD ["dramatiq", "-p 8", "-t 8", "delete_video_worker", "-Q", "josef_delete_video_josef"]