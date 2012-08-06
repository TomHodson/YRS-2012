from downloader import downloader
from sanitiser import sanitiser
from parser import parser
from multiprocessing import Process,Queue,Pool

def cleanup(signal,frame):
    downloadert.terminate()
    sanitisert.terminate()
    parsert.terminate()

fromDownloadQueue = Queue()
fromSanitiserQueue = Queue()
fromParserQueue = Queue()

downloadert = Process(target = downloader, args=(fromDownloadQueue,))
downloadert.start()

sanitisert = Process(target = sanitiser, args=(fromDownloadQueue,fromSanitiserQueue))
sanitisert.start()

parsert = Process(target = parser, args=(fromSanitiserQueue,fromParserQueue))
parsert.start()

while True:
    print fromParserQueue.get(True).single
