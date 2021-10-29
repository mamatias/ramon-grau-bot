from typing import TextIO


with open('texto.txt') as f:
    lines = f.readlines()

texto = lines[0]
#print(texto[texto.find('_json')+5:texto.find('_json')+20])
inicio = 0
jeisons = []
while True:
    indice = texto.find('_json',inicio+5)
    # print('Indice: {0}'.format(indice))
    if indice == -1:
        linea = texto[inicio:indice]
        jeisons.append(linea)
        # print('\n{0}'.format(linea[0:20]))
        break
    else:
        if inicio == 0:
            inicio = indice
        else:
            linea = texto[inicio:indice]
            jeisons.append(linea)
            # print('\n{0}'.format(linea[0:20]))
            inicio = indice


for line in jeisons:
    print(line)