from collections import defaultdict

def parser(inqueue,outqueue):
    while True: #forever
        tweet = inqueue.get(True) #read tweet object
        body = tweet.body.split() #get tweet data
        single = defaultdict(int)
        for word in body: #get count of single words
            single[word] += 1
        double = defaultdict(int)
        for i in range(len(body)-2): #get count of word pairs
            double[tuple(body[i:i+2])] += 1
        tweet.single = dict(single)
        tweet.double = dict(double)
        outqueue.put(tweet) #output to new queue
