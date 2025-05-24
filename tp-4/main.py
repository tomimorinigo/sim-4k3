import streamlit as st
import utils

st.set_page_config(
    page_title="Simulador Polideportivo",
    layout="wide"
)

st.title("Simulador Polideportivo General Paz")

with st.sidebar:
    st.header("Parámetros")

    st.subheader("Parámetros - Tiempo de ejecución y visualización")
    tiempo = st.number_input("Tiempo total a simular (minutos):",
        min_value=1,
        help="El tiempo de ejecución es el tiempo que se simula en minutos",
    )

    if tiempo <= 0:
        st.error("El valor mínimo (a) debe ser menor que el valor máximo (b)")

    iteraciones_mostrar = st.number_input(
        "Cantidad de iteraciones a mostrar:",
        min_value=1,
        max_value=100000,
        value=10
    )

    min_inicio_mostrar = st.number_input(
        "Minuto de inicio a mostrar:",
        min_value=0,
        max_value=1000000,
        value=0
    )

    tab_futbol, tab_handball, tab_basketball = st.tabs(["Fútbol", "Handball", "Basketball"])

    with tab_futbol:
        st.subheader("Parámetros - Grupos de Futbol")


        media_llegadas_futbol = st.number_input(
            "Media de Exponencial Negativa (Llegadas):",
            min_value=1,
            max_value=10000,
            value=10
        )

        col1_futbol, col2_futbol = st.columns(2)

        with col1_futbol:
            limite_inf_ocupacion_futbol = st.number_input(
                "Limite inferior de ocupacion de cancha (mins):",
                min_value=1,
                max_value=10000,
                value=80
            )

        with col2_futbol:
            limite_sup_ocupacion_futbol = st.number_input(
                "Limite superior de ocupacion de cancha (mins):",
                min_value=1,
                max_value=10000,
                value=100
            )

    with tab_handball:
        st.subheader("Parámetros - Grupos de Handball")

        col1_handball_llegadas, col2_handball_llegadas, = st.columns(2)

        with col1_handball_llegadas:
            limite_inf_llegadas_handball = st.number_input(
                "Limite inferior de llegadas handball (horas):",
                min_value=1,
                max_value=1000,
                value=10
            )

        with col2_handball_llegadas:
            limite_sup_llegadas_handball = st.number_input(
                "Limite superior de llegadas handball (horas):",
                min_value=1,
                max_value=1000,
                value=14
            )

        col1_handball_ocupacion, col2_handball_ocupacion, = st.columns(2)

        with col1_handball_ocupacion:
            limite_inf_ocupacion_handball = st.number_input(
                "Limite inferior de ocupacion de cancha handball (mins):",
                min_value=1,
                max_value=10000,
                value=60
            )

        with col2_handball_ocupacion:
            limite_sup_ocupacion_handball = st.number_input(
                "Limite superior de ocupacion de cancha handball (mins):",
                min_value=1,
                max_value=10000,
                value=100
            )

    with tab_basketball:
        st.subheader("Parámetros - Grupos de Basketball")

        col1_basketball_llegadas, col2_basketball_llegadas, = st.columns(2)

        with col1_basketball_llegadas:
            limite_inf_llegadas_basketball = st.number_input(
                "Limite inferior de llegadas basketball (horas):",
                min_value=1,
                max_value=1000,
                value=6
            )

        with col2_basketball_llegadas:
            limite_sup_llegadas_basketball = st.number_input(
                "Limite superior de llegadas basketball (horas):",
                min_value=1,
                max_value=1000,
                value=10
            )

        col1_basketball_ocupacion, col2_basketball_ocupacion, = st.columns(2)

        with col1_basketball_ocupacion:
            limite_inf_ocupacion_basketball = st.number_input(
                "Limite inferior de ocupacion de cancha basketball (mins):",
                min_value=1,
                max_value=10000,
                value=70
            )

        with col2_basketball_ocupacion:
            limite_sup_ocupacion_basketball = st.number_input(
                "Limite superior de ocupacion de cancha basketball (mins):",
                min_value=1,
                max_value=10000,
                value=130
            )

    
    generar_btn = st.button("Arrancar simulación", type="primary")

def generar_llegada(disciplina):
    if disciplina == "Futbol":
        lambda_param = 1 / media_llegadas_futbol
        params = (lambda_param)
        return utils.generar_numeros_aleatorios("Exponencial", 10, params)
    elif disciplina == "Handball":
        a, b = limite_inf_llegadas_handball, limite_sup_llegadas_handball
        params = (a, b)
        return utils.generar_numeros_aleatorios("Uniforme", 10, params)
    elif disciplina == "Basketball":
        a, b = limite_inf_llegadas_basketball, limite_sup_llegadas_basketball
        params = (a, b)
        return utils.generar_numeros_aleatorios("Uniforme", 10, params)
    

def generar_ocupacion(disciplina):
    if disciplina == "Futbol":
        a, b = limite_inf_ocupacion_futbol, limite_sup_ocupacion_futbol
        params = (a, b)
        return utils.generar_numeros_aleatorios("Uniforme", 1, params)
    elif disciplina == "Handball":
        a, b = limite_inf_ocupacion_handball, limite_sup_ocupacion_handball
        params = (a, b)
        return utils.generar_numeros_aleatorios("Uniforme", 1, params)
    elif disciplina == "Basketball":
        a, b = limite_inf_ocupacion_basketball, limite_sup_ocupacion_basketball
        params = (a, b)
        return utils.generar_numeros_aleatorios("Uniforme", 1, params)


# Constantes
max_iteraciones = 1000000
limpieza_duracion = 10

# Variables iniciales

eventos = []
vector_estado = []

reloj = 0
nro_evento = 0
estado_cancha = "Disponible"
grupo_ocupando = None
colas = {
    "Futbol": 0,
    "Handball": 0,
    "Basketball": 0
}
contador_colas = 0
esperas_acum = {
    "Futbol": 0,
    "Handball": 0,
    "Basketball": 0
}
contadores = {
    "Futbol": 0,
    "Handball": 0,
    "Basketball": 0
}
dia = 0
tiempo_ocupacion_acum = 0
objetos_temporales = []

disciplinas = ["Futbol", "Handball", "Basketball"]

if generar_btn:
    # Generar llegadas iniciales
    for d in disciplinas:
        llegada = generar_llegada(d)
        eventos.append({
            "evento": f"Llegada Grupo de {d}",
            "disciplina": d,
            "tiempo_entre_llegada": round(llegada[0] * 60, 2),
            "proximo_evento": round(llegada[0] * 60, 2),
        })
        
    # Simulacion
    for iteracion in range(max_iteraciones):
        if reloj >= tiempo:
            break

        # Actualizamos nuestro numero de dia
        dia = reloj // 1440  # 1440 minutos en un dia

        eventos.sort(key=lambda x: x["proximo_evento"])
        evento_actual = eventos.pop(0)
        reloj = evento_actual["proximo_evento"]

        disciplina = evento_actual.get("disciplina", "")
        evento = evento_actual["evento"]

        if evento == f"Llegada Grupo de {disciplina}":
            # Agregamos el evento de llegada del siguiente grupo
            tiempo_llegada = generar_llegada(disciplina)
            eventos.append({
                "evento": f"Llegada Grupo de {disciplina}",
                "disciplina": disciplina,
                "tiempo_entre_llegada": round(tiempo_llegada[0] * 60, 2),
                "proximo_evento": reloj + round(tiempo_llegada[0] * 60, 2),
            })

            if contador_colas > 6:
                # Si hay mas de 6 grupos esperando, no se permite la llegada de nuevos grupos
                continue

            # Creamos un objeto temporal para el grupo
            objeto_temporal = {
                "disciplina": disciplina,
                "tiempo_llegada": reloj,
                "tiempo_espera": 0,
                "estado": "Esperando"
            }

            if estado_cancha == "Disponible":
                # Pasamos a ocupada la cancha y definimos el grupo que la ocupa
                estado_cancha = "Ocupada"
                objeto_temporal["estado"] = "En Juego"
                grupo_ocupando = disciplina
                # Generamos el tiempo de ocupacion
                tiempo_ocupacion = generar_ocupacion(disciplina)

                # Agregamos el evento de fin de ocupacion
                eventos.append({
                    "evento": f"Fin Ocupacion",
                    "disciplina": disciplina,
                    "tiempo_ocupacion": round(tiempo_ocupacion[0], 2),
                    "proximo_evento": reloj + round(tiempo_ocupacion[0], 2),
                })

                contadores[disciplina] += 1

            if estado_cancha == "Ocupada" or estado_cancha == "Limpieza":
                # Si la cancha esta ocupada o en limpieza, agregamos el grupo a la cola
                colas[disciplina] += 1
                contador_colas += 1
                objeto_temporal["estado"] = "Esperando"
            
            objetos_temporales.append(objeto_temporal)

        if evento == "Fin Ocupacion":
            # Se libera la cancha
            estado_cancha = "Limpieza"
            grupo_ocupando = None

            # Agregamos el evento de fin de limpieza
            eventos.append({
                "evento": "Fin Limpieza",
                "proximo_evento": reloj + limpieza_duracion,
            })

            # Sumamos el tiempo de ocupacion a nuestro acumulador
            tiempo_ocupacion_acum += evento_actual["tiempo_ocupacion"]
           
            # Al grupo que estaba ocupando, lo borramos de los objetos temporales
            for objeto in objetos_temporales:
                if objeto["estado"] == "En Juego":
                    objetos_temporales.remove(objeto)
                    break

        if evento == "Fin Limpieza":
            # Se termina de limpiar la cancha
            # Verificamos las colas
            if contador_colas > 0:
                objetos_temporales.sort(key=lambda x: x["tiempo_llegada"])
                objetos_temporales[0]

                if objetos_temporales[0]["disciplina"] == "Basketball":
                    tiene_otros_deportes = any(
                        grupo["disciplina"] in ["Futbol", "Handball"] for grupo in objetos_temporales
                    )

                    if tiene_otros_deportes:
                        # Si hay otros deportes, estos tienen prioridad
                        siguiente_grupo = next(
                            (grupo for grupo in objetos_temporales if grupo["disciplina"] in ["Futbol", "Handball"]),
                            None
                        )

                estado_cancha = "Ocupada"
                objetos_temporales[0]["estado"] = "En Juego"
                grupo_ocupando = objetos_temporales[0]["disciplina"]

                # Generamos el tiempo de ocupacion
                tiempo_ocupacion = generar_ocupacion(objetos_temporales[0]["disciplina"])

                # Agregamos el evento de fin de ocupacion
                eventos.append({
                    "evento": f"Fin Ocupacion",
                    "disciplina": disciplina,
                    "tiempo_ocupacion": round(tiempo_ocupacion[0], 2),
                    "proximo_evento": reloj + round(tiempo_ocupacion[0], 2),
                })

            else:
                estado_cancha = "Disponible"
                continue

# TODO: 
# 1. Calcular tiempos de esperas. Y sacar estadisticas con el tiempo de ocupacion tmb
# 2. Generar vector de estados
# 3. Construir tabla y mostrarla


           