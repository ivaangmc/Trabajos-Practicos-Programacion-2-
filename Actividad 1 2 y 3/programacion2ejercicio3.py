# dada una frase y un diccionario con con los pesos de las palabras
# calcular el porcentaje de positividad del texto
# Buscar las palabras que estan en la frase y calcular el promedio segun el peso del diccionario
# si la palabra no esta en el diccionario el peso es cero


diccionario_pesos = {
    "estoy": 5,
    "feliz": 10
}

def positividad(frase):
    palabras = frase.split()
    suma_pesos = 0
    cantidad_palabras = len(palabras)

    for p in palabras:
        if p in diccionario_pesos:
            suma_pesos = suma_pesos + diccionario_pesos[p]

    if cantidad_palabras == 0:
        return 0.0
    
    return suma_pesos / cantidad_palabras

frase = "estoy en un mundo feliz"
promedio = positividad(frase)

print("promedio", promedio)
