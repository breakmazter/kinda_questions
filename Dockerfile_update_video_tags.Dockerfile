FROM python:3.9.2

WORKDIR /update_video_tags

COPY update_video_tags_worker.py /update_video_tags/update_video_tags_worker.py
COPY settings.py /update_video_tags/settings.py
COPY requirements.txt /update_video_tags/requirements.txt
COPY actors_interface.py /update_video_tags/actors_interface.py

COPY db/crud.py /update_video_tags/db/crud.py
COPY db/models.py /update_video_tags/db/models.py

COPY utils/clean_text.py /update_video_tags/utils/clean_text.py
COPY utils/proccesing_text.py /update_video_tags/utils/proccesing_text.py

RUN pip install --upgrade pip
RUN python -m pip install --no-cache-dir -U 'dramatiq[rabbitmq, redis]'==1.11.0
RUN python -m pip install --no-cache-dir -r requirements.txt
RUN python -m pip install --no-cache-dir emoji==1.2.0
RUN python -m pip install --no-cache-dir urlextract==1.2.0

CMD ["dramatiq", "-t 16", "update_video_tags_worker", "-Q", "josef_update_video_tags_josef"]
