#   / __\__ _ __ ___ (_)_ __ (_)___| |_  / __\ | ___   ___| | _____ _ __ 
#  / _\/ _ \ '_ ` _ \| | '_ \| / __| __|/__\// |/ _ \ / __| |/ / _ \ '__|
# / / |  __/ | | | | | | | | | \__ \ |_/ \/  \ | (_) | (__|   <  __/ |   
# \/   \___|_| |_| |_|_|_| |_|_|___/\__\_____/_|\___/ \___|_|\_\___|_|   

# This is a project inspired by GGAutoBlocker that aims to identify radical
# feminists and anti-gamergate supporters, and instead of maliciously and
# oppressively adding them to an ambiguous blocklist conflictingly making
# them more likely to attempt the behaviour and opinions they are being
# punished for, this script attempts to allow it's users to identify and
# aggregate these radicals for the purpose of mass ridicule and
# identification of such humorously idiotic thoughts.

import twitter
import nltk
import json
import sentiment

# grab twitter auth details and use them to initialise the twitter API wrapper
twitterAuth = json.loads(open('./auth.include', 'r').read())
twApi = twitter.Api(
		consumer_key =			twitterAuth['consumerKey'		],
		consumer_secret =		twitterAuth['consumerSecret'	],
		access_token_key =		twitterAuth['accessTokenKey'	],
		access_token_secret =	twitterAuth['accessTokenSecret'	])

# initialise the sentiment analyser
analyser = sentiment.sentimentAnalyser()

# phrases to search
goodThings = ["gamergate", "notyourshield"]
badThings = ["feminism",]
tenses = [goodThings, badThings]
turn = ["+","-"]
highScores = []
scannedUsers = []
scannedTweets = []
debugging = True
# search for tweets
# for each tense in the tenses
for index, tense in enumerate(tenses):
	# for each term we have for that tense
	for term in tense:
		# search for a list of tweets
		if debugging == True: print "[ ] Searching for tweets"
		hashtagTweets = twApi.GetSearch(term=term)
		# iterate through the tweets
		for tweet in hashtagTweets:
			# check that we haven't already scanned the user
			if tweet.user.name not in scannedUsers and tweet.text not in scannedTweets:
				scannedTweets.append(tweet.text)
				# identify the emotional intent of the tweet
				score = analyser.happyScore(tweet.text)
				if debugging == True: print "[ ] " + tweet.text.replace('\n', '') + " by " + tweet.user.name + " scored " + turn[index] + str(score)
				# if the tweet is about negative about a good topic or positive about a bad topic
				if index == 0 and score < 0 or index == 1 and score > 0:
					if debugging == True: print "[+] "+ tweet.user.name +" may be retarded. Scanning user"
					# the tweet is probably retarded.
					# grab other tweets by the user
					userTweets = twApi.GetUserTimeline(user_id = tweet.user.id)
					# give the user a score based on their tweets
					userScore = 0
					numScanned = 0
					# iterate through all their tweets
					for userTweet in userTweets:
						# for each tense
						for index1, tense1 in enumerate(tenses):
							# for each term in the tense
							for term1 in tense1:
								# if the user is tweeting about the term
								if term1 in userTweet.text:
									numScanned += 1
									# identify the emotional intent of the tweet
									score = analyser.happyScore(userTweet.text)
									if debugging == True: print "\t[ ] " + userTweet.text.replace('\n', '') + " by " + userTweet.user.name + " scored " + turn[index1] + str(score)
									# if the tweet is about negative about a good topic or positive about a bad topic
									if index1 == 0 and score < 0 or index1 == 1 and score > 0:
										# the tweet is probably retarded.
										# add some points to their score
										userScore += score
					# put the user on the ignorance high scores list
					if numScanned <= 0:
						if debugging == True: print "Couldn't find any more relevant tweets by that user."
					else:
						# divide the tweets between the number of tweets scanned - On second thought, maybe not.
						# userScore = userScore / numScanned
						# make sure we aren't scanning the same person multiple times
						scannedUsers.append(tweet.user.name)
						# actually add them to the high scores
						highScores.append([tweet.user.name, userScore])
						#print off some debugging information
						print tweet.user.name + " scores: " + str(userScore)
						
