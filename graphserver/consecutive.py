import sqlite3

def getconnwords(wid):
    query = "SELECT word2id,consecutive FROM doubles WHERE consecutive > 0 AND word1id == '%d' AND (word2id =='" % wid
    cursor.execute(query+"' OR word2id == '".join(allwids)+"')")
    return cursor.fetchall()

def getidcount(wid):
    cursor.execute("SELECT word,count FROM singles WHERE id == %s" % word)
    word,count = cursor.fetchone()
    return word,count

def consecutive(word):
    base = sqlite3.connect("../data.db")
    cursor = database.cursor()

    cursor.execute("SELECT id,count FROM singles WHERE word == %s" % word)
    wid,count = cursor.fetchone()
    if not wid: return '{"ERROR":"word not found"}'
    
