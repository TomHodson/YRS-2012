import re
import string
def sanitiser(inqueue, outqueue, kill):
    "Removes punctuation, email addresses and links from the Tweet.raw, then tokenises it and puts it into Tweet.body"
    while not kill == 1:
        try:
            tweetobj = inqueue.get(True)
        except IOError:
            return
        tweet = tweetobj.raw
        tweet = re.sub("[(){}\[\]]","",tweet)
        tweet = re.sub("[%s]*[%s]+[%s]+" % (string.ascii_letters, string.punctuation.replace('#',''), string.ascii_letters),"",tweet)
        tweet = re.sub("[%s]" % string.punctuation.replace('#',''), "",tweet)
        tweet = re.sub(" +"," ",tweet)
        tweet = tweet.encode('ascii','ignore')
        if not tweet: continue
        tweetobj.body = tweet.lower().split()
        inqueue.task_done()
        outqueue.put(tweetobj)


if __name__ == '__main__':
    import time
    from multiprocessing import Process
    from multiprocessing import JoinableQueue as Queue
    class Tweet():
        def __init__(self):
                pass
    testtweet = Tweet()
    testtweet.raw = "oh a tricky)((*()one <end> <?DF test*test"
    inputqueue = Queue()
    inputqueue.put(testtweet)
    outputqueue = Queue()

    p = Process(target = sanitiser, args = (inputqueue, outputqueue, 0))
    p.start()
    inputqueue.join()
    p.terminate()
    out = outputqueue.get()
    print 'parser: len={}, {}, {}'.format(len(out.double), out.single, out.double) 
