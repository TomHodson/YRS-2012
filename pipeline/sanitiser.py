import re
import string
def sanitiser(inqueue, outqueue, kill):
    "Removes punctuation, email addresses and links from the Tweet.raw, then tokenises it and puts it into Tweet.body"
    punctuation = string.punctuation.replace('#','').replace('.','')
    while not kill == 1:
        try:
            tweetobj = inqueue.get(True)
        except IOError:
            return
        tweet = tweetobj.raw
        tweet = re.sub("[(){}\[\].]","",tweet)
        tweet = re.sub("[%s]*[%s]+[%s]+" % (string.ascii_letters, punctuation, string.ascii_letters),"",tweet)
        tweet = re.sub("[%s]" % punctuation, "",tweet)
        tweet = re.sub(" +"," ",tweet)
        tweet = tweet.encode('ascii','ignore')
        if not tweet: continue
        tweetobj.consec = tweet.lower()
        tweet = tweet.replace('.','')
        tweetobj.body = tweet.lower().split()
        tweetobj.intweet = set(tweetobj.body)
        tweetobj.consec = tweetobj.consec.replace(".","<end> <start>").split()
        tweetobj.consec = ["<start>"]+tweetobj.consec+["<end>"]
        outqueue.put(tweetobj)
        inqueue.task_done()
