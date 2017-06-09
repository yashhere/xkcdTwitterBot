import tweepy
from secret import *

# create an OAuthHandler instance
# Twitter requires all requests to use OAuth for authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

auth.set_access_token(access_token, access_token_secret)

# Construct the API instance
api = tweepy.API(auth)  # create an API object

# public_tweets = api.home_timeline()
# for tweet in public_tweets:
#     print(tweet.text)

user = api.get_user('theyashagarwal')
print(user.screen_name)
print(user.followers_count)
for friend in user.friends():
    print(friend.screen_name)
