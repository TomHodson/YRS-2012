
#creates a clean DB and optionaly puts some test data in it

testrecords = False #whether to add some records for testing

import sqlite3
database = sqlite3.connect("../data.db")

database.execute("""CREATE TABLE
 tweetsum(id INTEGER PRIMARY KEY,
  count INTEGER NOT NULL);""")

database.execute("""CREATE TABLE
 singles(id INTEGER PRIMARY KEY,
  word varchar(140) UNIQUE NOT NULL ON CONFLICT REPLACE,
  count INTEGER NOT NULL,
  prob REAL,
  uniquecount INTEGER NOT NULL,
  uniqueprob REAL);
	""")

database.execute("""CREATE TABLE
 doubles(id INTEGER PRIMARY KEY,
 word1id INTEGER NOT NULL,
 word2id INTEGER NOT NULL,
 intweet INTEGER NOT NULL,
 consecutive INTEGER NOT NULL,
 intweetprob REAL,
 consecprob REAL,
 intweetstrength REAL,
 consecstrength REAL);
""")

if testrecords:
	database.execute("INSERT INTO singles (id,word,count) VALUES (1, 'hello', 200)")
	database.execute("INSERT INTO singles (id,word,count) VALUES (2, 'world', 100)")
	database.execute("INSERT INTO doubles (word1id,word2id,intweet,consecutive) VALUES (1, 2, 50, 40)")

database.commit()

