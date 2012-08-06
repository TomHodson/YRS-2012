YRS-2012
========

downloader
--------
downloads tweets from twitter and adds the tweet object to the queue with Tweet.body

sanitiser
--------
removes punctuation, email addresses and links from the Tweet.body

parse
--------
creates counts for individual and pairs of words and adds to Tweet.single/Tweet.double

merger
--------
merges 100 Tweet objects into a tuple of dicts containing both single and double summations
