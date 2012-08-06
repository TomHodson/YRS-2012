from collections import defaultdict

def parser(tweet,outqueue):
    body = tweet.body.split()
    single = defaultdict(int)
    for word in body:
        single[word] += 1
    double = defaultdict(int)
    for i in range(len(body)-2):
        double[tuple(body[i:i+2])] += 1
    tweet.single = dict(single)
    tweet.double = dict(double)
    outqueue.put(tweet)
