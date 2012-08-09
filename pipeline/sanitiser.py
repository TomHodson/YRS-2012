import re
import string
def sanitiser(inqueue, outqueue, kill):
    "Removes punctuation, email addresses and links from the Tweet.raw, then tokenises it and puts it into Tweet.body"
    punctuation = string.punctuation.replace('#','').replace('.','')
    while not kill == 1:
        try:
            tweetobj = inqueue.get(True)
        except IOError:
            return
        tweet = tweetobj.raw
        print tweet
        tweet = re.sub("[(){}\[\].]","",tweet)
        print tweet
        tweet = re.sub("[%s]*[%s]+[%s]+" % (string.ascii_letters, punctuation, string.ascii_letters),"",tweet)
        print tweet
        tweet = re.sub("[%s]" % punctuation, "",tweet)
        print tweet
        tweet = re.sub(" +"," ",tweet)
        print tweet
        tweet = tweet.encode('ascii','ignore')
        print tweet
        if not tweet: continue
        tweetobj.consec = tweet.lower()
        #tweet = tweet.replace('.','')
        tweetobj.body = tweet.lower().split()
        tweetobj.intweet = set(tweetobj.body)
        tweetobj.consec = tweetobj.consec.replace(".","<end> <start>").split()
        tweetobj.consec = ["<start>"]+tweetobj.consec+["<end>"]
        outqueue.put(tweetobj)
        inqueue.task_done()


if __name__ == '__main__':
    from multiprocessing import JoinableQueue, Process, Value

    class Tweet:
        pass
    testtweet = Tweet()
    testtweet.raw = "oh a tricky)((*()one <end> <?DF test.test"
    inqueue = JoinableQueue()
    inqueue.put(testtweet)
    outqueue = JoinableQueue()
    flag = Value('d',0)

    p = Process(target = sanitiser, args = (inqueue, outqueue, flag))
    p.start()
    inqueue.join()
    flag = 1
    inqueue.put(testtweet)
    out = outqueue.get()
    print 'consec', out.consec
    print 'intweet', out.intweet
