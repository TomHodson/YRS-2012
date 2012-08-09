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
        tweet = " "  + tweetobj.raw.lower() + " "

        tweet = tweet.encode('ascii','ignore')
        print "\nencode ascii: ", tweet

        tweet = re.sub(r'[^\s]*[\@][^\s]*', ' ', tweet) #remove usernames and emails
        print '\nremove usernames: ', tweet

        tweet = re.sub(r'http://[^\s]*\s', ' ', tweet) #remove links
        print '\nremove links: ', tweet

        allowed = string.ascii_letters + "#.'" #remove anything not in allowed string
        tweet = re.sub(r"[^{allowed}]+".format(allowed = allowed)," ",tweet)
        print '\nremove everything except allowed: ', tweet

        if not tweet: continue
        
        tweetobj.consec = re.sub(r"[\.]*[\s\.]*[\.]"," <end> <start> ", tweet) #should deal with elipsis and two full stops with some whitespace in between
        tweetobj.consec = ["<start>"]+tweetobj.consec.split()+["<end>"]
        print "\nconsec with tags:", tweetobj.consec

        tweet = tweet.replace(".", " ")
        print '\nreplace stops with spaces for intweet: ', tweet
        tweetobj.intweet = set(tweet.split())
        print '\n final intweet: ', tweetobj.intweet

        outqueue.put(tweetobj)
        inqueue.task_done()


if __name__ == '__main__':
    from multiprocessing import JoinableQueue, Process, Value

    class Tweet:
        pass
    testtweet = Tweet()
    testtweet.raw = "oh. a tricky)((*()one http://dfsdrgfd.g.regergde/fsrd/$#$%fg @t_hodson @t_hodson #haShTag <end> <?DF one.two three .... four. .five thomas.c.hodson@gmail.com"
    inqueue = JoinableQueue()
    inqueue.put(testtweet)
    outqueue = JoinableQueue()
    flag = Value('d',0)

    p = Process(target = sanitiser, args = (inqueue, outqueue, flag))
    p.start()
    inqueue.join()
    flag = 1
    inqueue.put(testtweet)
    out = outqueue.get()
    print 'consec', out.consec
    print 'intweet', out.intweet
