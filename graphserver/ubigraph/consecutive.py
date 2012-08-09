import sqlite3,xmlrpclib,math,random
server_url = "http://127.0.0.1:20738/RPC2"
server = xmlrpclib.Server(server_url)
G = server.ubigraph
G.clear()

database = sqlite3.connect("../../../../YRS-2012/data.db")
cursor = database.cursor()

full = """{"nodes":[%s],"links":[%s]}"""
node = """{"name":"%s","color":"#f00", "size": %d, "id":%d}"""
link = """{"source":%d,"target":%d,"value":%d, "color":"#f00"}"""

def getconnwords(wid):
    query = "SELECT word2id,consecutive FROM doubles WHERE consecutive > 0 AND (word1id == %d OR word2id == %d)" % (wid,wid)
    cursor.execute(query)
    return cursor.fetchall()

def getidcount(wid):
    cursor.execute("SELECT word,count FROM singles WHERE id == %d" % wid)
    word,prob = cursor.fetchone()
    return word,prob

def getnodeindex(cwid,allnodes):
    for index,node in enumerate(allnodes):
        if node.endswith("id\":%d}" % cwid):
            return index

def randcolor():
    return '#'+hex(random.randrange(255))[2:]+hex(random.randrange(255))[2:]+hex(random.randrange(255))[2:]

def consecutive(word):
    cursor.execute("SELECT id,count FROM singles WHERE word == '%s'" % word)
    wid,prob = cursor.fetchone()
    if not wid: return '{"ERROR":"word not found"}'
    allwids = list(set(getconnwords(wid)))
    G.new_vertex_w_id(wid)
    G.set_vertex_attribute(wid,'label',word.encode('ascii','ignore'))
    G.set_vertex_attribute(wid,'size',str(math.log(prob)))
    G.set_vertex_attribute(wid,'fontcolor',"#fff")
    G.set_vertex_attribute(wid,'color','%s' % randcolor())

    for cwid,consec in allwids:
        if cwid == wid: continue
        word,count = getidcount(cwid)
        G.new_vertex_w_id(cwid)
        G.set_vertex_attribute(cwid,'label',word.encode('ascii','ignore'))
        G.set_vertex_attribute(cwid,'size',str(math.log(count)))
        G.set_vertex_attribute(cwid,'fontcolor',"#fff")
        G.set_vertex_attribute(cwid,'color','%s' % randcolor())
        
    for cwid,consec in allwids:
        G.new_edge_w_id(cwid,wid,cwid)
        G.set_edge_attribute(cwid,'width',str(math.log(consec)))
        G.set_edge_attribute(cwid,'strength',"0.0")
        G.set_edge_attribute(cwid,'spline','true')
        G.set_edge_attribute(cwid,'strength','0.1')
        
consecutive("you")
