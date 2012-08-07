#CREATE TABLE singles(id INTEGER PRIMARY KEY, word varchar(140) UNIQUE NOT NULL ON CONFLICT REPLACE, count INTEGER NOT NULL);

#SELECT word FROM singles WHERE word == "%s" LIMIT 1;
#   INSERT INTO singles (word,count) VALUES ("%s", %d);
#   UPDATE singles SET count = count + %d WHERE word = "%s";
import sqlite3

def inserter(inqueue,kill):
    while not kill == 1:
        try:
            tweets = inqueue.get(True)
        except IOError:
            return
        #.singles
        #{"word":count}
        #.doubles
        #{("word1","word2"),(consecutive,intweet)}
        database = sqlite3.connect("data.db")
        cursor = database.cursor()
        for word in tweets.keys():#.singles:
            query = "SELECT word FROM singles WHERE word == '%s' LIMIT 1" % word
            cursor.execute(query)
            if not cursor.fetchone():
                query = "INSERT INTO singles (word,count) VALUES ('%s', %d)" % (word,tweets[word])
            else:
                query = "UPDATE singles SET count = count + %d WHERE word = '%s'" % (tweets[word],word)
            print query

from Queue import Queue
q = Queue()
q.put({"test":6})
q.put({"fail":5})
q.put({"guess":3})
q.put({"test":1})
inserter(q,0)
