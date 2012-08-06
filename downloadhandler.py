from downloader import downloader
from multiprocessing import Process,Queue

rawtweets = Queue()
downloaderp = Process(target = downloader, args=(rawtweets,))
sanitiserp = Process(target = sansi)
while True:
    print queue.get(True).body
