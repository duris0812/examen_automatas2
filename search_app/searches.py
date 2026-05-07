from .arbol import Nodo


def buscar_solucion_BFS(conexiones, estado_inicial, solucion):
    """Búsqueda en Amplitud (BFS)"""
    solucionado = False
    nodos_visitados = []
    nodos_frontera = []
    nodoInicial = Nodo(estado_inicial)
    nodos_frontera.append(nodoInicial)

    while (not solucionado) and len(nodos_frontera) != 0:
        nodo = nodos_frontera[0]
        
        # Extraer nodo y añadirlo a visitados
        nodos_visitados.append(nodos_frontera.pop(0))
        
        if nodo.get_datos() == solucion:
            solucionado = True
            return nodo
        else:
            # Expandir nodos hijo
            dato_nodo = nodo.get_datos()
            lista_hijos = []
            
            if dato_nodo in conexiones:
                for un_hijo in conexiones[dato_nodo]:
                    hijo = Nodo(un_hijo)
                    hijo.set_padre(nodo)
                    lista_hijos.append(hijo)
                    
                    if not hijo.en_lista(nodos_visitados) and not hijo.en_lista(nodos_frontera):
                        nodos_frontera.append(hijo)
                        nodo.set_hijos(lista_hijos)


def buscar_solucion_DFS(conexiones, estado_inicial, solucion):
    """Búsqueda en Profundidad (DFS) para grafos de ciudades"""
    solucionado = False
    nodos_visitados = []
    nodos_frontera = []

    nodoInicial = Nodo(estado_inicial)
    nodos_frontera.append(nodoInicial)

    while (not solucionado) and len(nodos_frontera) != 0:
        nodo = nodos_frontera.pop()
        nodos_visitados.append(nodo)

        if nodo.get_datos() == solucion:
            solucionado = True
            return nodo
        else:
            dato_nodo = nodo.get_datos()

            hijos = []
            if dato_nodo in conexiones:
                for ciudad_hija in reversed(list(conexiones[dato_nodo])):
                    hijo = Nodo(ciudad_hija)
                    hijo.set_padre(nodo)
                    if not hijo.en_lista(nodos_visitados) and not hijo.en_lista(nodos_frontera):
                        nodos_frontera.append(hijo)
                    hijos.append(hijo)
            
            nodo.set_hijos(hijos)


def buscar_solucion_UCS(conexiones, estado_inicial, solucion):
    """Búsqueda con Costo Uniforme (UCS)"""
    
    nodos_visitados = []
    nodos_frontera = []

    nodo_inicial = Nodo(estado_inicial)
    nodo_inicial.set_costo(0)

    nodos_frontera.append(nodo_inicial)

    while len(nodos_frontera) != 0:

        nodos_frontera = sorted(
            nodos_frontera,
            key=lambda x: x.get_costo()
        )

        nodo = nodos_frontera.pop(0)
        nodos_visitados.append(nodo)

        if nodo.get_datos() == solucion:
            return nodo

        dato_nodo = nodo.get_datos()

        if dato_nodo in conexiones:
            for ciudad_hija in conexiones[dato_nodo]:

                hijo = Nodo(ciudad_hija)
                hijo.set_padre(nodo)

                costo = conexiones[dato_nodo][ciudad_hija]
                hijo.set_costo(nodo.get_costo() + costo)

                if not hijo.en_lista(nodos_visitados):

                    if hijo.en_lista(nodos_frontera):

                        for n in nodos_frontera:
                            if n.igual(hijo):
                                if hijo.get_costo() < n.get_costo():
                                    nodos_frontera.remove(n)
                                    nodos_frontera.append(hijo)
                    else:
                        nodos_frontera.append(hijo)


def obtener_ruta(nodo_solucion, estado_inicial):
    """Obtiene la ruta completa desde el estado inicial hasta la solución"""
    resultado = []
    nodo = nodo_solucion

    while nodo.get_padre() != None:
        resultado.append(nodo.get_datos())
        nodo = nodo.get_padre()

    resultado.append(estado_inicial)
    resultado.reverse()

    return resultado
