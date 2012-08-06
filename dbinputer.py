import sqlite3
from collections import defaultdict
from itertools import combinations
from Queue import Queue

def intweetparser(inputqueue, outputqueue):
	tweetsperblock = 1
	words = defaultdict(int)
	wordwords = defaultdict(lambda : defaultdict(int))
	for _ in range(tweetsperblock):
		tweet  = inputqueue.get(block = True)
		wordpairs = combinations(tweet.words, 2) #(word1, word2) where word1 != word2 and order does NOT matter
		for word in tweet.words:
			words[word] += 1

		for word1,word2 in wordpairs:
			wordwords[word1][word2] += 1
			print word1,word2
		inputqueue.task_done()
	outputqueue.put((words, wordwords))

if __name__ == '__main__':
	class Tweet():
		def __init__(self):
				pass
	testtweet = Tweet()
	testtweet.words = ['this', 'is', 'a', 'test']
	inputqueue = Queue()
	inputqueue.put(testtweet)
	outputqueue = Queue()
	DBinputer(inputqueue, outputqueue)
	#inputqueue.join()
	print outputqueue.get(block=True)
