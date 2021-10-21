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

        self.client = tweepy.API(self.auth)

    def demo(self):
        public_tweets = self.client.home_timeline()
        for tweet in public_tweets:
            print(tweet.text)
            print('\n\n')

    def getUtilLastTweets(self,idUser, qtyTweets=1):
        lastTweet = self.client.user_timeline(screen_name=idUser, count=qtyTweets)
        return lastTweet

    def postNewTweet(self, tweet='hola...'):
        pass
