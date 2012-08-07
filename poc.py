from downloader import downloader
from sanitiser import sanitiser
from parser import parser
from merger import merger
from multiprocessing import Process,JoinableQueue,Value
import signal

def cleanup(signal,frame):
    killProc = 1
    fromDownloadQueue.join()
    downloadert.terminate()
    fromSanitiserQueue.join()
    sanitisert.terminate()
    fromMergerQueue.join()
    mergert.terminate()

signal.signal(signal.SIGINT,cleanup)

fromDownloadQueue = JoinableQueue()
killProc = Value(0)
fromSanitiserQueue = JoinableQueue()
fromParserQueue = JoinableQueue()
fromMergerQueue = JoinableQueue()

downloadert = Process(target = downloader, args=(fromDownloadQueue,killProc))
downloadert.start()

sanitisert = Process(target = sanitiser, args=(fromDownloadQueue,fromSanitiserQueue))
sanitisert.start()

parsert = Process(target = parser, args=(fromSanitiserQueue,fromParserQueue))
parsert.start()

mergert = Process(target = merger, args=(fromParserQueue,fromMergerQueue))
mergert.start()

while True:
    print fromMergerQueue.get(True)
