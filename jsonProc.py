from src.rgbot import Bot, clasificaTuit
from decouple import config
import json
import argparse

def main(modo='texto', cantidad = 5):
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
    bot.conectar()

    # Obtenemos los últimos tweets 
    tweets = bot.obtenerUltimosTuits(idUsuario='el_martolo', cantidadTuits=cantidad)
    if tweets != None:
        tweetsJSON = []
        for tweet in tweets:
            tweetObj = tweet._json
            if modo == 'texto':
                obj = clasificaTuit(
                    tuit=tweetObj.get('text'),
                    respuesta=tweetObj.get('in_reply_to_status_id'),
                    tuitId=tweetObj.get('id'),
                    rt=tweetObj.get('retweeted_status')
                )
                print(json.dumps(obj, sort_keys=True, indent=4))
                print('\n')
            elif modo == 'json':
                print(json.dumps(tweet._json, indent=4))
                print('\n')
                # tweetsJSON.append(json.load(tweet._json))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--modo', help='Modo a utilizar. [texto]: Solo texto del tweet. [json]: Representación JSON de low tweets.')
    parser.add_argument('-c', '--cantidad', help='Cantidad de tweets a obtener')
    parser.add_argument('-v', '--version', help='Versión del programa', action='store_true')
    args = parser.parse_args()
    if args.cantidad:
        cantidad = args.cantidad
    else:
        cantidad = 5

    if args.modo == 'texto' or args.modo == None:
        main(cantidad=cantidad)
    elif args.modo == 'json':
        main('json', cantidad=cantidad)
    elif args.version:
        print(u'Versión 1.0.0')