from collections import defaultdict

def consecutiveparser(inqueue,outqueue):
    while True: #forever
        tweet = inqueue.get(True) #read tweet object
        body = tweet.body #get tweet data
        single = defaultdict(int)
        for word in body: #get count of single words
            single[word] += 1
        double = defaultdict(int)
        for i in range(len(body)-2): #get count of word pairs
            pair = body[i:i+2]
            pair.sort()
            pair = tuple(pair)
            double[pair] += 1
        tweet.single = dict(single)
        tweet.double = dict(double)
        outqueue.put(tweet) #output to new queue

from collections import defaultdict
from itertools import combinations

def intweetparser(inputqueue, outputqueue):
    while True:
        tweet  = inputqueue.get(block = True)
        words = defaultdict(int)
        wordwords = {}

        wordpairs = combinations(tweet.body, 2) #(word1, word2) where word1 != word2 and order does NOT matter
        for word in tweet.body:
            words[word] += 1

        for word1,word2 in wordpairs:
            wordwords.get(word1, defaultdict(int))[word2] += 1
        tweet.single, tweet.double = words, wordwords
        outputqueue.put(tweet)

parser = consecutiveparser

#doesn't work now that parser is an infinite loop
if __name__ == '__main__':
    from Queue import Queue
    from multiprocessing import Process
    class Tweet():
        def __init__(self):
                pass
    testtweet = Tweet()
    testtweet.body = ['this', 'is', 'a', 'test']
    inputqueue = Queue()
    inputqueue.put(testtweet)
    outputqueue = Queue()
