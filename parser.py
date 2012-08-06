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
        words = sorted(tweet.body)
        tweet.single = Counter()
        tweet.double = Counter()
        
        for word in words:
            tweet.single[word] += 1

        wordpairs = combinations(words, 2) #(word1, word2) where word1 != word2 and order does NOT matter
        def f(x): tweet.double[x] += 1
        map(f, wordpairs)
        tweet.single, tweet.double = dict(tweet.single), dict(tweet.double)
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
    testtweet.body = ['this', 'is', 'a', 'test', 'blah', 'word', 'slajd']
    inputqueue = Queue()
    inputqueue.put(testtweet)
    outputqueue = Queue()

    p = Process(target = consecutiveparser, args = (inputqueue, outputqueue))
    p.start()
    time.sleep(0.5) #DIRTY HACK
    p.terminate()
    out = outputqueue.get()
    print 'intweetparser: len={}, {}, {}'.format(len(out.double), out.single, out.double) 

    inputqueue = Queue()
    inputqueue.put(testtweet)
    outputqueue = Queue()

    p = Process(target = intweetparser, args = (inputqueue, outputqueue))
    p.start()
    time.sleep(0.5) #DIRTY HACK
    p.terminate()
    out = outputqueue.get()
    print 'intweetparser: len={}, {}, {}'.format(len(out.double), out.single, out.double)
