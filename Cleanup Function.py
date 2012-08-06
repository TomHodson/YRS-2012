import re
import string
def cleanupfunction(tweet):
    tweet = tweet.translate(string.maketrans("","",),"(){}[]")
    tweet = re.sub("[%s]*[%s]+[%s]+" % (string.ascii_letters, string.punctuation, string.ascii_letters),"",tweet)
    tweet = tweet.translate(string.maketrans("","",),string.punctuation)
    tweet = re.sub(" +"," ",tweet)
    print tweet



cleanupfunction("ICT baan Amsterdam: Business Analist/Architect - (BI, processen, analyse, architectuur ) - Amsterdam http://bit.ly/R9UAOl #ict #vacature")    
