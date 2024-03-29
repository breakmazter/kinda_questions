FROM python:3.9.2

WORKDIR /create_youtube_video

COPY create_youtube_video_worker.py /create_youtube_video/create_youtube_video_worker.py
COPY settings.py /create_youtube_video/settings.py
COPY requirements.txt /create_youtube_video/requirements.txt
COPY actors_interface.py /create_youtube_video/actors_interface.py

COPY db/crud.py /create_youtube_video/db/crud.py
COPY db/models.py /create_youtube_video/db/models.py

RUN pip install --upgrade pip
RUN python -m pip install --no-cache-dir -U 'dramatiq[rabbitmq, redis]'==1.11.0
RUN python -m pip install --no-cache-dir -r requirements.txt

CMD ["dramatiq", "-t 8", "create_youtube_video_worker", "-Q", "josef_create_youtube_video_josef"]
