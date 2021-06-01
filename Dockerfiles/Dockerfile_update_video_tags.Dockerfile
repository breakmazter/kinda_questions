FROM python:3.9.2-slim-buster

WORKDIR /update_video_tags

COPY ../update_video_tags_worker.py /update_video_tags/update_video_tags_worker.py
COPY ../settings.py /update_video_tags/settings.py
COPY ../requirements/update_video_tags_requirements.txt /update_video_tags/update_video_tags_requirements.txt
COPY ../actors_interface.py /update_video_tags/actors_interface.py

COPY ../db/crud.py /update_video_tags/db/crud.py
COPY ../db/models.py /update_video_tags/db/models.py

RUN pip install --upgrade pip
RUN python -m pip install --no-cache-dir -U 'dramatiq[rabbitmq, redis]'==1.11.0
RUN python -m pip install -r update_video_tags_requirements.txt
RUN python -m pip install psycopg2-binary==2.8.6

CMD ["dramatiq", "-p 8", "-t 8", "update_video_tags_worker", "-Q", "josef_update_video_tags_josef"]
