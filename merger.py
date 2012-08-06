def merger(inqueue,outqueue):
    tweetcache = []
    while len(tweetcache) < 100:
        tweetcache.append(inqueue.get(True))
    print len(tweetcache)
