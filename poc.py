import downloader
from multiprocessing import Process,Queue,Pool
from collections import defaultdict

inqueue = Queue()
outqueue = Queue()
p = Process(target = downloader.downloader, args=(inqueue,))
p.start()

def parser(tweet):
    body = tweet.body.split()
    single = defaultdict(int)
    for word in body:
        single[word] += 1
    double = defaultdict(int)
    for i in range(len(body)-2):
        double[tuple(body[i:i+2])] += 1
    tweet.single = single
    tweet.double = double
    outqueue.put(tweet)

parser(inqueue.get(True))
#print outqueue.get(True)
p.terminate()
