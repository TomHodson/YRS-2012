import sqlite3
database = sqlite3.connect("../data.db")
cursor = database.cursor()

full = """{"nodes":[%s],"links":[%s]}"""
node = """{"name":"%s","color":"#f00", "size": %d, "id":%d}"""
link = """{"source":%d,"target":%d,"value":%d, "color":"#f00"}"""

def getconnwords(wid):
    query = "SELECT word2id,consecutive FROM doubles WHERE consecutive > 0 AND (word1id == %d OR word2id == %d)" % (wid,wid)
    cursor.execute(query)
    return cursor.fetchall()

def getidcount(wid):
    cursor.execute("SELECT word,prob FROM singles WHERE id == %d" % wid)
    word,prob = cursor.fetchone()
    return word,prob

def getnodeindex(cwid,allnodes):
    for index,node in enumerate(allnodes):
        if node.endswith("id\":%d}" % cwid):
            return index

def consecutive(word):
    cursor.execute("SELECT id,prob FROM singles WHERE word == '%s'" % word)
    wid,prob = cursor.fetchone()
    if not wid: return '{"ERROR":"word not found"}'
    allnodes = []
    alllinks = []
    allwidsdup = getconnwords(wid)
    allwids=[]
    allnodes.append(node % (word,prob,wid))
    for i in allwidsdup:
        if i not in allwids:
            allwids.append(i)
    for cwid,consec in allwids:
        word,count = getidcount(cwid)
        cnode = node % (word.encode('ascii','ignore'), count,cwid)
        allnodes.append(cnode)
    for cwid,consec in allwids:
        clink = link % (0,getnodeindex(cwid,allnodes),consec)
        if clink not in alllinks: alllinks.append(clink)
    return full % (',\n'.join(allnodes),',\n'.join(alllinks))
        
print consecutive("you")
