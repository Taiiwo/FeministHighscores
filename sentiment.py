import numpy as np

def readSentimentList(file_name):
	ifile = open(file_name, 'r')
	happy_log_probs = {}
	sad_log_probs = {}
	ifile.readline() #Ignore title row
	
	for line in ifile:
		tokens = line[:-1].split(',')
		happy_log_probs[tokens[0]] = float(tokens[1])
		sad_log_probs[tokens[0]] = float(tokens[2])

	return happy_log_probs, sad_log_probs

def classifySentiment(words, happy_log_probs, sad_log_probs):
	# Split string into list
	words = words.split()
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

def isHappy(string):# will return if we think something is happy
	# We load in the list of words and their log probabilities
	happy_log_probs, sad_log_probs = readSentimentList('twitter_sentiment_list.csv')
	happy_prob, sad_prob = classifySentiment(string, happy_log_probs, sad_log_probs)
	if happy_prob > sad_prob:
		return True
	else:
		return False

def happyScore(string):# will give a score of a string's happiness
	# We load in the list of words and their log probabilities
	happy_log_probs, sad_log_probs = readSentimentList('twitter_sentiment_list.csv')
	happy_prob, sad_prob = classifySentiment(string, happy_log_probs, sad_log_probs)
	if happy_prob > sad_prob:
		return happy_prob
	else:
		return 0 - sad_prob

def main():# this function is just for testing the analyser
	# Calculate the probabilities that the tweets are happy or sad
	#tweet1_happy_prob, tweet1_sad_prob = classifySentiment(tweet1, happy_log_probs, sad_log_probs)
	#tweet2_happy_prob, tweet2_sad_prob = classifySentiment(tweet2, happy_log_probs, sad_log_probs)
	
	while 1:
		tweet = raw_input("Try me: ")
		print "The probability that tweet1 (" + tweet + ") is happy is " + str(happyScore(tweet))

if __name__ == '__main__':
	main()
