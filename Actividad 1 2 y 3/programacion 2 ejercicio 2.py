def max_caracter(frase: str) -> tuple:
    conteo = {}
    

    for caracter in frase:
        if caracter in conteo:
            conteo[caracter] += 1
        else:
            conteo[caracter] = 1
            
    caracter_max = ""
    cantidad_max = 0
    
    for caracter, cantidad in conteo.items():
        if cantidad > cantidad_max:
            cantidad_max = cantidad
            caracter_max = caracter
            
    return (caracter_max, cantidad_max)


print(max_caracter("qwertyyyyyyy"))