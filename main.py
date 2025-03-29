from cProfile import label
import streamlit as st
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Trabajo Práctico 02",
    layout="wide"
)

st.title("Generador de Distribuciones Aleatorias")
st.markdown("Genera números aleatorios según diferentes distribuciones y visualiza su histograma.")

with st.sidebar:
    st.header("Parámetros")
    
    distribucion = st.selectbox(
        "Selecciona distribución:",
        ["Uniforme", "Exponencial", "Normal"]
    )
    
    tamano_muestra = st.number_input(
        "Tamaño de muestra:",
        min_value=1,
        max_value=1000000,
        value=10000,
        step=1000,
        help="Número de valores aleatorios a generar (máximo 1.000.000)"
    )
    
    num_intervalos = st.selectbox(
        "Número de intervalos:",
        [10, 15, 20, 30]
    )
    
    if distribucion == "Uniforme":
        st.subheader("Parámetros - Uniforme [a, b]")
        a = st.number_input("Valor mínimo (a):", value=0.0, step=0.1)
        b = st.number_input("Valor máximo (b):", value=1.0, step=0.1)
        if a >= b:
            st.error("El valor mínimo (a) debe ser menor que el valor máximo (b)")
    
    elif distribucion == "Exponencial":
        st.subheader("Parámetros - Exponencial")
        lambda_param = st.number_input("Lambda (λ):", min_value=0.01, value=1.0, step=0.1)
    
    elif distribucion == "Normal":
        st.subheader("Parámetros - Normal")
        mu = st.number_input("Media (μ):", value=0.0, step=0.1)
        sigma = st.number_input("Desviación estándar (σ):", min_value=0.01, value=1.0, step=0.1)
    
    generar_btn = st.button("Generar Distribución", type="primary")

def generar_numeros_aleatorios(distribucion, tamano_muestra, params):
    random.seed(42)

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
            valor = np.log(1 - rnd) / -lambda_param
            numeros.append(round(valor, 4))
    
    elif distribucion == "Normal":
        mu, sigma = params
        i = 0 # Hace referencia a la cantidad de números aleatorios generados

        while i < tamano_muestra:
            # Generamos un numero aleatorio utilizando la formula de Box Muller
            r1 = random.uniform(0, 1)
            r2 = random.uniform(0, 1)
            z1 = np.sqrt(-2 * np.log(r1)) * np.sin(2 * np.pi * r2)
            z2 = np.sqrt(-2 * np.log(r1)) * np.cos(2 * np.pi * r2)
            numeros.append(round(z1 * sigma + mu, 4))
            i += 1

            if i < tamano_muestra:
                numeros.append(round(z2 * sigma + mu, 4))
                i += 1
    
    return numeros

def generar_histograma(muestra, num_intervalos):

    datos_np = np.array(muestra)

    # bins = arreglo de limites superiores de los intervalos
    # freq = arreglo de frecuencias segun los intervalos
    freq, bins = np.histogram(datos_np, bins=num_intervalos)
    
    intervalos = [f"[{round(bins[i], 3)}, {round(bins[i+1], 3)}]" for i in range(len(bins)-1)]
    frecuencia_absoluta = freq
    frecuencia_acumulada = np.cumsum(frecuencia_absoluta)

    tabla = pd.DataFrame({
        'Intervalo': intervalos,
        'Frecuencia Absoluta': frecuencia_absoluta,
        'Frecuencia Acumulada': frecuencia_acumulada
    })

    return freq, bins, tabla

if generar_btn:
    if distribucion == "Uniforme":
        params = (a, b)
    elif distribucion == "Exponencial":
        params = (lambda_param)
    elif distribucion == "Normal":
        params = (mu, sigma)

    numeros = generar_numeros_aleatorios(distribucion, tamano_muestra, params)
    freq, bins, tabla = generar_histograma(numeros, num_intervalos)

    df_numeros = pd.DataFrame({
        'Índice': range(1, tamano_muestra + 1),
        'Valor': numeros
    })

    tab1, tab2 = st.tabs(["Tabla de Frecuencias", "Histograma"])
    # Tabla de frecuencias
    with tab1:
        st.dataframe(tabla)
    # Histograma
    with tab2:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.set_style("whitegrid")
        ax = sns.histplot(numeros, bins=bins, ax=ax, color="steelblue", edgecolor="black", label="Frecuencia")

        ax.set_title(f"Histograma de la Distribución {distribucion} ({tamano_muestra} muestras)")
        ax.set_xlabel("Valor")
        ax.set_ylabel("Frecuencia")
        st.pyplot(fig)

# INSTRUCCIONES
if 'numeros' not in locals():
    st.info("""
    ### Instrucciones:
    1. Selecciona una distribución en el panel lateral
    2. Configura el tamaño de la muestra (hasta 1.000.000)
    3. Selecciona el número de intervalos para el histograma
    4. Ajusta los parámetros específicos de la distribución
    5. Haz clic en "Generar Distribución" para ver los resultados
    """)
    
    # Mostrar información sobre cada distribución y métodos de generación
    with st.expander("Información sobre las Distribuciones y Métodos de Generación"):
        st.markdown("""
        ### Distribución Uniforme [a, b]
        La distribución uniforme genera números aleatorios con igual probabilidad en un intervalo [a, b].
        **Método de generación**: Uso directo de `random.uniform(a, b)` de Python.
        
        ### Distribución Exponencial
        La distribución exponencial modela el tiempo entre eventos en un proceso de Poisson.
        El parámetro lambda (λ) representa la tasa de ocurrencia de los eventos.
        **Método de generación**: Transformación inversa usando `F⁻¹(u) = -ln(u)/λ` donde u es un número aleatorio uniforme.
        
        ### Distribución Normal
        La distribución normal o gaussiana es simétrica alrededor de su media (μ) y
        dispersa según su desviación estándar (σ).
        **Método de generación**: Método de Box-Muller que transforma números aleatorios uniformes en variables aleatorias normales estándar.
        """)