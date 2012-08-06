import downloader
from multiprocessing import Process,Queue

queue = Queue()
p = Process(target = downloader.downloader, args=(queue,))
p.start()
while True:
    print queue.get(True).body
