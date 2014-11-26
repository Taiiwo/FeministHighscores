import numpy as np

class sentimentAnalyser():
	def __init__(self):# read the sentiment list only once when we initialise
		# We load in the list of words and their log probabilities
		self.happy_log_probs, self.sad_log_probs = self.loadSentimentList('twitter_sentiment_list.csv')
	
	def loadSentimentList(self, file_name):
		ifile = open(file_name, 'r')
		happy_log_probs = {}
		sad_log_probs = {}
		ifile.readline() #Ignore title row
		
		for line in ifile:
			tokens = line[:-1].split(',')
			happy_log_probs[tokens[0]] = float(tokens[1])
			sad_log_probs[tokens[0]] = float(tokens[2])

		return happy_log_probs, sad_log_probs
		
	def classifySentiment(self, words, happy_log_probs, sad_log_probs):
		# Split string into list
		words = words.lower().split()
		# Get the log-probability of each word under each sentiment
		happy_probs = [happy_log_probs[word] for word in words if word in happy_log_probs]
		sad_probs = [sad_log_probs[word] for word in words if word in sad_log_probs]

		# Sum all the log-probabilities for each sentiment to get a log-probability for the whole tweet
		tweet_happy_log_prob = np.sum(happy_probs)
		tweet_sad_log_prob = np.sum(sad_probs)

		# Calculate the probability of the tweet belonging to each sentiment
		prob_happy = np.reciprocal(np.exp(tweet_sad_log_prob - tweet_happy_log_prob) + 1)
		prob_sad = 1 - prob_happy

		return prob_happy, prob_sad

	def happyScore(self, string):# will give a score of a string's happiness
		happy_prob, sad_prob = self.classifySentiment(string, self.happy_log_probs, self.sad_log_probs)
		#return happy_prob - sad_prob
		if happy_prob > sad_prob:
			return happy_prob
		else:
			return 0 - sad_prob

	def isHappy(self, string):# will return if we think something is happy
		# note: We don't really need this, I just thought it might be useful.
		happy_prob, sad_prob = self.classifySentiment(string, self.happy_log_probs, self.sad_log_probs)
		if happy_prob > sad_prob:
			return True
		else:
			return False
			
if __name__ == '__main__':
	anal = sentimentAnalyser()# kek
	while 1:
		tweet = raw_input("Try me: ")
		print "The probability that tweet1 (" + tweet + ") is happy is " + str(anal.happyScore(tweet))
