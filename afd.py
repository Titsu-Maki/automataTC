from graphviz import Digraph

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


def visualizar_afd(afd, nombre_archivo='afd'):
    dot = Digraph(name=nombre_archivo, format='png')
    
    # Nodo invisible para apuntar al estado inicial
    dot.attr('node', shape='none')
    dot.node('')
    
    # Agregar nodos de estados
    for nombre, estado in afd.estados.items():
        forma = 'doublecircle' if estado.es_final else 'circle'
        dot.attr('node', shape=forma)
        dot.node(nombre)

    # Flecha hacia el estado inicial
    dot.edge('', afd.estado_inicial.nombre)

    # Agregar transiciones
    for (origen, simbolo), destino in afd.transiciones.items():
        dot.edge(origen, destino, label=simbolo)

    # Guardar como imagen
    dot.render(filename=nombre_archivo, cleanup=True)
