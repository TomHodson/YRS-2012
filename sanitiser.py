import re
import string
def sanitiser(inqueue, outqueue):
    while True:
        tweetobj = inqueue.get(True)
        tweet = tweetobj.body
        #tweet = tweet.translate(string.maketrans("","",),"(){}[]")
        tweet = re.sub("[(){}\[\]]","",tweet)
        tweet = re.sub("[%s]*[%s]+[%s]+" % (string.ascii_letters, string.punctuation, string.ascii_letters),"",tweet)
        #tweet = tweet.translate(string.maketrans("","",),string.punctuation)
        tweet = re.sub("[%s]" % string.punctuation, "",tweet)
        tweet = re.sub(" +"," ",tweet)
        tweetobj.body = tweet
        outqueue.put(tweetobj)
