from collections import Counter

def consecutiveparser(inqueue,outqueue):
    while True: #forever
        tweet = inqueue.get(True) #read tweet object
        body = tweet.body #get tweet data
        single = Counter()
        for word in body: #get count of single words
            single[word] += 1
        double = Counter()
        for i in range(len(body)-1): #get count of word pairs
            pair = body[i:i+2]
            pair.sort()
            pair = tuple(pair)
            double[pair] += 1
        tweet.single = dict(single)
        tweet.double = dict(double)
        outqueue.put(tweet) #output to new queue

from collections import defaultdict, Counter
from itertools import combinations

def intweetparser(inputqueue, outputqueue):
    while True:
        tweet  = inputqueue.get(block = True)
        singles = Counter()
        doubles = Counter()
        
        for word in tweet.body:
            singles[word] += 1

        wordpairs = combinations(tweet.body, 2) #(word1, word2) where word1 != word2 and order does NOT matter
        for wordpair in wordpairs:
            doubles[wordpair] += 1
        tweet.single, tweet.double = singles, doubles
        outputqueue.put(tweet)

parser = consecutiveparser

#yay for testing
if __name__ == '__main__':
    import time
    from multiprocessing import Process, Queue
    class Tweet():
        def __init__(self):
                pass
    testtweet = Tweet()
    testtweet.body = ['this', 'is', 'a', 'test']
    inputqueue = Queue()
    inputqueue.put(testtweet)
    outputqueue = Queue()

    p = Process(target = consecutiveparser, args = (inputqueue, outputqueue))
    p.start()
    time.sleep(0.5) #DIRTY HACK
    p.terminate()
    print 'consecutiveparser:', outputqueue.get().double

    inputqueue = Queue()
    inputqueue.put(testtweet)
    outputqueue = Queue()

    p = Process(target = intweetparser, args = (inputqueue, outputqueue))
    p.start()
    time.sleep(0.5) #DIRTY HACK
    p.terminate()
    print 'intweetparser:', outputqueue.get().double
