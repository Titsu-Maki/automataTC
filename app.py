import streamlit as st
from afd import construir_afd_desde_palabras, visualizar_afd_con_networkx

st.set_page_config(page_title="AFD Simulador", layout="wide")
st.title("🔤 Simulador de AFD para Palabras Reservadas")

# Palabras que serán reconocidas por el autómata
palabras_reservadas = ['if', 'else', 'while', 'for', 'return', 'int', 'float', 'void']
afd = construir_afd_desde_palabras(palabras_reservadas)

# Entrada del usuario
palabra = st.text_input("Escribe una palabra para verificar si es reservada:")

if palabra:
    if afd.acepta(palabra):
        st.success(f"La palabra **{palabra}** es una palabra reservada.")
    else:
        st.error(f"La palabra **{palabra}** NO es una palabra reservada.")

# Mostrar el autómata visualmente
st.subheader("📘 Representación gráfica del AFD generado")
grafico = visualizar_afd_con_networkx(afd)
st.pyplot(grafico)
