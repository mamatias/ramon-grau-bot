import json, os, logging

def milog(msg='Mensaje de prueba'):
    logging.basicConfig(format='[%(asctime)s] | %(message)s', datefmt='%I:%M:%S %p')
    logging.warning(msg)

class Tacho:
    def __init__(self) -> None:
        # Inicializamos variables
        self.nombreTacho = ''
        self.tacho = None
        self.rutaTacho = ''
        self.estado = None
        self.modoApertura = None
        
    # Método encargado de abrir un tacho
    def abrirTacho(self, nombreTacho='db'):
        # Hay que chequear que exista el archivo donde se guarda la información (JSON)
        self.rutaTacho = '.tacho/{0}.tch'.format(nombreTacho)
        if os.path.isfile(self.rutaTacho):
            archivoTacho = open(self.rutaTacho, 'rb')
            self.tacho = json.load(archivoTacho)
            archivoTacho.close()
            milog('Tacho leido con éxito.')
            self.estado = 'conectado'
            self.modoApertura = 'read'
            return True

        else:
            milog(msg='Tacho indicado [{0}] inexistente'.format(nombreTacho))
            return False


    # Método encargado de guardar los cambios
    def guardar(self):
        # Hay que chequear el estado y luego si existe el tacho
        if self.estado != 'conectado':
            milog(msg='No se puede guardar el tacho si no se está conectado')
            return False

        elif self.nombreTacho == '' or self.tacho == None:
            milog(msg='No se puede guardar el tacho. Tacho sin nombre o vacío (corrupto)')
            return False

        else:
            # Aquí se tienen 3 opciones
            opciones = '''
            1. El archivo es nuevo
            '''

    # Método que agrega "bolsa" al tacho. Viene a ser algo así como una tabla
    def agregarBolsa(self, nombreBolsa='bolsa', datos=[]):
        bolsa = {
            'nombre' : nombreBolsa,
            'datos' : datos
        }
        # Se agrega la bolsa al tacho.

    # Renueva los datos de la bolsa
    def actualizarBolsa(self, nombreBolsa, datos):
        if nombreBolsa == None or datos == None or self.estado != 'conectado':
            return False
        else:
            # Se debe buscar si existe la bolsa y luego actualizarle los datos
            pass


    # Función encargada de crear una nueva base de datos (JSON)
    def nuevoTacho(self, nombreTacho='tacho'):
        # Debería quedar en la carpeta .tacho/
        os.mkdir('.tacho')
        archivoTacho = open('.tacho/{0}.tch'.format(nombreTacho),'wb')
        archivoTacho.close()
        milog('Tacho [{0}] creado con éxito.'.format(nombreTacho))

    # Para un análisis externo, se retorna el diccionario que representa el 
    def retornaTacho(self):
        if self.estado == 'conectado':
            return self.tacho
        else:
            return None

if __name__ == '__main__':
    # Rutina de prueba
    tacho = Tacho()
    if not tacho.abrirTacho(nombreTacho='_test'):
        # Tacho inexistente. Se procede a crear uno nuevo
        milog('Tacho inexistente. Se procede a crear uno nuevo')
        tacho.nuevoTacho(nombreTacho='_test')

    print(json.dumps(tacho.retornaTacho(), indent=4))