from src.rgbot import Bot
from src.generator import generador
from decouple import config
from json import dumps
from src.tacho import Tacho, milog
from copy import deepcopy

# Toma los tweets en formato JSON y actualiza la publicación anterior y la nueva
def tweetsAlTacho(tweets, usuario):
    if usuario == None and tweets == None:
        milog(msg='Tweets o usuario en valor None')

    else:
        # tenemos inputs válidos
        nombreTacho = 'tacho-{0}'.format(usuario)
        tiposTweets = ['RT', 'RPLY', 'CITA', 'DFLT']
        tacho = Tacho(nombreTacho=nombreTacho)
        if not tacho.leerTacho():
            # No existe el archivo y por ende se debe crear
            for tipo in tiposTweets:
                tacho.agregarBolsa(nombreBolsa=tipo, bolsa=[])

        # Recorremos los tweets y actualizamos el almacenamiento
        for tweet in reversed(tweets):
            sigla = tweet.get('sigla')
            if sigla in tiposTweets:
                bolsa = tacho.obtenerBolsa(sigla)
                # bolsa = deepcopy(tacho.obtenerBolsa(sigla)) # Versión con deepcopy requiere usar el método de actualizar bolsas.
                tweet['estado'] = False
                # De la bolsa obtenida, se debe chequear si está vacío o si el ID del último tweet es menor que el tweet actual
                largoDatos = len(bolsa['datos'])
                if largoDatos == 0:
                    bolsa['datos'].append(tweet)

                else:
                    idUltimoTweet = bolsa['datos'][largoDatos-1].get('id')
                    idTweetActual = tweet.get('id')
                    if idTweetActual > idUltimoTweet:
                        bolsa['datos'].append(tweet)

            # print(json.dumps(tweet, indent=4))
        
        # Se cargó el tacho desde el archivo o se inicializó en memoria el tacho. Al final hay que guardarlo
        tacho.escribirTacho()


# Procesa el tacho con tweets y eventualmente generará texto original
def procesarTachoDeTweets(usuario, generadorNLP=None, tiposExcluidos=['RT','CITA','DFLT']):
    # Solo si el usuario no es None
    if usuario == None:
        milog(msg='Usuario no entregado para el análisis')
        return False

    else:
        tacho = Tacho(nombreTacho='tacho-{0}'.format(usuario))
        if not tacho.leerTacho():
            milog('Error al leer el tacho de análisis [{0}].'.format(usuario))
            return False

        else:
            tiposTweets = ['RT', 'RPLY', 'CITA', 'DFLT']
            for tipo in tiposTweets:
                bolsa = tacho.obtenerBolsa(nombreBolsa=tipo)
                cantidadTweets = len(bolsa['datos'])
                if cantidadTweets > 0:
                    # Se toma el último tweet y se procesa según su estado
                    ultimoTweet = bolsa['datos'][cantidadTweets-1]
                    if not ultimoTweet.get('estado'):
                        generarTextoNuevo(ultimoTweet, tipo, tiposExcluidos=tiposExcluidos, generadorNLP=generadorNLP)
                        ultimoTweet['estado'] = True
                        bolsa['datos'] = [ultimoTweet]
            
            tacho.escribirTacho()


# Función que genera el texto nuevo. Parte de NLP
def generarTextoNuevo(diccBase, tipo=0, tiposExcluidos=[], generadorNLP=None):
    textoBase = diccBase.get('tuit')
    # Solo se procesan los de tipo no excluido
    if tipo not in tiposExcluidos:
        if generadorNLP == None:
            milog(msg='=== No hay generador de texto ===\nTipo: {0}\nTexto: {1}'.format(tipo, textoBase))
        
        else:
            textoGenerado = generadorNLP.generarTexto(prompt=textoBase)
            milog('=== Nuevo tweet a procesar y texto generado ===')
            print('Tipo: {0}\nTexto original: {1}\nTexto generado: {2}'.format(
                tipo,
                textoBase,
                textoGenerado[0]
            ))
            return [textoBase, textoGenerado[0]]
    return


# Aplicación principal desde la cual se ejecutan las distintas acciones
#     * Obtener últimos tweets
#     * Actualizar registros en almacén local (Tacho)
#     * Mostrar anterior y nuevo
#     * Analizar últimos registros y generar textos
def app():
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

    # Creeamos el generador
    gen = generador()

    #Definición de usuarios chequeables
    usuariosChequeables = ['el_martolo']
    # usuariosChequeables = ['ramonlopez54']

    for usuario in usuariosChequeables:
        tweets = bot.obtenerUltimosTuits(idUsuario=usuario, cantidadTuits=50)
        # Se envían los tweets a los 4 tachos existentes: RT, RPLY, CITA y DFLT
        tweetsAlTacho(tweets=tweets, usuario=usuario)

        # Se procesa el tacho y se realiza la acción deseada (Generar texto)
        datos = procesarTachoDeTweets(usuario=usuario, generadorNLP=gen, tiposExcluidos=['RT', 'CITA'])
    
    pass


if __name__ == '__main__':
    app()