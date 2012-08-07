from collections import Counter, defaultdict

class Tweets:
    pass



def merger(inqueue,outqueue,kill):
    while not kill == 1:
        tweets = Tweets()
        tweets.singles = Counter()
        for _ in range(100):
            try:
                #tweetcache.append(inqueue.get(True))
                tweet = inqueue.get()
                tweets.singles += Counter(tweet.single) #this works because addition is defined for Counter objects
                tweets.doubles = defaultdict(lambda : [0, 0])
                for wordpair in tweet.double:
                    tweets.doubles[wordpair][0] += tweet.double[wordpair][0]
                    tweets.doubles[wordpair][1] += tweet.double[wordpair][1]
                tweets.doubles = dict(tweets.doubles)
            except IOError:
                return
        outqueue.put(tweets)

if __name__ == '__main__':
    from multiprocessing import JoinableQueue, Process

    class Tweet:
        pass
    testtweet = Tweet()
    testtweet.single = {'a': 1, 'word': 1, 'blah': 1, 'this': 1, 'is': 1, 'slajd': 1, 'test': 1}
    testtweet.double = {('is', 'this'): [0, 1], ('test', 'this'): [0, 1], ('is', 'blah'): [0, 1], ('slajd', 'is'): [0, 1], ('blah', 'a'): [0, 1], ('this', 'a'): [0, 1], ('word', 'slajd'): [1, 1], ('this', 'is'): [1, 1], ('test', 'word'): [0, 1], ('a', 'blah'): [0, 1], ('blah', 'test'): [0, 1], ('is', 'a'): [1, 1], ('test', 'a'): [0, 1], ('word', 'is'): [0, 1], ('blah', 'this'): [0, 1], ('a', 'this'): [0, 1], ('is', 'word'): [0, 1], ('test', 'blah'): [1, 1], ('a', 'test'): [1, 1], ('word', 'test'): [0, 1], ('this', 'blah'): [0, 1], ('blah', 'slajd'): [0, 1], ('slajd', 'word'): [0, 1], ('is', 'slajd'): [0, 1], ('word', 'this'): [0, 1], ('blah', 'is'): [0, 1], ('slajd', 'a'): [0, 1], ('word', 'blah'): [0, 1], ('a', 'slajd'): [0, 1], ('slajd', 'test'): [0, 1], ('test', 'is'): [0, 1], ('word', 'a'): [0, 1], ('slajd', 'this'): [0, 1], ('this', 'test'): [0, 1], ('test', 'slajd'): [0, 1], ('slajd', 'blah'): [0, 1], ('is', 'test'): [0, 1], ('a', 'is'): [0, 1], ('a', 'word'): [0, 1], ('this', 'slajd'): [0, 1], ('blah', 'word'): [1, 1], ('this', 'word'): [0, 1]}
    inqueue = JoinableQueue()
    outqueue = JoinableQueue()

    for _ in range(200):
        inqueue.put(testtweet)

    p = Process(target = merger, args = (inqueue, outqueue, 0))
    p.start()
    inqueue.join()
    p.terminate()
    out = outputqueue.get()
    print out

	

