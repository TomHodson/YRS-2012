import base64
import socket
import ssl
import json

class Tweet(): #empty class to store tweet metadata
    pass

def readline(sock): #read single line (tweet) from socket
    tweet = ""
    while not tweet.endswith("\r\n"):
        tweet += sock.recv(1)
    return tweet

def downloader(queue,killproc):
    "Downloads tweets from twitter and adds a Tweet object to the sanitiser queue with the raw text in Tweet.raw"
    
    user = "RoryMcNamara3"
    pwd = "YRS2012"
    auth = base64.b64encode(user+":"+pwd) #Basic auth
    req =  "GET /1/statuses/sample.json HTTP/1.1\r\n" #http request for stream
    req += "Host: stream.twitter.com\r\n"
    req += "Authorization: Basic %s\r\n" % auth
    req += "Accept: */*\r\n\r\n"
    while not killproc == 1:
        try:
            sock = socket.socket()
            sock = ssl.wrap_socket(sock) #twitter uses https for stream
            sock.connect(("stream.twitter.com",443))
            sock.send(req) #send our request
            for i in range(5): #get rid of http response
                readline(sock)
            while not killproc == 1: #begin reading tweets
                tweet = Tweet()
                tweetraw = readline(sock) #tweet json data
                readline(sock) #size of next tweet
                readline(sock) #blank line
                tweetjson = json.loads(tweetraw)
                try:
                    if tweetjson[u"delete"]: continue #deleted tweet info
                except:
                    pass
                if not tweetjson[u"user"][u"lang"] == u"en": #only want en tweets
                    continue
                try: #incase something went wrong
                    tweet.raw = tweetjson[u"text"]
                except:
                    continue #if no text, move to next tweet
                queue.put(tweet) #add to end of queue
        except:
            continue
    sock.close()
