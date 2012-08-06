import base64
import socket
import ssl
from multiprocessing import Queue

def downloader(queue):
    user = "RoryMcNamara3"
    pwd = "YRS2012"
    sock = socket.socket()
    auth = base64.b64encode(user+":"+pwd)
    req =  "GET /1/statuses/sample.json\r\n"
    req += "Host: stream.twitter.com\r\n"
    req += "Authorization: Basic %s\r\n\r\n" % auth
    sock.connect(("stream.twitter.com",443))
    sock.send(req)
queue = Queue()
downloader(queue)   
