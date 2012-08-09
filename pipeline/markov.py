import json
import gdbm
from collections import Counter

database = gdbm.open("../markov.db","csu")

def gettriples(data):
    data = data.split()
    triples = []
    for i in range(len(data)-2):
        triples.append(data[i:i+3])
    return triples

def addtriple(triple):
    #key = json.dumps((triple[0],triple[1]))
    #if key not in  database.keys():
    #    database[key] = json.dumps([triple[2]])
    #else:
    #    data = json.loads(database[key])
    #    data.append(triple[2])
    #    database[key] = json.dumps(data)
    key = json.dumps((triple[0],triple[1]))
    if not key in database.keys():
        database[key] = json.dumps(Counter([triple[2]]))
    else:
        data = Counter(json.loads(database[key]))
        data[triple[2]] += 1
        database[key] = json.dumps(data)

def markov(inqueue,killProc):
    while not killProc == 1:
        try:
            tweet = inqueue.get(True)
        except IOError:
            return
        tweetdata = tweet.raw
        for triple in gettriples(tweetdata):
            addtriple(triple)
    database.close()
    
