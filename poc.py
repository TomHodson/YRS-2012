from downloader import downloader
from parser import parser
from multiprocessing import Process,Queue,Pool

inqueue = Queue()
outqueue = Queue()
p = Process(target = downloader, args=(inqueue,))
p.start()

parser(inqueue.get(True),outqueue)
p.terminate()
