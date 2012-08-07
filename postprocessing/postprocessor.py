
import sqlite3
database = sqlite3.connect("minimaltest.db")
database.row_factory = sqlite3.Row #wraps the tuples returned by cursor with a highly optimised and useful object
cursor = database.cursor()	

def postprocess():
	#Go through the singles table and set the 'prob' column equal to the count 
	#for that word divided by the total number of words
    total = cursor.execute("SELECT SUM(count) FROM singles").fetchone()[0]
    cursor.execute("UPDATE singles SET prob = count / {}  ".format(float(total)))

    #loop through all the entries in the doubles table and there are four 
    #values that need to be set:

    #intweetprob = number of times we've seen word2 in tweets that contain 
    #word1 DIVIDED BY number of times we've seen word1 (from the singles table)

    #intweetstrength = intweetprob / prob of seeing word1 in any tweet 
    #(singles table) 

    #consecprob = number of times we've seen word2 directly after word1 divided
    # by number of times we've seen word1 (from the singles table)

    #consecstrength = consecprob / prob (0-1) of seeing word1 in any tweet 
    #(singles table)     

    cursor.execute("SELECT singles.id, intweet, consecutive, count, prob FROM doubles INNER JOIN singles ON doubles.word1id == singles.id")
    for record in cursor:
        invcount = 1.0 / record['count']#'count' and 'prob' are coming from the word1 record in the singles table
        invprob = 1.0 /  record['prob']

        intweetprob = record['intweet'] * invcount #multipying by the inverse is the same as dividing but you only have to do 
        intweetstrength = intweetprob * invprob    #the expensive division once

        consecprob = record['consecutive'] * invcount
        consecstrength = consecprob * invprob

    	updatequery = """
        UPDATE doubles
        SET intweetprob = {},
        intweetstrength = {},
        consecprob =      {},
        consecstrength =  {}
        WHERE id == {}
        """.format(
            intweetprob,
            intweetstrength,
            consecprob,
            consecstrength,
            record['id']
        )
        cursor.execute(updatequery)
    database.commit()

if __name__ == '__main__':
    pass
