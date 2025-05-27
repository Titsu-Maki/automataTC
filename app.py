import streamlit as st
from afd import construir_afd_desde_palabras, visualizar_afd_con_networkx

st.title("Simulador de AFD para Palabras Reservadas")

palabras_reservadas = ['if', 'else', 'while', 'for', 'return', 'int', 'float', 'void']
afd = construir_afd_desde_palabras(palabras_reservadas)

# Entrada de palabra
palabra = st.text_input("Escribe una palabra para verificar:")

if palabra:
    if afd.acepta(palabra):
        st.success(f"La palabra **{palabra}** es una palabra reservada.")
    else:
        st.error(f"La palabra **{palabra}** NO es una palabra reservada.")

# Mostrar imagen del AFD generada en memoria
st.subheader("Representación del AFD")
grafico = visualizar_afd_con_networkx(afd)
st.pyplot(grafico)

