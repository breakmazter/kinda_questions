import os
from queue import Queue
from threading import Thread

tasks = (
    'cmd /k "cloud_sql_proxy -instances=oximain:us-central1:oc-video-products-clone-3=tcp:5434"',
    'cmd /k "cloud_sql_proxy -instances=oximain:us-central1:iosif-mazan-db-testing-aaa=tcp:5435"'
)


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
