import json, os, logging, random

def milog(msg='Mensaje de prueba', debug=True):
    if debug:
        logging.basicConfig(format='[%(asctime)s] | %(message)s', datefmt='%I:%M:%S %p')
        logging.warning(msg)

class Tacho:
    def __init__(self, nombreTacho='tacho', debug=False) -> None:
        # Versión
        self.__version__ = '1.0.0'
        # Inicializamos variables
        self.nombreTacho = nombreTacho
        self.tacho = [{
            'nombre':'bolsa-inicial',
            'datos':[{
                'numero':1,
                'texto':'texto',
                'boolean':False
            }]
        }]
        self.rutaTacho = '.tacho/{0}.json'.format(nombreTacho)
        self.estado = 'iniciado'
        self.debug = debug

    ####################################################################
    ######             Métodos para manejar el tacho              ######
    ####################################################################

    # Retornar versión de forma fácil
    def version(self):
        print(self.__version__)

    # Leer un tacho desde un archivo
    def leerTacho(self):
        # Primero se chequea que exista el archivo y luego se carga lo que corresponda
        if os.path.isfile(self.rutaTacho):
            # Existe y se carga
            with open(self.rutaTacho, 'r') as outfile:
                self.tacho = json.load(outfile)
            milog(msg='Se carga el tacho [{0}]'.format(self.nombreTacho), debug=self.debug)
            return True

        else:
            milog(msg='El tacho indicado [{0}] no existe'.format(self.nombreTacho), debug=self.debug)
            return False


    # Escribir un tacho en un archivo tch
    def escribirTacho(self):
        # Se pregunta que no exista el tacho
        if os.path.isfile(self.rutaTacho):
            # Existe y por ende se borra y se crea nuevamente
            self.borrarTacho()

        # Crear el tacho. Primero ver si ya existe el directorio
        if not os.path.isdir('.tacho'):
            os.mkdir('.tacho')
        with open(self.rutaTacho, 'w') as outfile:
            json.dump(self.tacho, outfile)

        milog('Tacho [{0}] escrito con éxito.'.format(self.nombreTacho), debug=self.debug)
        return True


    # Muestra el tacho (print)
    def mostrarTacho(self):
        print(json.dumps(self.tacho, indent=4))
    
    # Encargado de borrar un tacho del disco
    def borrarTacho(self):
        # Se pregunta que no exista el tacho
        if os.path.isfile(self.rutaTacho):
            # Existe y por ende no se puede guardar a menos que sea forzado
            os.remove(self.rutaTacho)
            milog(msg='Tacho [{0}] se borra con éxito', debug=self.debug)
            return True
            
        else:
            milog(msg='El tacho [{0}] no está guardado en disco y por ende no se puede borrar', debug=self.debug)
            return False

    # Encargado de buscar si existe una determinada bolsa. Retorna -1 o índice de donde está
    def buscarBolsa(self, nombreBolsa):
        # Recorremos todas las bolsas
        for (idx, bolsa) in enumerate(self.tacho):
            if bolsa.get('nombre') == nombreBolsa:
                milog(msg='Bolsa [{0}] encontrada en índice [{1}]'.format(nombreBolsa, idx), debug=self.debug)
                return idx
        
        milog(msg='Bolsa [{0}] no encontrada'.format(nombreBolsa), debug=self.debug)
        return -1

    
    # Encargado de agregar una bolsa en el tacho
    def agregarBolsa(self, nombreBolsa='bolsa', bolsa={None}):
        # Se debe chequear que no exista la bolsa pues deben ser únicas en nombre
        idx = self.buscarBolsa(nombreBolsa)
        if idx == -1:
            self.tacho.append({
                'nombre' : nombreBolsa,
                'datos' : bolsa
            })
            milog(msg='Bolsa [{0}] agregada'.format(nombreBolsa), debug=self.debug)
            return True

        else:
            # Ya existe así que no se crea
            milog(msg='Bolsa [{0}] ya existe en índice [{1}]'.format(nombreBolsa, idx), debug=self.debug)
            return False


    # Encargado de entregar una bolsa
    def obtenerBolsa(self, nombreBolsa):
        # Buscamos la bolsa. Índice -1 es que no la encontró
        idx = self.buscarBolsa(nombreBolsa)
        if idx != -1:
            milog(msg='Bolsa [{0}] encontrada y retornada'.format(nombreBolsa), debug=self.debug)
            return self.tacho[idx]

        return False

    # Encargado de actualizar los datos de una bolsa
    def actualizarBolsa(self, nombreBolsa, datosBolsa):
        # Partimos buscado donde stá la bolsa.
        idx = self.buscarBolsa(nombreBolsa)
        if idx != -1:
            self.tacho[idx]['datos'] = datosBolsa
            milog(msg='Bolsa [{0}] encontrada y actualizada'.format(nombreBolsa), debug=self.debug)
            return True

        milog(msg='Bolsa [{0}] no encontrada'.format(nombreBolsa), debug=self.debug)
        return False


####################################################################
######                   Rutina de prueba                     ######
####################################################################

if __name__ == '__main__':
    # Rutina de prueba
    NOMBRETACHO = 'tacho'
    DEBUG = False

    # Se crea un tacho
    tacho = Tacho(NOMBRETACHO, DEBUG)
    tacho.version()

    # Se intanta leer el tacho
    tacho.leerTacho(NOMBRETACHO)

    # Se muestra el tacho en línea de comandos
    print('\nTacho con datos iniciales:')
    tacho.mostrarTacho()

    # Creamos una bolsa con datos ficticios
    nombreBolsa = 'bolsa-demo'
    nuevosDatos = {
        'id' : random.randint(0,999999999),
        'valor' : (random.randint(0,999)*1.0)/100.0
    }

    mibolsa = tacho.obtenerBolsa(nombreBolsa)
    if not mibolsa:
        tacho.agregarBolsa(nombreBolsa, [nuevosDatos])
    else:
        mibolsa['datos'].append(nuevosDatos)
        tacho.actualizarBolsa(nombreBolsa, mibolsa['datos'])

    # Se muestra el tacho en línea de comandos
    print('\nTacho con datos nuevos:')
    tacho.mostrarTacho()

    # Se muestra una bolsa
    print('\nBolsa buscada y mostrada en formato entendible:')
    print(json.dumps(tacho.obtenerBolsa(nombreBolsa), indent=4))

    # Guardamos los cambios
    tacho.escribirTacho()

    # tacho.borrarTacho()
