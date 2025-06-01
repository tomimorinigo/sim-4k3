import streamlit as st
import utils
import pandas as pd

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

def inicializar_tabla_estado():
    """
    Inicializa la tabla en session_state si no existe
    """
    if 'tabla_estados' not in st.session_state:
        st.session_state.tabla_estados = pd.DataFrame()

def agregar_fila_tabla(vector_estado):
    """
    Agrega una nueva fila a la tabla acumulativa con un único estado
    
    Args:
        vector_estado (list): Lista que contiene un diccionario con el estado actual del evento
    """
    # Inicializar tabla si no existe
    inicializar_tabla_estado()
    
    # Extraer el diccionario del vector (último elemento si hay varios)
    if isinstance(vector_estado, list) and len(vector_estado) > 0:
        estado_actual = vector_estado[-1]  # Tomar el último estado
    elif isinstance(vector_estado, dict):
        estado_actual = vector_estado  # Si es directamente un diccionario
    else:
        st.error("Error: vector_estado debe ser una lista con diccionarios o un diccionario")
        return
    
    # Procesar objetos temporales - manejo robusto de casos vacíos
    #objetos_temp = estado_actual.get("objetos_temporales", [])
    #temp_str = ""
    
    # Verificar si existe y no está vacío

    #    if objetos_temp and len(objetos_temp) > 0:
    #   temp_str = "; ".join([
    #       f"Disciplina: {obj.get('disciplina', 'N/A')}, "
    #       f"T.Llegada: {obj.get('tiempo_llegada', 'N/A')}, "
    #       f"T.Espera: {obj.get('tiempo_espera', 'N/A')}, "
    #       f"Estado: {obj.get('estado', 'N/A')}"
    #       for obj in objetos_temp
    #       if obj  # Filtrar objetos None o vacíos
    #   ])
    #else:
    #   temp_str = "Sin objetos temporales"
    
    # Crear nueva fila
    nueva_fila = {
        "Nro. Evento": estado_actual.get("nro.evento", ""),
        "Evento": estado_actual.get("evento", ""),
        "Reloj": estado_actual.get("reloj", ""),
        "Próxima Llegada Fútbol": estado_actual.get("proxima_llegada_futbol", ""),
        "Próxima Llegada Handball": estado_actual.get("proxima_llegada_handball", ""),
        "Próxima Llegada Basketball": estado_actual.get("proxima_llegada_basketball", ""),
        "Fin Ocupación": estado_actual.get("fin_ocupacion", ""),
        "Fin Limpieza": estado_actual.get("fin_limpieza", ""),
        "Estado Cancha": estado_actual.get("estado_cancha", ""),
        "Grupo Ocupando": estado_actual.get("grupo_ocupando", ""),
        "Cola Fútbol": estado_actual.get("cola_futbol", ""),
        "Cola Handball": estado_actual.get("cola_handball", ""),
        "Cola Basketball": estado_actual.get("colas_basketball", ""),
        "Contador Colas": estado_actual.get("contador_colas", ""),
        "Espera Acum. Fútbol": estado_actual.get("espera_acum_futbol", ""),
        "Contador Fútbol": estado_actual.get("contador_futbol", ""),
        "Espera Acum. Handball": estado_actual.get("espera_acum_handball", ""),
        "Contador Handball": estado_actual.get("contador_handball", ""),
        "Espera Acum. Basketball": estado_actual.get("espera_acum_basketball", ""),
        "Contador Basketball": estado_actual.get("contador_basketball", ""),
        "Día": estado_actual.get("dia", ""),
        "Tiempo Ocupación": estado_actual.get("tiempo_ocupacion", "")
    }
    
    # Agregar fila al DataFrame existente
    nueva_fila_df = pd.DataFrame([nueva_fila])
    st.session_state.tabla_estados = pd.concat(
        [st.session_state.tabla_estados, nueva_fila_df], 
        ignore_index=True
    )

def mostrar_tabla_acumulativa(titulo="Tabla de Estados Acumulativa", container=None):
    """
    Muestra la tabla acumulativa actual
    
    Args:
        titulo (str): Título para mostrar encima de la tabla
        container: Container de Streamlit donde mostrar la tabla (opcional)
    """
    # Inicializar si no existe
    inicializar_tabla_estado()
    
    # Usar container si se proporciona, sino usar st directamente
    ctx = container if container else st
    
    ctx.subheader(titulo)
    
    if not st.session_state.tabla_estados.empty:
        # Mostrar la tabla completa
        ctx.dataframe(
            st.session_state.tabla_estados,
            use_container_width=True,
            hide_index=True
        )
        
        # Mostrar información de la tabla
        ctx.info(f"Total de eventos registrados: {len(st.session_state.tabla_estados)}")
        
        # Opción para descargar como CSV
        csv = st.session_state.tabla_estados.to_csv(index=False)
        ctx.download_button(
            label="Descargar tabla completa como CSV",
            data=csv,
            file_name="estados_simulacion.csv",
            mime="text/csv"
        )
    else:
        ctx.warning("No hay datos para mostrar")

def actualizar_tabla_en_contenedor(contenedor):
    """
    Actualiza la tabla en un contenedor específico
    
    Args:
        contenedor: Container de Streamlit donde actualizar la tabla
    """
    with contenedor:
        mostrar_tabla_acumulativa("Tabla de Estados Acumulativa")

def limpiar_tabla():
    """
    Limpia la tabla acumulativa (útil para reiniciar simulación)
    """
    st.session_state.tabla_estados = pd.DataFrame()
    st.success("Tabla limpiada")

def obtener_tabla_actual():
    """
    Retorna el DataFrame actual para usar en otros lugares
    
    Returns:
        pandas.DataFrame: DataFrame con todos los estados acumulados
    """
    inicializar_tabla_estado()
    return st.session_state.tabla_estados


# Constantes
max_iteraciones = 1000000
limpieza_duracion = 10
cant_iteraciones_mostrar = iteraciones_mostrar

# Variables iniciales

eventos = []
vector_estado = []
vector_estado_anterior = []

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
                contador_colas -= 1
                objetos_temporales[0]["estado"] = "En Juego"
                grupo_ocupando = objetos_temporales[0]["disciplina"]
                #acumulo los tiempos de espera segun la disciplina.
                if disciplina == "Futbol":
                    esperas_acum["Futbol"] += reloj - objetos_temporales[0]["tiempo_llegada"]
                elif disciplina == "Handball":
                    esperas_acum["Handball"] += reloj - objetos_temporales[0]["tiempo_llegada"]
                else:
                    esperas_acum["Basketball"] += reloj - objetos_temporales[0]["tiempo_llegada"]

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
        proxima_llegada_futbol = next((evento["proximo_evento"] for evento in eventos if evento["evento"] == "Llegada Grupo de Futbol" and evento["disciplina"] == "Futbol"), None)
        proxima_llegada_basketball = next((evento["proximo_evento"] for evento in eventos if evento["evento"] == "Llegada Grupo de Basketball" and evento["disciplina"] == "Basketball"), None)
        proxima_llegada_handball = next((evento["proximo_evento"] for evento in eventos if evento["evento"] == "Llegada Grupo de Handball" and evento["disciplina"] == "Handball"), None)
        fin_limpieza = ""
        grupo_ocupando = ""
        if estado_cancha == "Limpieza":
            fin_limpieza = reloj + limpieza_duracion
        elif estado_cancha == "Ocupada":
            grp_ocupando = grupo_ocupando
        if vector_estado == []:
            vector_estado.append({
                "nro.evento": iteracion,
                "evento" : evento,
                "reloj" : reloj,
                "proxima_llegada_futbol": proxima_llegada_futbol,
                "proxima_llegada_handball": proxima_llegada_handball,
                "proxima_llegada_basketball": proxima_llegada_basketball,
                "fin_ocupacion": reloj + round(tiempo_llegada[0] * 60, 2),
                "fin_limpieza": fin_limpieza,
                "estado_cancha": estado_cancha,
                "grupo_ocupando": grp_ocupando,
                "cola_futbol": colas["Futbol"],
                "cola_handball": colas["Handball"],
                "colas_basketball": colas["Basketball"],
                "contador_colas": contador_colas,
                "espera_acum_futbol":esperas_acum["Futbol"],
                "contador_futbol": contadores["Futbol"],
                "espera_acum_handball":esperas_acum["Handball"],
                "contador_handball": contadores["Handball"],
                "espera_acum_basketball":esperas_acum["Basketball"],
                "contador_basketball": contadores["Basketball"],
                "dia":dia,
                "tiempo_ocupacion":tiempo_ocupacion_acum
            })
        else:
            vector_estado_anterior = vector_estado.pop()
            vector_estado.append({
                "nro.evento": iteracion,
                "evento" : evento,
                "reloj" : reloj,
                "proxima_llegada_futbol": proxima_llegada_futbol,
                "proxima_llegada_handball": proxima_llegada_handball,
                "proxima_llegada_basketball": proxima_llegada_basketball,
                "fin_ocupacion": reloj + round(tiempo_llegada[0] * 60, 2),
                "fin_limpieza": fin_limpieza,
                "estado_cancha": estado_cancha,
                "grupo_ocupando": grp_ocupando,
                "cola_futbol": colas["Futbol"],
                "cola_handball": colas["Handball"],
                "colas_basketball": colas["Basketball"],
                "contador_colas": contador_colas,
                "espera_acum_futbol":esperas_acum["Futbol"],
                "contador_futbol": contadores["Futbol"],
                "espera_acum_handball":esperas_acum["Handball"],
                "contador_handball": contadores["Handball"],
                "espera_acum_basketball":esperas_acum["Basketball"],
                "contador_basketball": contadores["Basketball"],
                "dia":dia,
                "tiempo_ocupacion":tiempo_ocupacion_acum
            })
        if reloj >= min_inicio_mostrar and cant_iteraciones_mostrar >= 1:
            cant_iteraciones_mostrar -= 1
            agregar_fila_tabla(vector_estado)
    mostrar_tabla_acumulativa()
                

promedio_espera = {
    "espera_futbol" : esperas_acum["Futbol"]/contadores["Futbol"] if contadores["Futbol"] != 0 else 0,
    "espera_basket" : esperas_acum["Basketball"]/contadores["Basketball"] if contadores["Basketball"] != 0 else 0,
    "espera_handball" : esperas_acum["Handball"]/contadores["Handball"] if contadores["Handball"] != 0 else 0}

print(f"promedio espera futbol: {promedio_espera['espera_futbol']}\n Promedio espera Handball: {promedio_espera['espera_handball']}\n Promedio espera basket: {promedio_espera['espera_basket']}")
print(f"promedio de ocupacion por dia: {tiempo_ocupacion_acum/dia if dia != 0 else tiempo_ocupacion_acum}")

# TODO: 
# 1. sacar de la pantalla principal los objetos creados
# 2. agragar a la pantalla los calculos realizados


           