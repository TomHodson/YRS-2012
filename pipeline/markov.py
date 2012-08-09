def markov(inqueue,killProc):
    while not killProc == 1:
        try:
            tweet = inqueue.get(True)
        except IOError:
            return
        print tweet.raw
