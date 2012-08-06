from collections import Counter

def merger(inqueue,outqueue):
    while True:
        tweetcache = []
        while len(tweetcache) < 100:
            tweetcache.append(inqueue.get(True))
        singles = [i.single for i in tweetcache]
        doubles = [i.double for i in tweetcache]
        print len(singles),len(doubles)
        singles = dict(sum((Counter(dict(x)) for x in singles),Counter()))
        doubles = dict(sum((Counter(dict(x)) for x in doubles),Counter()))
        outqueue.put((singles,doubles))
