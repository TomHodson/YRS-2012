import re
import string
def sanitiser(inqueue, outqueue):
    while True:
        tweetobj = inqueue.get(True)
        tweet = tweetobj.body
        tweet = re.sub("[(){}\[\]]","",tweet)
        tweet = re.sub("[%s]*[%s]+[%s]+" % (string.ascii_letters, string.punctuation, string.ascii_letters),"",tweet)
        tweet = re.sub("[%s]" % string.punctuation, "",tweet)
        tweet = re.sub(" +"," ",tweet)
        tweetobj.body = tweet.lower().split()
        inqueue.task_done()
        outqueue.put(tweetobj)
