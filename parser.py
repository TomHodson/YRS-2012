from collections import Counter, defaultdict, namedtuple
from itertools import permutations

def parser(inqueue,outqueue,kill):
    while not kill == 1: #forever
        try:
            tweet = inqueue.get(True) #read tweet object
        except IOError:
            print "parser out"
            return
        tweet.body #get tweet data

    #make singles data
        tweet.single = Counter()
        for word in tweet.body: #get count of single words
            tweet.single[word] += 1

    #make doubles data
    #IMPORTANT data is in the format {(word1, word2) : [consecutive, intweetcount]}
        tweet.double = defaultdict(lambda :[0,0]) #initialise the double attribute
        #make consecutive data    
        for i in range(len(tweet.body)-1): #get count of word pairs
            pair = tuple(tweet.body[i:i+2])
            tweet.double[pair][0] += 1
        #make intweetdata
        wordpairs = permutations(tweet.body, 2) #all the ways of picking two words from the tweet where word1 != word2
        def f(x): tweet.double[x][1] += 1
        map(f, wordpairs) #using fp here for the lulz
            
        tweet.single = dict(tweet.single)
        tweet.double = dict(tweet.double)
        outqueue.put(tweet) #output to new queue
        inqueue.task_done()

#yay for testing
if __name__ == '__main__':
    import time
    from multiprocessing import Process
    from multiprocessing import JoinableQueue as Queue
    class Tweet():
        def __init__(self):
                pass
    testtweet = Tweet()
    testtweet.body = ['this', 'is', 'a', 'test', 'blah', 'word', 'slajd']
    inputqueue = Queue()
    inputqueue.put(testtweet)
    outputqueue = Queue()

    p = Process(target = parser, args = (inputqueue, outputqueue, 0))
    p.start()
    inputqueue.join()
    p.terminate()
    out = outputqueue.get()
    print 'parser: len={}, {}, {}'.format(len(out.double), out.single, out.double) 