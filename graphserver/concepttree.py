import sqlite3
database = sqlite3.connect("../data.db")
database.row_factory = sqlite3.Row #wraps the tuples returned by cursor with a highly optimised and useful object
cursor = database.cursor()

full = """{"nodes":[%s],"links":[%s]}"""
node = """{"name":"%s","color":"#f00", "size": %d, "id":%d}"""
link = """{"source":%d,"target":%d,"value":%d, "color":"#f00"}"""

def topnlinks(word, n):
	wordrecord = cursor.execute("SELECT id FROM singles WHERE word == {wordstr}".format(wordstr=word) ).fetchone()

	children = cursor.execute("SELECT word1id, word1id FROM doubles WHERE (word1id == {id} OR word2id == {id}) ORDER BY intweetstrength DESC LIMIT {num}".format(id=wordrecord['id'] , num=n)).fetchall()
	

	links = []
	for i, child in enumerate(children):
		link = 
		links.append

def concepttree(args):
	depth = args['depth']
	seed = args['seed']
	num = args['num']

	levels = [seed]

	for level in range(num):









