import gdbm
import xmlrpclib
import json
from collections import Counter
from random import randrange
from sys import exit

def addnode(word,allchildren,root = False):
    if not root:
        wordperc,perc = getnameperc(word,allchildren)
    else:
        wordperc = word
        perc = 2.5
    nid = randrange(2**16)
    graphid[word] = nid
    G.new_vertex_w_id(nid)
    G.set_vertex_attribute(nid,'label',wordperc.encode('ascii','ignore'))
    G.set_vertex_attribute(nid,'size',str(perc))
    G.set_vertex_attribute(nid,'fontcolor',"#ffffff")
    if root:
        G.set_vertex_attribute(nid,'color','#ff0000')

def addlink(parent,child,allchildren,root = False):
    eid = randrange(2**16)
    if not root:
        word,width = getnameperc(child,allchildren)
    else:
        width = 1
    G.new_edge_w_id(eid,getnodeid(parent),getnodeid(child))
    #G.set_edge_attribute(eid,'spline','true')
    G.set_edge_attribute(eid,'oriented','true')
    G.set_edge_attribute(eid,'width',str(width))
    G.set_edge_attribute(eid,'strength',"0.1")

def getnameperc(word,level):
    perc = level[word]/float(sum(level.values()))
    word = word + " (%.2f%%)" % (perc*100)
    return word,perc#*10

def getnodeid(word):
    return graphid[word]

def topn(level):
    return dict(sorted(level.iteritems(), key=lambda x:x[1], reverse=True)[:limit])

server_url = "http://127.0.0.1:20738/RPC2"
server = xmlrpclib.Server(server_url)
G = server.ubigraph
G.clear()

database = gdbm.open("markov.db","r")

wordpair = [u"in",u"the"]
limit = 10

#for word in wordpair:
#    wordid = randrange(2**16)
#    addnode(wordid,word,2.5)
#    graphid[word] = wordid
#addlink(randrange(2**16),graphid[wordpair[0]],graphid[wordpair[1]],1)
#
#try:
#    level = Counter(json.loads(database[json.dumps(wordpair)]))
#except:
#    print "Pair not seen"
#    exit()
#
#level = topn(level)
#
#for rawword in level.keys():
#    nid = randrange(2**16)
#    word,size = getnameperc(rawword,level)
#    addnode(nid,word,size/2)
#    graphid[rawword] = nid
#    addlink(randrange(2**16),graphid[wordpair[1]],graphid[rawword],size*10)
#
#for word in level.keys():
#    currwordpair = [wordpair[1],word]
#    try:
#        currlevel = Counter(json.loads(database[json.dumps(currwordpair)]))
#    except:
#        currlevel = {}
#    currlevel = topn(currlevel)
#    for rawsubword in currlevel.keys():
#        nid = randrange(2**16)
#        subword,size = getnameperc(rawsubword,currlevel)
#        addnode(nid,subword,size/4)
#        graphid[rawsubword] = nid
#        addlink(randrange(2**16),graphid[currwordpair[1]],graphid[rawsubword],size*10)
def getchildren(wordpair):
    try:
        allchildren = Counter(json.loads(database[json.dumps(wordpair)]))
    except:
        allchildren = {}
    children = topn(allchildren)
    return allchildren,children

graphid = {}

addnode(wordpair[0],{},root=True)
addnode(wordpair[1],{},root=True)
addlink(wordpair[0],wordpair[1],{},root = True)

def recursion(wordpair,depth):
    if not depth: return
    allchildren,children = getchildren(wordpair)
    for child in children:
        addnode(child,allchildren)
        addlink(wordpair[1],child,allchildren)
    #for child in children: self((wordpair[1],child),depth-1)
    for child in children:
        recursion((wordpair[1],child),depth-1)
recursion(wordpair,3)
#have grandparent var
#for i in parent, get wordpair
#   get all children
#   add all children
#   connect all children
#   add all children to list
#   wordpair = nextwordpair
#parent = childrenlist
