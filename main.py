from src.rgbot import Bot
import src.utiutil as myutil
from src.generator import generador
from decouple import config
from json import dump

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
    if tweets != None:
        for tweet in tweets:
            jsonTweet = tweet._json
            print(dump(tweet))
            print(tweet.text)

    Gen = generador()
    texto = Gen.generarTexto(lastTweet)
    print(texto[0])

    # Shuffle de letras en el tweet
    lastTweetShuffled = myutil.randomizeString(lastTweet)
    print(lastTweetShuffled)

    # Posteamos el tweet shuffleado, Ja!
    bot.postNewTweet(lastTweetShuffled)

    # Hacemos la demo
    # bot.demo()


if __name__ == '__main__':
    main()