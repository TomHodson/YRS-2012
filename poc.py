from downloader import downloader
from sanitiser import sanitiser
from parser import parser
from merger import merger
from inserter import inserter
from multiprocessing import Process,JoinableQueue,Value
import signal

def cleanup(signal,frame):
    killProc = 1
    
signal.signal(signal.SIGINT,cleanup)

fromDownloadQueue = JoinableQueue()
killProc = Value('d',0)
fromSanitiserQueue = JoinableQueue()
fromParserQueue = JoinableQueue()
fromMergerQueue = JoinableQueue()

downloadert = Process(target = downloader, args=(fromDownloadQueue,killProc))
downloadert.start()

sanitisert = Process(target = sanitiser, args=(fromDownloadQueue,fromSanitiserQueue,killProc))
sanitisert.start()

parsert = Process(target = parser, args=(fromSanitiserQueue,fromParserQueue,killProc))
parsert.start()

mergert = Process(target = merger, args=(fromParserQueue,fromMergerQueue,killProc))
mergert.start()

insertert = Process(target = inserter, args=(fromMergerQueue,killProc))
insertert.start()
insertert.join()
