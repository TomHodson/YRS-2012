from downloader import downloader
from sanitiser import sanitiser
from analyzer import analyzer
from merger import merger
from inserter import inserter
from forker import forker
from markov import markov
from multiprocessing import Process,JoinableQueue,Value,active_children
from time import sleep
from os import kill
from signal import SIGKILL

def cleanup():
    killProc = 1
    sleep(3)
    downloadert.terminate()
    forkert.terminate()
    markovt.terminate()
    sanitisert.terminate()
    analyzert.terminate()
    insertert.terminate()
    for i in active_children():
        kill(i.pid,SIGKILL)
    import sys;sys.exit()

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

raw_input("press any key to exit\n") #blocks
cleanup()
