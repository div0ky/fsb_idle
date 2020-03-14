from queue import Queue
from threading import Thread, Lock


def do_stuff(q):
    job_lock = Lock()
    while True:
        with job_lock:
            print( q.get() )
            q.task_done()

q = Queue()
num_threads = 20

for i in range(num_threads):
    worker = Thread(target=do_stuff, args=(q,), daemon=True).start()

for y in range (10000):
    for x in range(100):
        q.put(x + y * 100)
    q.join()
    print( "Batch " + str(y) + " Done" )