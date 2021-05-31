import os
from queue import Queue
from threading import Thread

tasks = ('cmd /k "cloud_sql_proxy -instances=oximain:us-central1:oc-video-products-clone-3=tcp:5433"',
         'cmd /k "cloud_sql_proxy -instances=krokai-gav:us-central1:iosif=tcp:5432"')


def worker():
    while True:
        item = q.get()
        os.system(item)


q = Queue()
for i in tasks:
    t = Thread(target=worker)
    t.setDaemon(True)
    t.start()

for item in tasks:
    q.put(item)

q.join()
