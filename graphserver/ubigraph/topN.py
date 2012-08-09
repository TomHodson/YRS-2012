import sqlite3,xmlrpclib,math

server_url = "http://127.0.0.1:20738/RPC2"
server = xmlrpclib.Server(server_url)
G = server.ubigraph
G.clear()

def getconnwords(wid):
    query = "SELECT id,word2id,intweet FROM doubles WHERE consecutive > 0 AND word1id == '%d' AND (word2id =='" % wid
    cursor.execute(query+"' OR word2id == '".join(allwids)+"')")
    return cursor.fetchall()

database = sqlite3.connect("../../../../YRS-2012/data.db")
cursor = database.cursor()

cursor.execute("SELECT id,word,count FROM singles ORDER BY count DESC LIMIT 50")
rows = cursor.fetchall()
allwids = [str(i[0]) for i in rows]

for wid,word,count in rows:
    G.new_vertex_w_id(wid)
    G.set_vertex_attribute(wid,'label',word)
    G.set_vertex_attribute(wid,'size',str(math.log(math.log(count))))
    G.set_vertex_attribute(wid,'fontcolor',"#ffffff")

for wid,word,count in rows:
    for i in getconnwords(wid):
        G.new_edge_w_id(i[0],wid,i[1])
        #G.set_edge_attribute(i[0],'spline','true')
        G.set_edge_attribute(i[0],'width',str(i[2]))
        G.set_edge_attribute(i[0],'strength',"0.0")

