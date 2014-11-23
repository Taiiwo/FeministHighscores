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
import json

# grab twitter auth details and use them to initialize the twitter API wrapper
twitterAuth = json.loads(open('./include', 'r').read())
twApi = twitter.Api(
		consumer_key =			twitterAuth['consumerKey'		],
		consumer_secret =		twitterAuth['consumerSecret'	],
		access_token_key =		twitterAuth['accessTokenKey'	],
		access_token_secret =	twitterAuth['accessTokenSecret'	])

# hashtags to search
hashtags = ["feminism",]
# search for tweets using sexist hashtags
for hashtag in hashtags:
	
# identify the emotional intent of the tweet
# if the tweet is retarded
	# compare with other tweets by the user
	# give the user a score based on their tweets
	# put the user on the ignorance high scores list