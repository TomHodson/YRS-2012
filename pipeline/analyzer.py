from collections import Counter, defaultdict, namedtuple
from itertools import combinations

def analyzer(inqueue,outqueue,kill):
    "Creates counts for individual and pairs of words and tracks various metrics"
    while not kill == 1: #forever
        try:
            tweet = inqueue.get(True) #read tweet object
        except IOError:
            return
        tweet.body #get tweet data

    #make singles data
    #IMPORTANT data is in the format {(word1) : [consecutive, intweetcount]}
        tweet.single = defaultdict(lambda :[0,0]) 
        for word in tweet.body: #get count of single words
            tweet.single[word][0] += 1
        for word in set(tweet.body):
            tweet.single[word][1] += 1

    #make doubles data
    #IMPORTANT data is in the format {(word1, word2) : [consecutive, intweetcount]}
        tweet.double = defaultdict(lambda :[0,0]) #initialise the double attribute
        #make consecutive data
        tagsadded = ['<start>'] + tweet.body + ['<end>'] 

        for i in range(len(tagsadded)-1): #get count of word pairs
            pair = tuple(tweet.body[i:i+2])
            tweet.double[pair][0] += 1
        #make intweetdata
        wordpairs = combinations(set(tweet.body), 2) #all the unordered ways of picking two words from the tweet where word1 != word2
        def f(x): 
            x = tuple(sorted(x))
            tweet.double[x][1] += 1
        map(f, wordpairs) 
            
        tweet.single = dict(tweet.single)
        tweet.double = dict(tweet.double)
        outqueue.put(tweet) #output to new queue
        inqueue.task_done()

#yay for testing OUT OF DATE
if __name__ == '__main__':
    import time
    from multiprocessing import Process
    from multiprocessing import JoinableQueue as Queue
    class Tweet():
        def __init__(self):
                pass
    testtweet = Tweet()
    testtweet.body = ['this', 'is', 'a', 'this']
    inputqueue = Queue()
    inputqueue.put(testtweet)
    outputqueue = Queue()

    p = Process(target = analyzer, args = (inputqueue, outputqueue, 0))
    p.start()
    inputqueue.join()
    p.terminate()
    out = outputqueue.get()
    print 'parser: len={}, {}, {}'.format(len(out.double), out.single, out.double) 
