from collections import Counter

def merger(inqueue,outqueue,kill):
    while not kill == 1:
        tweetcache = []
        while len(tweetcache) < 100:
            try:
                tweetcache.append(inqueue.get(True))
            except IOError:
                return
        singles = [i.single for i in tweetcache]
        doubles = [i.double for i in tweetcache]
        singles = dict(sum((Counter(dict(x)) for x in singles),Counter()))
        doubles = dict(sum((Counter(dict(x)) for x in doubles),Counter()))
        outqueue.put((singles,doubles))

if __name__ == '__main__':
	pass
	
