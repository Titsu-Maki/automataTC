class Estado:
    def __init__(self, nombre, es_final=False):
        self.nombre = nombre
        self.es_final = es_final

class AFD:
    def __init__(self):
        self.estados = {}
        self.transiciones = {}
        self.estado_inicial = None

    def agregar_estado(self, nombre, es_final=False):
        estado = Estado(nombre, es_final)
        self.estados[nombre] = estado
        if self.estado_inicial is None:
            self.estado_inicial = estado
        return estado

    def agregar_transicion(self, origen, simbolo, destino):
        self.transiciones[(origen, simbolo)] = destino

    def acepta(self, palabra):
        actual = self.estado_inicial.nombre
        for simbolo in palabra:
            clave = (actual, simbolo)
            if clave in self.transiciones:
                actual = self.transiciones[clave]
            else:
                return False
        return self.estados[actual].es_final

def construir_afd_desde_palabras(palabras):
    afd = AFD()
    contador = 0
    estado_inicial = f"q{contador}"
    afd.agregar_estado(estado_inicial)
    contador += 1

    transiciones_temp = {}  # para evitar estados duplicados
    for palabra in palabras:
        actual = estado_inicial
        for i, simbolo in enumerate(palabra):
            clave = (actual, simbolo)
            if clave in transiciones_temp:
                siguiente = transiciones_temp[clave]
            else:
                siguiente = f"q{contador}"
                es_final = i == len(palabra) - 1
                afd.agregar_estado(siguiente, es_final)
                afd.agregar_transicion(actual, simbolo, siguiente)
                transiciones_temp[clave] = siguiente
                contador += 1
            actual = siguiente
        # Asegurar que el estado final esté marcado
        afd.estados[actual].es_final = True

    return afd

# Visualización con networkx y matplotlib
import networkx as nx
import matplotlib.pyplot as plt

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
