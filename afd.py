from graphviz import Digraph
from PIL import Image
import io
import networkx as nx
import matplotlib.pyplot as plt

class Estado:
    def __init__(self, nombre, es_final=False):
        self.nombre = nombre
        self.es_final = es_final

class Transicion:
    def __init__(self, origen, simbolo, destino):
        self.origen = origen
        self.simbolo = simbolo
        self.destino = destino

class AFD:
    def __init__(self):
        self.estados = {}
        self.transiciones = {}
        self.estado_inicial = None

    def agregar_estado(self, nombre, es_final=False):
        estado = Estado(nombre, es_final)
        self.estados[nombre] = estado
        return estado

    def definir_estado_inicial(self, nombre):
        self.estado_inicial = self.estados[nombre]

    def agregar_transicion(self, origen, simbolo, destino):
        self.transiciones[(origen, simbolo)] = destino

    def acepta(self, palabra):
        estado_actual = self.estado_inicial.nombre
        for simbolo in palabra:
            clave = (estado_actual, simbolo)
            if clave in self.transiciones:
                estado_actual = self.transiciones[clave]
            else:
                return False
        return self.estados[estado_actual].es_final

def construir_afd_desde_palabras(palabras):
    afd = AFD()
    contador = 1

    # Crear estado inicial
    afd.agregar_estado('q0')
    afd.definir_estado_inicial('q0')

    for palabra in palabras:
        estado_actual = 'q0'
        for letra in palabra:
            clave = (estado_actual, letra)
            if clave not in afd.transiciones:
                nuevo_estado = f'q{contador}'
                afd.agregar_estado(nuevo_estado)
                afd.agregar_transicion(estado_actual, letra, nuevo_estado)
                estado_actual = nuevo_estado
                contador += 1
            else:
                estado_actual = afd.transiciones[clave]
        afd.estados[estado_actual].es_final = True

    return afd


def visualizar_afd(afd):
    dot = Digraph(name="AFD", format='png')

    dot.attr('node', shape='none')
    dot.node('')

    for nombre, estado in afd.estados.items():
        forma = 'doublecircle' if estado.es_final else 'circle'
        dot.attr('node', shape=forma)
        dot.node(nombre)

    dot.edge('', afd.estado_inicial.nombre)

    for (origen, simbolo), destino in afd.transiciones.items():
        dot.edge(origen, destino, label=simbolo)

    # Generar imagen en memoria
    img_bytes = dot.pipe(format='png')
    return Image.open(io.BytesIO(img_bytes))

def visualizar_afd_con_networkx(afd):
    G = nx.MultiDiGraph()

    for nombre, estado in afd.estados.items():
        G.add_node(nombre, shape='doublecircle' if estado.es_final else 'circle')

    for (origen, simbolo), destino in afd.transiciones.items():
        G.add_edge(origen, destino, label=simbolo)

    pos = nx.spring_layout(G)
    plt.figure(figsize=(8, 6))

    node_shapes = {'circle': [], 'doublecircle': []}
    for node, attr in G.nodes(data=True):
        shape = attr.get('shape', 'circle')
        node_shapes[shape].append(node)

    for shape, nodes in node_shapes.items():
        nx.draw_networkx_nodes(G, pos, nodelist=nodes, node_shape='o', node_size=1500, node_color='lightblue')

    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
    nx.draw_networkx_edges(G, pos, arrows=True)

    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.axis('off')
    return plt
