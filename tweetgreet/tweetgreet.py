from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, API
from tweepy import Stream
import json
import logging
import warnings
from pprint import pprint

warnings.filterwarnings("ignore")

access_token = "4464294380-GHJ3PY...lEqzZ8FikULPnkxaS4huT"
access_token_secret = "L033NEsDOA...tZVoaU8prpFbiREWhcVROw2"
consumer_key = "D1G0bn...9Y88p"
consumer_secret = "rGJjCU...FRISsiMURYlqCXJvOP"

auth_handler = OAuthHandler(consumer_key, consumer_secret)
auth_handler.set_access_token(access_token, access_token_secret)

twitter_client = API(auth_handler)

logging.getLogger("main").setLevel(logging.INFO)

AVOID = ["monty", "leather", "skin", "bag", "blood", "bite"]


class PyStreamListener(StreamListener):
    def on_data(self, data):
        tweet = json.loads(data)
        try:
            publish = True
            for word in AVOID:
                if word in tweet['text'].lower():
                    logging.info("SKIPPED FOR {}".format(word))
                    publish = False

            if tweet.get('lang') and tweet.get('lang') != 'en':
                publish = False

            if publish:
                twitter_client.retweet(tweet['id'])
                logging.debug("RT: {}".format(tweet['text']))

        except Exception as ex:
            logging.error(ex)

        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    listener = PyStreamListener()
    stream = Stream(auth_handler, listener)
    stream.filter(track=['python', 'django', 'kivy', 'scrapy'])
