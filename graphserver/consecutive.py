import sqlite3
database = sqlite3.connect("../data.db")
cursor = database.cursor()

full = """{"nodes":[%s],"links":[%s]}"""
node = """{"name":"%s","color":"#f00", "size": %d, "id":%d}"""
link = """{"source":%d,"target":%d,"value":%d, "color":"#f00"}"""

def getconnwords(wid, num):
    query = "SELECT word2id,consecstrength FROM doubles WHERE consecutive > 0 AND word1id == %d ORDER BY consecstrength LIMIT %d" % (wid, num)
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

def consecutive(args):
    word = args['seed'][0]
    num = args['depth'][0]

    print word, num

    cursor.execute("SELECT id,prob FROM singles WHERE word == '%s'" % word)
    try:
        wid,prob = cursor.fetchone()
    except: return '{"ERROR":"word not found"}'
    allnodes = []
    alllinks = []
    allwids = list(set(getconnwords(wid, num)))
    allnodes.append(node % (word,prob,wid))
    for cwid,consec in allwids:
        if cwid == wid: continue
        word,count = getidcount(cwid)
        cnode = node % (word.encode('ascii','ignore'), count,cwid)
        allnodes.append(cnode)
    import math
    for cwid,consec in allwids:
        clink = link % (0,getnodeindex(cwid,allnodes),consec)
        if clink not in alllinks: alllinks.append(clink)
    #allnodes = list(set(allnodes))
    alllinks = list(set(alllinks))
    return full % (',\n'.join(allnodes),',\n'.join(alllinks))
        
if __name__ == '__main__':
    args = {'num':10, 'seed':'this'}
    print consecutive(args)
