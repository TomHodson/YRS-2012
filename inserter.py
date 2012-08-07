#CREATE TABLE singles(id INTEGER PRIMARY KEY, word varchar(140) UNIQUE NOT NULL ON CONFLICT REPLACE, count INTEGER NOT NULL);

#SELECT word,count FROM singles WHERE word == "%s" LIMIT 1;
#   INSERT INTO singles (word,count) VALUES ("%s", 1);
#   UPDATE singles SET count = count + 1 WHERE word = "%s";
