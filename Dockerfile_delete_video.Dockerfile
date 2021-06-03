FROM python:3.9.2

WORKDIR /delete_video

COPY delete_video_worker.py /delete_video/delete_video_worker.py
COPY settings.py /delete_video/settings.py
COPY requirements/requirements.txt /delete_video/requirements.txt
COPY actors_interface.py /delete_video/actors_interface.py

COPY db/crud.py /delete_video/db/crud.py
COPY db/models.py /delete_video/db/models.py

RUN pip install --upgrade pip
RUN python -m pip install --no-cache-dir -U 'dramatiq[all]'==1.11.0
RUN python -m pip install --no-cache-dir -r requirements.txt

CMD ["dramatiq", "-p 8", "-t 8", "delete_video_worker", "-Q", "josef_delete_video_josef"
