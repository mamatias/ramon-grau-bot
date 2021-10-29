import tweepy

class Bot:
    def __init__(self, consumer_key, consumer_secret, access_key, access_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_key = access_key
        self.access_secret = access_secret
    
    def conectar(self):
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

    def obtenerUltimosTuits(self,idUsuario, cantidadTuits=1):
        ultimosTuits = self.client.user_timeline(screen_name=idUsuario, count=cantidadTuits)
        return ultimosTuits

    def posteaNuevoTuit(self, tuit='hola...'):
        pass


# Funciones úitles
def clasificaTuit(tuit='RT Ejemplo de tuit tipo retwittear',respuesta=None, tuitId=None, rt=None):
    # Retuit
    if rt != None:
        return {
            'id'            : tuitId,
            'tipo'          : 'Retuit',
            'respuesta'     : respuesta,
            'sigla'         : 'RT',
            'tuit'          : tuit[3:]
        }
    
    # Respeusta o reply
    elif respuesta != None:
        return {
            'id'            : tuitId,
            'tipo'          : 'Respuesta',
            'respuesta'     : respuesta,
            'sigla'         : 'RPLY',
            'tuit'          : tuit
        }

    # Cita
    elif 'https://t.co/' in tuit:
        return {
            'id'            : tuitId,
            'tipo'          : 'Cita',
            'respuesta'     : respuesta,
            'sigla'         : 'CITA',
            'tuit'          : tuit
        }

    # Default normal
    else:
        return {
            'id'            : tuitId,
            'tipo'          : 'Normal',
            'respuesta'     : respuesta,
            'sigla'         : 'DFLT',
            'tuit'          : tuit
        }
