import streamlit as st
from pyvis.network import Network
import tempfile
import os

# Clase del autómata para palabras reservadas
class AutomataReservadas:
    def __init__(self, palabras):
        self.palabras = palabras
        self.trie = self._crear_trie(palabras)

    def _crear_trie(self, palabras):
        trie = {}
        for palabra in palabras:
            nodo = trie
            for letra in palabra:
                if letra not in nodo:
                    nodo[letra] = {}
                nodo = nodo[letra]
            nodo['#'] = True
        return trie

    def es_reservada(self, palabra):
        nodo = self.trie
        for letra in palabra:
            if letra in nodo:
                nodo = nodo[letra]
            else:
                return False
        return '#' in nodo

    def obtener_transiciones(self):
        estados = set()
        transiciones = []
        contador = 1
        mapa_estados = {id(self.trie): 'q0'}

        def recorrer(nodo, estado_actual):
            nonlocal contador
            for letra, subnodo in nodo.items():
                if letra == '#':
                    continue
                if id(subnodo) not in mapa_estados:
                    nuevo_estado = f"q{contador}"
                    mapa_estados[id(subnodo)] = nuevo_estado
                    contador += 1
                else:
                    nuevo_estado = mapa_estados[id(subnodo)]

                transiciones.append((estado_actual, letra, nuevo_estado))
                estados.add(nuevo_estado)
                recorrer(subnodo, nuevo_estado)

        recorrer(self.trie, 'q0')
        estados.add('q0')
        return list(estados), transiciones

    def obtener_estado_final(self, palabra):
        nodo = self.trie
        camino = ['q0']
        mapa_estados = {id(self.trie): 'q0'}
        contador = 1

        for letra in palabra:
            if letra in nodo:
                nodo = nodo[letra]
                if id(nodo) not in mapa_estados:
                    mapa_estados[id(nodo)] = f"q{contador}"
                    contador += 1
                camino.append(mapa_estados[id(nodo)])
            else:
                return None  # No es válida

        return camino[-1] if '#' in nodo else None

# Interfaz Streamlit
st.set_page_config(page_title="Autómata de Palabras Reservadas", layout="centered")
st.title("Autómata Finito para Palabras Reservadas")

# Definir palabras reservadas
palabras_reservadas = ["if", "else", "for", "while", "return", "switch"]
automata = AutomataReservadas(palabras_reservadas)

entrada = st.text_input("🔤 Ingresa una palabra:")

if entrada:
    if automata.es_reservada(entrada):
        st.success(f"'{entrada}' es una palabra reservada.")
    else:
        st.error(f"'{entrada}' no es una palabra reservada.")

    # Visualización con PyVis
    estados, transiciones = automata.obtener_transiciones()
    estado_final = automata.obtener_estado_final(entrada)

    net = Network(height='400px', directed=True)

    for estado in estados:
        if estado == 'q0':
            color = 'skyblue'
        elif estado == estado_final and estado_final is not None:
            color = 'red'  # Estado final alcanzado por la palabra
        else:
            color = 'lightgreen'
        net.add_node(estado, label=estado, color=color)

    for origen, letra, destino in transiciones:
        net.add_edge(origen, destino, label=letra)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
        net.save_graph(tmp_file.name)
        tmp_path = tmp_file.name

    with open(tmp_path, 'r', encoding='utf-8') as HtmlFile:
        source_code = HtmlFile.read()
        components = st.components.v1
        components.html(source_code, height=450)

    os.unlink(tmp_path)

st.markdown("---")
