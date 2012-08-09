import gdbm
import xmlrpclib
import json
from collections import Counter
from random import randrange
from sys import exit

def addnode(nid,word,count):
    G.new_vertex_w_id(nid)
    G.set_vertex_attribute(nid,'label',word)
    G.set_vertex_attribute(nid,'size',str(count))
    G.set_vertex_attribute(nid,'fontcolor',"#ffffff")

def addlink(eid,nid1,nid2,width):
    G.new_edge_w_id(eid,nid1,nid2)
    #G.set_edge_attribute(i[0],'spline','true')
    G.set_edge_attribute(eid,'oriented','true')
    G.set_edge_attribute(eid,'width',str(width))
    G.set_edge_attribute(eid,'strength',"1")

def getnameperc(word,level):
    perc = level[word]/float(sum(level.values()))
    word = word + " (%.2f%%)" % (perc*100)
    return word,perc*10

def topn(level):
    return dict(sorted(level.iteritems(), key=lambda x:x[1], reverse=True)[:limit])

server_url = "http://127.0.0.1:20738/RPC2"
server = xmlrpclib.Server(server_url)
G = server.ubigraph
G.clear()

database = gdbm.open("markov.db","r")

graphid = {}

wordpair = [u"in",u"the"]
limit = 10

for word in wordpair:
    wordid = randrange(2**16)
    addnode(wordid,word,2.5)
    graphid[word] = wordid
addlink(randrange(2**16),graphid[wordpair[0]],graphid[wordpair[1]],1)

try:
    level = Counter(json.loads(database[json.dumps(wordpair)]))
except:
    print "Pair not seen"
    exit()

level = topn(level)

for rawword in level.keys():
    nid = randrange(2**16)
    word,size = getnameperc(rawword,level)
    addnode(nid,word,size/2)
    graphid[rawword] = nid
    addlink(randrange(2**16),graphid[wordpair[1]],graphid[rawword],size*10)

for word in level.keys():
    currwordpair = [wordpair[1],word]
    try:
        currlevel = Counter(json.loads(database[json.dumps(currwordpair)]))
    except:
        currlevel = {}
    currlevel = topn(currlevel)
    for rawsubword in currlevel.keys():
        nid = randrange(2**16)
        subword,size = getnameperc(rawsubword,currlevel)
        addnode(nid,subword,size/4)
        graphid[rawsubword] = nid
        addlink(randrange(2**16),graphid[currwordpair[1]],graphid[rawsubword],size*10)
