import base64
import socket
import ssl
from multiprocessing import Queue
import json

class Tweet():
    pass

def readline(sock):
    tweet = ""
    while not tweet.endswith("\r\n"):
        tweet += sock.recv(1)
    return tweet

def downloader(queue):
    user = "RoryMcNamara3"
    pwd = "YRS2012"
    sock = socket.socket()
    auth = base64.b64encode(user+":"+pwd)
    req =  "GET /1/statuses/sample.json HTTP/1.1\r\n"
    req += "Host: stream.twitter.com\r\n"
    req += "Authorization: Basic %s\r\n" % auth
    req += "Accept: */*\r\n\r\n"
    sock = ssl.wrap_socket(sock)
    sock.connect(("stream.twitter.com",443))
    sock.send(req)
    for i in range(5):
        readline(sock)
    while True:
        tweet = Tweet()
        tweetraw = readline(sock)
        readline(sock)
        readline(sock)
        tweetjson = json.loads(tweetraw)
        try:
            if not tweetjson[u"lang"] == u"en":
                continue
        except:
            continue
        try:
            tweet.body = tweetjson[u"text"]
        except:
            continue
        print tweet.body
    sock.close()

queue = Queue()
downloader(queue)   
