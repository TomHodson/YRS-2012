from downloader import downloader
from sanitiser import sanitiser
from parser import parser
from merger import merger
from multiprocessing import Process,Queue
import signal

def cleanup(signal,frame):
    downloadert.terminate()
    sanitisert.terminate()
    parsert.terminate()
signal.signal(signal.SIGINT,cleanup)

fromDownloadQueue = Queue()
fromSanitiserQueue = Queue()
fromParserQueue = Queue()
fromMergerQueue = Queue()

downloadert = Process(target = downloader, args=(fromDownloadQueue,))
downloadert.start()

sanitisert = Process(target = sanitiser, args=(fromDownloadQueue,fromSanitiserQueue))
sanitisert.start()

parsert = Process(target = parser, args=(fromSanitiserQueue,fromParserQueue))
parsert.start()

mergert = Process(target = merger, args=(fromParserQueue,fromMergerQueue))
mergert.start()

while True:
    print fromMergerQueue.get(True)
