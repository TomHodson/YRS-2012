import sqlite3
database = sqlite3.connect("data.db")
cursor = database.cursor()

def totalcount():
	query = "SELECT sum(count) FROM singles"
	cursor.execute(query, wordid)
	return cursor.fetchone()	

def getwordcountandprob(wordid):
	query = "SELECT count,normalised FROM singles WHERE id == ?"
	cursor.execute(query, wordid)
	return cursor.fetchone()

def postprocess():
	#Go through the singles table and set the 'prob' column equal to the count 
	#for that word divided by the total number of words
    total = totalcount()
    	cursor.execute(
    		"UPDATE singles SET prob = count / {}  ".format(float(total))



    #loop through all the entries in the doubles table and there are four 
    #values that need to be set:

    #intweetprob = number of times we've seen word2 in tweets that contain 
    #word1 DIVIDED BY number of times we've seen word1 (from the singles table)

    #intweetstrength = intweetprob / prob (0-1) of seeing word1 in any tweet 
    #(singles table) 

    #consecprob = number of times we've seen word2 directly after word1 divided
    # by number of times we've seen word1 (from the singles table)

    #consecstrength = consecprob / prob (0-1) of seeing word1 in any tweet 
    #(singles table)     

    #dividing the conditional probablity (intweetprob or consecprob) by the base probability
    # of the given word (word1) gives a measure of how much more more likely 
    #you are to see word 2 in a tweet than you are to see it in any tweet
    #which gives a measure of the 'strength' of the connection between two 
    #words

    doublequery = "SELECT id,word1id, word2id, intweet, consecutive FROM doubles"
    cursor.execute(doublequery)
    doubles = cursor.fetchall()
    for record in doubles:
    	countword1, probword1 = getwordcount(record[0])
    	id,word1id, word2id, intweet, consecutive = record
    	condprobintweet = countword2givenword1 / float(countword1)
    	linkstrength = condprobintweet / probword1
    	updatequery = "UPDATE doubles SET intweetstrength == {} WHERE id == {}".format(intweetstrength, id)
