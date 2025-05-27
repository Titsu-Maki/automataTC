import streamlit as st
from afd import construir_afd_desde_palabras, visualizar_afd
from PIL import Image
import os

# Palabras reservadas
palabras_reservadas = ['if', 'else', 'while', 'for', 'return', 'int', 'float', 'void']

# Construir el AFD
afd = construir_afd_desde_palabras(palabras_reservadas)

# Visualizar AFD (se guarda como afd.png)
visualizar_afd(afd, 'afd')

# Interfaz Streamlit
st.title("Simulador de AFD para Palabras Reservadas")
st.markdown("Este simulador usa un Autómata Finito Determinista real para validar si una palabra es reservada.")

# Entrada de palabra
palabra = st.text_input("Escribe una palabra para verificar:")

if palabra:
    if afd.acepta(palabra):
        st.success(f"La palabra **{palabra}** es una palabra reservada.")
    else:
        st.error(f"La palabra **{palabra}** NO es una palabra reservada.")

# Mostrar la imagen del AFD
st.subheader("Representación del AFD")
if os.path.exists("afd.png"):
    image = Image.open("afd.png")
    st.image(image, caption="AFD generado desde las palabras reservadas", use_column_width=True)
else:
    st.warning("No se encontró la imagen del AFD.")
