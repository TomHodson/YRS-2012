#CREATE TABLE singles(id INTEGER PRIMARY KEY, word varchar(140) NOT NULL, count INTEGER NOT NULL);

#SELECT word FROM singles WHERE word == '%s' LIMIT 1
#   INSERT INTO singles (word,count) VALUES ('%s', %d)
#   UPDATE singles SET count = count + %d WHERE word = '%s'

#CREATE TABLE doubles(id INTEGER PRIMARY KEY, word1id INTEGER NOT NULL, word2id INTEGER NOT NULL, intweet INTEGER NOT NULL, consecutive INTEGER NOT NULL);

#SELECT id FROM singles WHERE word == '%s' LIMIT 1 #word1id
#SELECT id FROM singles WHERE word == '%s' LIMIT 1 #word2id
#SELECT word1id,word2id FROM doubles WHERE word1id == '%s' AND word2id == '%s' LIMIT 1
#   INSERT INTO doubles (word1id,word2id,intweet,consecutive) VALUES (%d, %d, %d, %d)
#   UPDATE doubles SET intweet = intweet + %d, consecutive = consecutive + %d WHERE word1id == %d AND WHERE word2id == %d
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
        for word in tweets.singles:
            query = "SELECT word FROM singles WHERE word == '%s' LIMIT 1" % word
            cursor.execute(query)
            if not cursor.fetchone():
                query = "INSERT INTO singles (word,count) VALUES ('%s', %d)" % (word,tweets.singles[word])
            else:
                query = "UPDATE singles SET count = count + %d WHERE word = '%s'" % (tweets.singles[word],word)
            cursor.execute(query)
        database.commit()
        for pair in tweets.doubles:
            word1,word2 = pair
            consecutive,intweet = tweets.doubles[pair]
            query = "SELECT id FROM singles WHERE word == '%s' LIMIT 1"
            cursor.execute(query % word1)
            word1id = cursor.fetchone()[0]
            cursor.execute(query % word2)
            word2id = cursor.fetchone()[0]
            query = "SELECT word1id,word2id FROM doubles WHERE word1id == %d AND word2id == %d LIMIT 1"
            query = query % (word1id,word2id)
            cursor.execute(query)
            if not cursor.fetchone():
                query = "INSERT INTO doubles (word1id,word2id,intweet,consecutive) VALUES (%d, %d, %d, %d)"
                query = query % (word1id,word2id,intweet,consecutive)
            else:
                query = "UPDATE doubles SET intweet = intweet + %d, consecutive = consecutive + %d WHERE word1id == %d AND WHERE word2id == %d"
                query = query % (intweet,consecutive,word1id,word2id)
            try:
                cursor.execute(query)
            except:
                print query
        database.commit()
        print "set"
