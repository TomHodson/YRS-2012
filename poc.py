import downloader
from multiprocessing import Process,Queue,Pool
from collections import defaultdict

inqueue = Queue()
outqueue = Queue()
p = Process(target = downloader.downloader, args=(inqueue,))
p.start()

def parser(tweet):
    global outqueue
    body = tweet.body
    d = defaultdict(int)
    for word in body.split():
        d[word] += 1
    singlewords = d
    #outqueue.put(d)

parser(inqueue.get(True))
print outqueue.get(True)
p.terminate()
