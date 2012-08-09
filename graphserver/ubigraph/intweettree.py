import sqlite3,xmlrpclib,math

server_url = "http://127.0.0.1:20738/RPC2"
server = xmlrpclib.Server(server_url)
G = server.ubigraph
G.clear()

def addnode(nid,word,size,colour="#ffffff"):
    G.new_vertex_w_id(nid)
    G.set_vertex_attribute(nid,'label',word)
    G.set_vertex_attribute(nid,'size',str(size))
    G.set_vertex_attribute(nid,'fontcolor',"#ffffff")

def addrecordasnode(word):
    nid = word["id"]
    word = word['word']
    size = word['intweetprob']

    addnode(nid, word, size)

def addlink(eid,nid1,nid2,width):
        G.new_edge_w_id(eid,nid1,nid2)
        #G.set_edge_attribute(i[0],'spline','true')
        G.set_edge_attribute(eid,'width',str(width))
        G.set_edge_attribute(eid,'strength',"0.0")

def getconnwords(wid):
    "return a list of word records given a word id"

database = sqlite3.connect("../../../../YRS-2012/data.db")
database.row_factory = sqlite3.Row #wraps the tuples returned by cursor with a highly optimised and useful object
cursor = database.cursor()  

seed = 'the'
tree = [ [ getidbyname(seed) ] ]
depth = 3

for iteration in range(depth):
    words = tree[iteration]
    tree.append([])
    for childgroup in [getconnwords(word) for word in words]
        tree[iteration + 1].append(childnodes) #add them to the tree
        for childnode in childgroup:
            addrecordasnode(childnode)
            




