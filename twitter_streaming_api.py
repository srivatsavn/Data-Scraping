from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import glob
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer

senti = SentimentIntensityAnalyzer()

consumer_key = "d7Jk527rEdilwqze0W9vDu1PO"
consumer_secret = "Fth7cqctfgt4bAAoX21Yqnheub3XP0vJSfrhYGYuY7t2dr3INt"

access_token = "1062987419908276225-OIQGQceKSpJGqSNyccxoN8pn546ZC9"
access_token_secret = "YPUl8AkEcpD7Bri1yu20rs1njbtWGCydhZAQo5rKcvIJF"

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.twitter
collection = db.abhinandan

class StdOutListener(StreamListener):

    def on_data(self, data):
        data = json.loads(data)
        score = senti.polarity_scores(data['text'])['compound']
        if score > 0.1:
            sentiment = 'Positive'
        elif score < -0.1:
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'
        data['sentiment'] = sentiment
        collection.insert_one(data)
        print(data['text'])
        print('---------')
        return True

    def on_error(self, status):
        print (status)


if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    stream.filter(track=['#WelcomeHomeAbhinandan'])