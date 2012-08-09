import gdbm
import xmlrpclib
import json
from collections import Counter

def addnode(nid,word,size):
    G.new_vertex_w_id(nid)
    G.set_vertex_attribute(nid,'label',word)
    G.set_vertex_attribute(nid,'size',str(size))
    G.set_vertex_attribute(nid,'fontcolor',"#ffffff")

def addlink(eid,nid1,nid2,width):
        G.new_edge_w_id(eid,nid1,nid2)
        #G.set_edge_attribute(i[0],'spline','true')
        G.set_edge_attribute(eid,'width',str(width))
        G.set_edge_attribute(eid,'strength',"0.0")

server_url = "http://127.0.0.1:20738/RPC2"
server = xmlrpclib.Server(server_url)
G = server.ubigraph
G.clear()

database = gdbm.open("markov.db","r")

graphid = {}

wordpair = ["and","the"]

level1 = Counter(json.loads(database[json.dumps(wordpair)]))

for i in level1.keys():
    print level1[i],i,wordpair[1]
