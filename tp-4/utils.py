import random

import numpy as np

def generar_numeros_aleatorios(distribucion, params):
    random.seed()
    numero_generado = None
    rnd = None

    if distribucion == "Uniforme":
        a, b = params
        rnd = random.uniform(0, 1)
        numero_generado = a + (b - a) * rnd

    elif distribucion == "Exponencial":
        lambda_param = params
        # Generamos un numero aleatorio utilizando la formula de la exponencial negativa
        rnd = random.uniform(0, 1)
        valor = np.log(1 - rnd) / -lambda_param
        numero_generado = round(valor, 4)

    return numero_generado, rnd

def generar_nueva_fila(estado_actual, con_objetos_temporales=False):
    nueva_fila = {
        "Nro. Evento": estado_actual.get("nro_evento", ""),
        "Evento": estado_actual.get("evento", ""),
        "Reloj": estado_actual.get("reloj", ""),
        "RND Próxima Llegada Fútbol": estado_actual.get("rnd_proxima_llegada_futbol", ""),
        "Tiempo entre llegadas Fútbol": estado_actual.get("tiempo_entre_llegada_futbol", ""),
        "Próxima Llegada Fútbol": estado_actual.get("proxima_llegada_futbol", ""),
        "RND Próxima Llegada Handball": estado_actual.get("rnd_proxima_llegada_handball", ""),
        "Tiempo entre llegadas Handball": estado_actual.get("tiempo_entre_llegada_handball", ""),
        "Próxima Llegada Handball": estado_actual.get("proxima_llegada_handball", ""),
        "RND Próxima Llegada Basketball": estado_actual.get("rnd_proxima_llegada_basketball", ""),
        "Tiempo entre llegadas Basketball": estado_actual.get("tiempo_entre_llegada_basketball", ""),
        "Próxima Llegada Basketball": estado_actual.get("proxima_llegada_basketball", ""),
        "RND Fin Ocupación": estado_actual.get("rnd_fin_ocupacion", ""),
        "Fin Ocupación": estado_actual.get("fin_ocupacion", ""),
        "Fin Limpieza": estado_actual.get("fin_limpieza", ""),
        "Estado Cancha": estado_actual.get("estado_cancha", ""),
        "Grupo Ocupando": estado_actual.get("grupo_ocupando", ""),
        "Cola Fútbol": estado_actual.get("cola_futbol", ""),
        "Cola Handball": estado_actual.get("cola_handball", ""),
        "Cola Basketball": estado_actual.get("cola_basketball", ""),
        "Contador Colas": estado_actual.get("contador_colas", ""),
        "Espera Acum. Fútbol": estado_actual.get("espera_acum_futbol", ""),
        "Contador Fútbol": estado_actual.get("contador_futbol", ""),
        "Espera Acum. Handball": estado_actual.get("espera_acum_handball", ""),
        "Contador Handball": estado_actual.get("contador_handball", ""),
        "Espera Acum. Basketball": estado_actual.get("espera_acum_basketball", ""),
        "Contador Basketball": estado_actual.get("contador_basketball", ""),
        "Día": estado_actual.get("dia", ""),
        "Tiempo Ocupación": estado_actual.get("tiempo_ocupacion", ""),
    }

    if con_objetos_temporales:
        nueva_fila["Nro. Grupo Temp."] = ", ".join([str(obj["id"]) for obj in estado_actual.get("objetos_temporales", [])])
        nueva_fila["Tipo Grupo Temp."] = ", ".join([obj["disciplina"] for obj in estado_actual.get("objetos_temporales", [])])
        nueva_fila["Llegada Grupo Temp."] = ", ".join([f'{obj["tiempo_llegada"]:.2f}' for obj in estado_actual.get("objetos_temporales", [])])
        nueva_fila["Estado Grupo Temp."] = ", ".join([obj["estado"] for obj in estado_actual.get("objetos_temporales", [])])

    return nueva_fila