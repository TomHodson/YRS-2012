import re
import string
def sanitiser(inqueue, outqueue, kill):
    while not kill == 1:
        try:
            tweetobj = inqueue.get(True)
        except IOError:
            return
        tweet = tweetobj.raw
        tweet = re.sub("[(){}\[\]]","",tweet)
        tweet = re.sub("[%s]*[%s]+[%s]+" % (string.ascii_letters, string.punctuation, string.ascii_letters),"",tweet)
        tweet = re.sub("[%s]" % string.punctuation, "",tweet)
        tweet = re.sub(" +"," ",tweet)
        tweetobj.body = tweet.lower().split()
        inqueue.task_done()
        outqueue.put(tweetobj)
