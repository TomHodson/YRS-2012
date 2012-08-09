import sqlite3,xmlrpclib,math
from random import randrange

server_url = "http://127.0.0.1:20738/RPC2"
server = xmlrpclib.Server(server_url)
G = server.ubigraph
G.clear()

childlimit = 5
widthscale = 100
depth = 3


database = sqlite3.connect("../../data.db")
database.row_factory = sqlite3.Row #wraps the tuples returned by cursor with a highly optimised and useful object
cursor = database.cursor()

def addnode(nid,word,size,colour="#ffffff"):
    G.new_vertex_w_id(nid)
    G.set_vertex_attribute(nid,'label',word)
    G.set_vertex_attribute(nid,'size',str(size))
    G.set_vertex_attribute(nid,'fontcolor',"#ffffff")

def addrecordasnode(wordrecord):
    nid = wordrecord["id"]
    word = wordrecord['word']
    size = wordrecord['uniqueprob']

    addnode(nid, word, size)

def addlink(eid,nid1,nid2,width):
        G.new_edge_w_id(eid,nid1,nid2)
        #G.set_edge_attribute(i[0],'spline','true')
        G.set_edge_attribute(eid,'width',str(width))
        G.set_edge_attribute(eid,'strength',"0.0")

def linktworecords(record1, record2):
    global widthscale

    key = sorted((record1, record2), key = lambda x : x['word'])
    word1id, word2id = key[0]['id'], key[1]['id']
    width = cursor.execute("SELECT intweetstrength FROM doubles WHERE word1id == {} AND word2id == {}".format(word1id, word2id)).fetchone()[0] * widthscale
    addlink(randrange(2**16), record1['id'], record2['id'], width)

def getconnwords(word):
    "return a list of wordids records given a word record"
    global childlimit
    connrecords = cursor.execute("SELECT * FROM doubles WHERE (word1id == {id} OR word2id == {id}) AND intweet > 0 ORDER BY intweetstrength DESC LIMIT {childlimit}".format(id = word['id'], childlimit = childlimit)).fetchall()
    return [(record['word1id'] if word['id'] != record['word1id'] else record['word2id']) for record in connrecords]
    


def getrecordbyname(name):
    return cursor.execute("SELECT * FROM singles WHERE word == '{}'".format(name)).fetchone()

def getrecordbyid(theid):
    return cursor.execute("SELECT * FROM singles WHERE id == '{}'".format(theid)).fetchone()

seed = 'rt'
seed = getrecordbyname(seed)

#for iteration in range(depth):
#    words = tree[iteration]
#    tree.append([])
#    for parent in words:
#        for child in getconnwords(parent):
#            tree[iteration + 1].append(child) #add them to the tree
#            for childnode in childgroup:
#                addrecordasnode(childnode)
#                linkrecords()
def  f(parent, depth):
    if depth != 0:
        children = getconnwords(parent)
        for thisid in children:
            child = getrecordbyid(thisid)
            addrecordasnode(child)
            linktworecords(parent,child)
            f(child, depth-1)
    return

if __name__ == '__main__':
    f(seed, depth)


