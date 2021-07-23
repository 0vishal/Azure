'''
@Author: Vishal Salaskar
@Date: 2021-06-26
@Last Modified by: Vishal Salaskar
@Last Modified time: 2021-06-26
@Title : Program to perform apache kafka datastreaming from producer
'''

import tweepy,time
import os,log
from kafka import KafkaProducer

class Producer:

    def __init__(self):
        '''
        Description : required connection to twitter app
        '''
        consumer_key = os.getenv('CKEY')
        consumer_key_secret = os.getenv('CSECRET')
        access_token = os.getenv('ATOKEN')
        access_token_secret = os.getenv('ASECRET')

        auth = tweepy.OAuthHandler(consumer_key,consumer_key_secret)
        auth.set_access_token(access_token,access_token_secret)
        api = tweepy.API(auth)

        self.public_tweets = api.search('covid19')
        serverdetails = os.getenv('SERVER')
        self.topic_name = os.getenv('TOPIC_NAME')
        self.producer = KafkaProducer(bootstrap_servers=[serverdetails],api_version=(0, 10)) 

    def get_tweet(self):
        """
        description :
        function : to get the tweet 
        """
        try:
            for tweet in self.public_tweets:
                data = tweet.text
                self.producer.send(self.topic_name, data.encode('utf-8'))
                log.logger("data produced has been sent")
        except:
            print("error")        

    def periodic_interval(self,period):
        """
        description :
        function : to get the tweet at a periodic interval of time
        parameters: a period of time
        """
        try:
            while True:
                    self.get_tweet()
                    time.sleep(period)
        except:
            print("stopped now ")            


if __name__ == "__main__":

    get_data = Producer()
    get_data.get_tweet()
    get_data.periodic_interval(100)
    