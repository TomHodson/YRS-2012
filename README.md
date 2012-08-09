YRS-2012
========

Probability Refresher
---------------------
N(A) is the number of times A has happened

P(A) means the probability of A happening
P(A|B) means the probility of A happening given that B has already happened

Tweet Scraping Pipeline
=======================
This multithreaded pipeline downloads and processes tweets from the Twitter firehose, in order from first to last they are:

Downloader
--------
Downloads tweets from twitter and adds a Tweet object to the sanitiser queue with the raw text in Tweet.raw

Sanitiser
---------
Removes punctuation, email addresses and links from the Tweet.raw, then tokenises it and puts it into Tweet.body

Analyser
--------
Creates counts for individual and pairs of words and tracks three metrics:
	
	-Tweet.single: The number of time each token has appeared in the tweet.
	
	-Tweet.intweet: The number of times token2 has appeared given that token1 appeared anywhere in the tweet.
	
	-Tweet.consecutive: The number of times token2 has appeared with token1 directly before it.

Merger
--------
Waits for a large number of tweets to a accumulate (dependant on available RAM) then merges their data together to attain a Tweets object that contains the sums of the individual metrics, this is effectively a in-memory cache to ease load on the DB.

Inputter
--------
Takes a Tweets object and runs the necessary MySQL queries to enter it into the DB.

Post Processing
================
Values dependant on the raw metrics can only be efficiently computed when the DB is not being modified by the scraper so the post processor performs these computations and stores them in the DB.These values will be valid untill the next time the scaper is run.

Values computer by this step:
	'wordprob' - Probility of this token apearing in the tweet
		N(this token) / N(any token)

	'intweetprob' - Conditional probability of token2 given token1 appeared somewhere in the tweet:
		N(token2 and token1 in same tweet) / N(token1)
	
	'consecutiveprob' - Conditional probability of token2 given it appeared straight after token1:
		N(token2 after token1) / N(token1)

	'intweetprob' - How much more likely it is to see token2 given token1 than simply seeing token in any tweet:
		P(token2 | token1) / P(token1)
	
	'consecutiveprob' - Conditional probability of token2 given it appeared straight after token1:
		P(token2 | token1) / P(token1)



We wanted to look at the statistical relationships between words in tweets, we wrote a multi-threaded miner to pull data from the twitter fire hose, perform analyses on and put the data into a database.

Specifically, we're looking at how likely you are to see two words anywhere in the same tweet and how likely you are to see two words consecutively in the same tweet. For instance by calculating how likely you are to see 'usain' in a tweet containing 'olympics' and comparing that to how likely you are to see 'usain' in any tweet you can get a measure for how related these words are. You can also apply the same logic to pairs or triplets of consecutive words.

We then wrote programs to visualize this data using networked graphs.




