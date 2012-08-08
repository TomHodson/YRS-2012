import sqlite3
database = sqlite3.connect("../data.db")
cursor = database.cursor()

full = """{"nodes":[%s],"links":[%s]}"""
node = """{"name":"%s","color":"#fff", "size": %d, "id":%d}"""
link = """{"source":%d,"target":%d,"value":%d, "color":"#fff"}"""

def getconnwords(wid):
    query = "SELECT word2id,consecutive FROM doubles WHERE consecutive > 0 AND (word1id == %d OR word2id == %d)" % (wid,wid)
    cursor.execute(query)
    return cursor.fetchall()

def getidcount(wid):
    cursor.execute("SELECT word,count FROM singles WHERE id == %d" % wid)
    word,count = cursor.fetchone()
    return word,count

def getnodeindex(cwid,allnodes):
    for index,node in enumerate(allnodes):
        if node.endswith("id\":%d}" % cwid):
            return index

def consecutive(word):
    cursor.execute("SELECT id,count FROM singles WHERE word == '%s'" % word)
    wid,count = cursor.fetchone()
    if not wid: return '{"ERROR":"word not found"}'
    allnodes = []
    alllinks = []
    allwidsdup = getconnwords(wid)
    allwids=[]
    for i in allwidsdup:
        if i not in allwids:
            allwids.append(i)
    for cwid,consec in allwids:
        word,count = getidcount(cwid)
        cnode = node % (word, count,cwid)
        allnodes.append(cnode)
    for cwid,consec in allwids:
        clink = link % (0,getnodeindex(cwid,allnodes),consec)
        if clink not in alllinks: allinks.append(clink)
        
consecutive("you")
