from downloader import downloader
from sanitiser import sanitiser
from analyzer import analyzer
from merger import merger
from inserter import inserter
from forker import forker
from markov import markov
from multiprocessing import Process,JoinableQueue,Value
import signal

def cleanup(signal,frame):
    killProc = 1
    
signal.signal(signal.SIGINT,cleanup)

fromDownloadQueue = JoinableQueue()
killProc = Value('d',0)
toSanitiser = JoinableQueue()
toMarkov = JoinableQueue()
fromSanitiserQueue = JoinableQueue()
fromAnalyzerQueue = JoinableQueue()
fromMergerQueue = JoinableQueue()

downloadert = Process(target = downloader, args=(fromDownloadQueue,killProc))
downloadert.start()

forkert = Process(target = forker, args=(fromDownloadQueue,toSanitiser,toMarkov,killProc))
forkert.start()

sanitisert = Process(target = sanitiser, args=(toSanitiser,fromSanitiserQueue,killProc))
sanitisert.start()
markovt = Process(target = markov, args=(toMarkov,killProc))
markovt.start()

analyzert = Process(target = analyzer, args=(fromSanitiserQueue,fromAnalyzerQueue,killProc))
analyzert.start()

mergert = Process(target = merger, args=(fromAnalyzerQueue,fromMergerQueue,killProc))
mergert.start()

insertert = Process(target = inserter, args=(fromMergerQueue,killProc))
insertert.start()
insertert.join()
