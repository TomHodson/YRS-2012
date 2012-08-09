import gdbm
import xmlrpclib
import json
from collections import Counter
from random import randrange

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
    word = word + " (%.2f%%)" % perc
    return word,perc*10

server_url = "http://127.0.0.1:20738/RPC2"
server = xmlrpclib.Server(server_url)
G = server.ubigraph
G.clear()

database = gdbm.open("markov.db","r")

graphid = {}

wordpair = [u"and",u"the"]
for word in wordpair:
    wordid = randrange(2**16)
    addnode(wordid,word,2.5)
    graphid[word] = wordid
addlink(randrange(2**16),graphid[wordpair[0]],graphid[wordpair[1]],10)


level = Counter(json.loads(database[json.dumps(wordpair)]))

for rawword in level.keys():
    nid = randrange(2**16)
    word,size = getnameperc(rawword,level)
    addnode(nid,word,size)
    graphid[rawword] = nid
    addlink(randrange(2**16),graphid[wordpair[1]],graphid[rawword],size)

for word in level.keys():
    currwordpair = [wordpair[1],word]
    currlevel = Counter(json.loads(database[json.dumps(currwordpair)]))
    print currwordpair[1],currlevel
    for rawsubword in currlevel.keys():
        nid = randrange(2**16)
        subword,size = getnameperc(rawsubword,currlevel)
        addnode(nid,subword,size)
        graphid[subword] = nid
        print graphid
        addlink(randrange(2**16),graphid[currwordpair[1]],graphid[rawsubword],size)
