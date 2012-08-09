#CREATE TABLE singles(id INTEGER PRIMARY KEY, word varchar(140) UNIQUE NOT NULL ON CONFLICT REPLACE, count INTEGER NOT NULL, prob double);
#CREATE TABLE doubles(id INTEGER PRIMARY KEY, word1id INTEGER NOT NULL, word2id INTEGER NOT NULL, intweet INTEGER NOT NULL, consecutive INTEGER NOT NULL, intweetprob double, consecprob double, intweetstrength double, consecstrength double);
#CREATE TABLE tweetsum (id INTEGER PRIMARY KEY,count INTEGER);
#INSERT INTO tweetsum VALUES(1,0);

#SELECT word FROM singles WHERE word == '%s' LIMIT 1
#   INSERT INTO singles (word,count) VALUES ('%s', %d)
#   UPDATE singles SET count = count + %d WHERE word = '%s'

#SELECT id FROM singles WHERE word == '%s' LIMIT 1 #word1id
#SELECT id FROM singles WHERE word == '%s' LIMIT 1 #word2id
#SELECT word1id,word2id FROM doubles WHERE word1id == '%s' AND word2id == '%s' LIMIT 1
#   INSERT INTO doubles (word1id,word2id,intweet,consecutive) VALUES (%d, %d, %d, %d)
#   UPDATE doubles SET intweet = intweet + %d, consecutive = consecutive + %d WHERE word1id == %d AND WHERE word2id == %d
import sqlite3

def inserter(inqueue,kill):
    """Takes a Tweets object and runs the necessary MySQL queries to enter
     it into the DB."""
    while not kill == 1:
        try:
            tweets = inqueue.get(True)
        except IOError:
            return
        #.singles
        #{"word":count}
        #.doubles
        #{("word1","word2"),(consecutive,intweet)}
        database = sqlite3.connect("../data.db")
        cursor = database.cursor()
        for word in tweets.singles:
            query = "SELECT word FROM singles WHERE word == '%s' LIMIT 1" % word
            cursor.execute(query)
            if not cursor.fetchone():
                query = "INSERT INTO singles (word,count,unique) VALUES ('%s', %d, %d)" % (word,tweets.singles[word][0], tweets.singles[word][1])
            else:
                query = "UPDATE singles SET count = count + %d, unique = unique + %d WHERE word = '%s'" % (tweets.singles[word][0],tweets.singles[word][1] ,word)
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
                if not intweet:
                    setintweet = ""
                else:
                    setintweet = "intweet = intweet + %d" % intweet
                if not consecutive:
                    setconsecutive = ""
                else:
                    setconsecutive = "consecutive = consecutive + %d" % consecutive
                if setintweet and setconsecutive:
                    doset = setintweet+","+setconsecutive
                else:
                    doset = setintweet if setintweet else setconsecutive
                query = "UPDATE doubles SET %s WHERE word1id == %d AND word2id == %d"
                query = query % (doset,word1id,word2id)
            try:
                cursor.execute(query)
            except:
                pass
        cursor.execute("UPDATE tweetsum SET count = count + 100 WHERE id = 1")
        database.commit()
        print "100 down"
