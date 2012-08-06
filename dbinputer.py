import sqlite3

probs = sqlite3.connect('probs.db')

def DBinputer(queue):
	while sizeof(cache):
		cache = {}
		while True:
			tweet  = queue.get(block = true)
			wordpairs = combinations(words, 2) #(word1, word2) where word1 != word2 and order does NOT matter
			for wordpair in wordpairs:



			queue.task_done()