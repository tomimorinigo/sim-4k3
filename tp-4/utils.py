import random

import numpy as np

def generar_numeros_aleatorios(distribucion, tamano_muestra, params):
    random.seed()
    numeros = []

    if distribucion == "Uniforme":
        a, b = params
        for _ in range(tamano_muestra):
            numeros.append(round(random.uniform(a, b), 4))
    
    elif distribucion == "Exponencial":
        lambda_param = params
        for _ in range(tamano_muestra):
            # Generamos un numero aleatorio utilizando la formula de la exponencial negativa
            rnd = random.uniform(0, 1)
            print(f"rnd: {rnd}")
            valor = np.log(1 - rnd) / -lambda_param
            print(f"valor: {valor}")
            numeros.append(round(valor, 4))
            print(f"Numeros: {numeros}")
    
    elif distribucion == "Normal":
        mu, sigma = params
        i = 0 # Cantidad de numeros aleatorios generados

        while i < tamano_muestra:
            # Generamos un numero aleatorio utilizando la formula de Box Muller
            r1 = random.uniform(0, 1)
            r2 = random.uniform(0, 1)
            z1 = np.sqrt(-2 * np.log(r1)) * np.sin(2 * np.pi * r2)
            z2 = np.sqrt(-2 * np.log(r1)) * np.cos(2 * np.pi * r2)
            numeros.append(round(z1 * sigma + mu, 4))
            i += 1

            # Si i es menor que el tamaño de la muestra, generamos otro numero
            # aleatorio utilizando la segunda parte de la formula de Box Muller
            # Esto soluciona el problema de que tamano_muestra sea impar
            if i < tamano_muestra:
                numeros.append(round(z2 * sigma + mu, 4))
                i += 1
    
    return numeros
