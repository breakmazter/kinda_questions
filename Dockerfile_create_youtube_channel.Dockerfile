FROM python:3.9.2

WORKDIR /create_youtube_channel

COPY create_youtube_channel_worker.py /create_youtube_channel/create_youtube_channel_worker.py
COPY settings.py /create_youtube_channel/settings.py
COPY requirements.txt /create_youtube_channel/requirements.txt
COPY actors_interface.py /create_youtube_channel/actors_interface.py

COPY db/crud.py /create_youtube_channel/db/crud.py
COPY db/models.py /create_youtube_channel/db/models.py

RUN pip install --upgrade pip
RUN python -m pip install --no-cache-dir -U 'dramatiq[rabbitmq, redis]'==1.11.0
RUN python -m pip install --no-cache-dir -r requirements.txt

CMD ["dramatiq", "-t 16", "create_youtube_channel_worker", "-Q", "josef_create_youtube_channel_josef"]
