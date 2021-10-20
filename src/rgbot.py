import tweepy

class Bot:
    def __init__(self, consumer_key, consumer_secret, access_key, access_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_key = access_key
        self.access_secret = access_secret
    
    def connect(self):
        self.auth = tweepy.OAuthHandler(
            self.consumer_key,
            self.consumer_secret)

        self.auth.set_access_token(
            self.access_key,
            self.access_secret)

    def demo(self):
        api = tweepy.API(self.auth)
        
        public_tweets = api.home_timeline()
        for tweet in public_tweets:
            print(tweet.text)
