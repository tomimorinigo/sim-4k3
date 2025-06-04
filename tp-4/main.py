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
    limpiar_btn = st.button("Limpiar tabla acumulativa", type="secondary")

def generar_llegada(disciplina):
    if disciplina == "Futbol":
        lambda_param = 1 / media_llegadas_futbol
        params = (lambda_param)
        return utils.generar_numeros_aleatorios("Exponencial", params)
    elif disciplina == "Handball":
        a, b = limite_inf_llegadas_handball, limite_sup_llegadas_handball
        params = (a, b)
        return utils.generar_numeros_aleatorios("Uniforme", params)
    elif disciplina == "Basketball":
        a, b = limite_inf_llegadas_basketball, limite_sup_llegadas_basketball
        params = (a, b)
        return utils.generar_numeros_aleatorios("Uniforme", params)
    

def generar_ocupacion(disciplina):
    if disciplina == "Futbol":
        a, b = limite_inf_ocupacion_futbol, limite_sup_ocupacion_futbol
        params = (a, b)
        return utils.generar_numeros_aleatorios("Uniforme", params)
    elif disciplina == "Handball":
        a, b = limite_inf_ocupacion_handball, limite_sup_ocupacion_handball
        params = (a, b)
        return utils.generar_numeros_aleatorios("Uniforme", params)
    elif disciplina == "Basketball":
        a, b = limite_inf_ocupacion_basketball, limite_sup_ocupacion_basketball
        params = (a, b)
        return utils.generar_numeros_aleatorios("Uniforme", params)

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
    
    # Crear nueva fila
    nueva_fila = utils.generar_nueva_fila(estado_actual, True)
    
    # Agregar fila al DataFrame existente
    nueva_fila_df = pd.DataFrame([nueva_fila])
    st.session_state.tabla_estados = pd.concat(
        [st.session_state.tabla_estados, nueva_fila_df], 
        ignore_index=True
    )

def mostrar_tabla_acumulativa(titulo="Tabla de Estados Acumulativa", container=None):
    """Muestra la tabla acumulativa actual"""
    inicializar_tabla_estado()
    
    ctx = container if container else st
    
    ctx.subheader(titulo)
    
    if not st.session_state.tabla_estados.empty:
        # Mostrar la tabla completa
        ctx.dataframe(
            st.session_state.tabla_estados,
            use_container_width=True,
            hide_index=True
        )
                
        csv = st.session_state.tabla_estados.to_csv(index=False)
        ctx.download_button(
            label="Descargar tabla completa como CSV",
            data=csv,
            file_name="estados_simulacion.csv",
            mime="text/csv"
        )
    else:
        ctx.warning("No hay datos para mostrar")

def limpiar_tabla():
    """Limpia la tabla acumulativa"""
    st.session_state.tabla_estados = pd.DataFrame()
    st.success("Tabla limpia")


if limpiar_btn:
    limpiar_tabla()

if generar_btn:

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
    dia = 1
    tiempo_ocupacion_acum = 0
    objetos_temporales = []
    contador_objetos = 0 

    disciplinas = ["Futbol", "Handball", "Basketball"]

    # Generar llegadas iniciales
    for d in disciplinas:
        llegada, rnd = generar_llegada(d)
        eventos.append({
            "evento": f"Llegada Grupo de {d}",
            "disciplina": d,
            "RND": rnd,
            "tiempo_entre_llegada": round(llegada * 60, 2),
            "proximo_evento": round(llegada * 60, 2),
        })
        
    # Simulacion
    for iteracion in range(max_iteraciones):
        if reloj >= tiempo:
            break

        # Actualizamos nuestro numero de dia
        dia = (reloj // 1440) + 1  # 1440 minutos en un dia

        eventos.sort(key=lambda x: x["proximo_evento"])
        evento_actual = eventos.pop(0)
        reloj = evento_actual["proximo_evento"]

        disciplina = evento_actual.get("disciplina", "")
        evento = evento_actual["evento"]

        if evento == f"Llegada Grupo de {disciplina}":
            # Agregamos el evento de llegada del siguiente grupo
            tiempo_llegada, rnd = generar_llegada(disciplina)
            eventos.append({
                "evento": f"Llegada Grupo de {disciplina}",
                "disciplina": disciplina,
                "RND": rnd,
                "tiempo_entre_llegada": round(tiempo_llegada * 60, 2),
                "proximo_evento": reloj + round(tiempo_llegada * 60, 2),
            })

            if contador_colas >= 6:
                # Si hay mas de 6 grupos esperando, no se permite la llegada de nuevos grupos
                continue

            contador_objetos += 1
            # Creamos un objeto temporal para el grupo
            objeto_temporal = {
                "id": contador_objetos,
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
                tiempo_ocupacion, rnd = generar_ocupacion(disciplina)

                # Agregamos el evento de fin de ocupacion
                eventos.append({
                    "evento": f"Fin Ocupacion",
                    "RND": rnd,
                    "disciplina": disciplina,
                    "tiempo_ocupacion": round(tiempo_ocupacion, 2),
                    "proximo_evento": reloj + round(tiempo_ocupacion, 2),
                })

                contadores[disciplina] += 1

            else:
                colas[disciplina] += 1
                contador_colas += 1
                objeto_temporal["estado"] = "Esperando"
            
            objetos_temporales.append(objeto_temporal)

        elif evento == "Fin Ocupacion":
            # Se libera la cancha
            estado_cancha = "Limpieza"
            grupo_ocupando = None

            # Sumamos el tiempo de ocupacion a nuestro acumulador
            tiempo_ocupacion_acum += evento_actual["tiempo_ocupacion"]
           
            # Remover grupo que terminó
            objetos_temporales = [obj for obj in objetos_temporales if obj["estado"] != "En Juego"]
            
            eventos.append({
                "evento": "Fin Limpieza",
                "proximo_evento": reloj + limpieza_duracion,
            })

        elif evento == "Fin Limpieza":
            # Se termina de limpiar la cancha
            # Verificamos las colas
            if contador_colas > 0:
                objetos_temporales.sort(key=lambda x: x["tiempo_llegada"])
                siguiente_grupo = None

                basketball_grupos = [obj for obj in objetos_temporales if obj["disciplina"] == "Basketball" and obj["estado"] == "Esperando"]
                otros_grupos = [obj for obj in objetos_temporales if obj["disciplina"] in ["Futbol", "Handball"] and obj["estado"] == "Esperando"]
                
                if otros_grupos:
                    siguiente_grupo = otros_grupos[0]
                elif basketball_grupos:
                    siguiente_grupo = basketball_grupos[0]
                
                if siguiente_grupo:
                    estado_cancha = "Ocupada"
                    contador_colas -= 1
                    colas[siguiente_grupo["disciplina"]] -= 1

                    siguiente_grupo["estado"] = "En Juego"
                    grupo_ocupando = siguiente_grupo["disciplina"]

                    # Acumulo los tiempos de espera segun la disciplina.
                    tiempo_espera = reloj - siguiente_grupo["tiempo_llegada"]
                    esperas_acum[siguiente_grupo["disciplina"]] += tiempo_espera
                    contadores[siguiente_grupo["disciplina"]] += 1
                    
                    # Generamos el tiempo de ocupacion
                    tiempo_ocupacion, rnd = generar_ocupacion(siguiente_grupo["disciplina"])
                    eventos.append({
                        "evento": f"Fin Ocupacion",
                        "RND": rnd,
                        "disciplina": siguiente_grupo["disciplina"],
                        "tiempo_ocupacion": round(tiempo_ocupacion, 2),
                        "proximo_evento": reloj + round(tiempo_ocupacion, 2),
                    })
            else:
                estado_cancha = "Disponible"

        proxima_llegada_futbol = next((evento for evento in eventos if evento["evento"] == "Llegada Grupo de Futbol" and evento["disciplina"] == "Futbol"), None)
        proxima_llegada_basketball = next((evento for evento in eventos if evento["evento"] == "Llegada Grupo de Basketball" and evento["disciplina"] == "Basketball"), None)
        proxima_llegada_handball = next((evento for evento in eventos if evento["evento"] == "Llegada Grupo de Handball" and evento["disciplina"] == "Handball"), None)
        
        evento_fin_ocupacion = next((evento for evento in eventos if evento["evento"] == "Fin Ocupacion"), None)
        print(f"Evento fin ocupacion: {evento_fin_ocupacion}")
        fin_limpieza = next((evento["proximo_evento"] for evento in eventos if evento["evento"] == "Fin Limpieza"), None)

        # Crear vector de estado
        estado_dict = {
            "nro_evento": iteracion + 1,
            "evento": evento,
            "reloj": reloj,
            "rnd_proxima_llegada_futbol": proxima_llegada_futbol["RND"] if proxima_llegada_futbol else None,
            "tiempo_entre_llegada_futbol": proxima_llegada_futbol["tiempo_entre_llegada"] if proxima_llegada_futbol else None,
            "proxima_llegada_futbol": proxima_llegada_futbol["proximo_evento"] if proxima_llegada_futbol else None,
            "rnd_proxima_llegada_handball": proxima_llegada_handball["RND"] if proxima_llegada_handball else None,
            "tiempo_entre_llegada_handball": proxima_llegada_handball["tiempo_entre_llegada"] if proxima_llegada_handball else None,
            "proxima_llegada_handball": proxima_llegada_handball["proximo_evento"] if proxima_llegada_handball else None,
            "rnd_proxima_llegada_basketball": proxima_llegada_basketball["RND"] if proxima_llegada_basketball else None,
            "tiempo_entre_llegada_basketball": proxima_llegada_basketball["tiempo_entre_llegada"] if proxima_llegada_basketball else None,
            "proxima_llegada_basketball": proxima_llegada_basketball["proximo_evento"] if proxima_llegada_basketball else None,
            "rnd_fin_ocupacion": evento_fin_ocupacion["RND"] if evento_fin_ocupacion else None,
            "fin_ocupacion": evento_fin_ocupacion["proximo_evento"] if evento_fin_ocupacion else None,
            "fin_limpieza": fin_limpieza,
            "estado_cancha": estado_cancha,
            "grupo_ocupando": grupo_ocupando,
            "cola_futbol": colas["Futbol"],
            "cola_handball": colas["Handball"],
            "cola_basketball": colas["Basketball"],
            "contador_colas": contador_colas,
            "espera_acum_futbol": esperas_acum["Futbol"],
            "contador_futbol": contadores["Futbol"],
            "espera_acum_handball": esperas_acum["Handball"],
            "contador_handball": contadores["Handball"],
            "espera_acum_basketball": esperas_acum["Basketball"],
            "contador_basketball": contadores["Basketball"],
            "dia": dia,
            "tiempo_ocupacion": tiempo_ocupacion_acum,
            "objetos_temporales": objetos_temporales.copy()
        }
        
        # Actualizar vector de estado (mantener solo el último)
        vector_estado = [estado_dict]
        
        # Agregar a tabla si corresponde mostrar
        if reloj >= min_inicio_mostrar and cant_iteraciones_mostrar > 0:
            cant_iteraciones_mostrar -= 1
            agregar_fila_tabla(vector_estado)

    mostrar_tabla_acumulativa()

    # Mostrar la última fila del vector de estado
    st.subheader("Último Estado de la Simulación")
    if vector_estado:
        ultimo_estado_df = pd.DataFrame([vector_estado[-1]])
        fila = utils.generar_nueva_fila(ultimo_estado_df)
        st.dataframe(
            fila,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Aún no se ha generado ninguna simulación.")

    # Calcular y mostrar estadísticas finales
    st.subheader("Estadísticas Finales")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Promedio Espera Fútbol", 
                 f"{esperas_acum['Futbol']/contadores['Futbol']:.2f} min" if contadores['Futbol'] > 0 else "0 min")
    
    with col2:
        st.metric("Promedio Espera Handball", 
                 f"{esperas_acum['Handball']/contadores['Handball']:.2f} min" if contadores['Handball'] > 0 else "0 min")
    
    with col3:
        st.metric("Promedio Espera Basketball", 
                 f"{esperas_acum['Basketball']/contadores['Basketball']:.2f} min" if contadores['Basketball'] > 0 else "0 min")
    
    st.metric("Promedio de Ocupación por Día", 
             f"{tiempo_ocupacion_acum/dia:.2f} min/día" if dia > 0 else f"{tiempo_ocupacion_acum:.2f} min")

           