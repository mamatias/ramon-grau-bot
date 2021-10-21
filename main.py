import json
from src.rgbot import Bot
import src.utiutil as myutil
from decouple import config

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
    lastTweet = (bot.getUtilLastTweets(idUser='ManuelDTP', qtyTweets=1))[0].text
    if lastTweet == None:
        print('No hay last tweet aun!')
    else:
        # convert object to string
        print(lastTweet)

    # Shuffle de letras en el tweet
    lastTweetShuffled = myutil.randomizeString(lastTweet)
    print(lastTweetShuffled)

    # Posteamos el tweet shuffleado, Ja!
    bot.postNewTweet(lastTweetShuffled)

    # Hacemos la demo
    # bot.demo()


if __name__ == '__main__':
    main()