from src.rgbot import Bot
from decouple import config
import json

def main():
    # Lectura de variables de conexión
    CONSUMER_KEY = config('CONSUMER_KEY')
    CONSUMER_SECRET = config('CONSUMER_SECRET')
    ACCESS_KEY = config('ACCESS_KEY')
    ACCESS_SECRET = config('ACCESS_SECRET')
    
    # Inicializamos el bot
    bot = Bot(
        CONSUMER_KEY,
        CONSUMER_SECRET,
        ACCESS_KEY,
        ACCESS_SECRET
    )

    # Inicializamos la conexión
    bot.connect()

    # Obtenemos el último tweet del usuario de interés
    #lastTweet = (bot.getUtilLastTweets(idUser='ramonlopez54', qtyTweets=20))[0].text
    tweets = bot.getUtilLastTweets(idUser='ramonlopez54', qtyTweets=10)
    jsonTweet = '['
    if tweets != None:
        for tweet in tweets:
            print(tweet._json)

if __name__ == '__main__':
    main()