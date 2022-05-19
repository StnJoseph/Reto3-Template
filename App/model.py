"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """

import config
from DISClib.ADT import graph as gr
from DISClib.ADT import map as mp
from DISClib.ADT import list as lt
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import dfs as dfs
from DISClib.Algorithms.Graphs import bfs as bfs
from DISClib.Utils import error as error
assert config

# =============================================================
# Construccion de modelos
# =============================================================

def newAnalyzer():
    try:
        analyzer = {
            'station': None,
            'connections': None,
            'vertex': None
        }

        analyzer['station'] = mp.newMap(numelements=1000,
                                     maptype='PROBING',
                                     comparefunction=compareStationIds)

        analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=35755,
                                              comparefunction=compareStationIds)

        analyzer['vertex'] =  lt.newList('SINGLE_LINKED', compareIds)

        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')


# =============================================================
# Funciones para agregar informacion al catalogo
# =============================================================

def addStation(analyzer, service):
    lt.addLast(analyzer['vertex'], service)
    return analyzer

def addStationConnection(analyzer, service):
    try:
        origin, destination = formatVertex(service)
        cleanServiceDuration(service)

        duration = float(service['Trip Duration'])
        addTrip(analyzer, origin)
        addTrip(analyzer, destination)
        addConnection(analyzer, origin, destination, duration)
        #addRouteStation(analyzer, service)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addStopConnection')


def addTrip(analyzer, id):
    """
    Adiciona una estación como un vertice del grafo
    """
    try:
        if not gr.containsVertex(analyzer['connections'], id):
            gr.insertVertex(analyzer['connections'], id)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addstop')

def addConnection(analyzer, origin, destination, distance):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(analyzer['connections'], origin, destination)
    if edge is None:
        gr.addEdge(analyzer['connections'], origin, destination, distance)
    return analyzer

def addRouteStation(analyzer, service):
    """
    Agrega a una estacion, una estacion final
    """
    entry = mp.get(analyzer['station'], service['Start Station Id'])
    if entry is None:
        lstroutes = lt.newList(cmpfunction=compareroutes)
        lt.addLast(lstroutes, service['End Station Id'])
        mp.put(analyzer['station'], service['Start Station Id'], lstroutes)
    else:
        lstroutes = entry['value']
        info = service['End Station Id']
        if lt.isPresent(lstroutes, info) == 0:
            lt.addLast(lstroutes, info)
    return analyzer

def addRouteConnections(analyzer):
    """
    Por cada vertice (cada estacion) se recorre la lista
    de rutas servidas en dicha estación y se crean
    arcos entre ellas para representar el cambio de ruta
    que se puede realizar en una estación.
    """
    lststops = mp.keySet(analyzer['station'])
    for key in lt.iterator(lststops):
        lstroutes = mp.get(analyzer['station'], key)['value']
        prevrout = None
        for route in lt.iterator(lstroutes):
            route = key + '-' + route
            if prevrout is not None:
                addConnection(analyzer, prevrout, route, 0)
                addConnection(analyzer, route, prevrout, 0)
            prevrout = route


def addConnection(analyzer, origin, destination, distance):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(analyzer['connections'], origin, destination)
    if edge is None:
        table = mp.newMap(numelements=3,
                                maptype='PROBING',
                                comparefunction=compareStationIds)

        mp.put(table, "Sumatory", distance)
        mp.put(table, "Cont", 1)
        mp.put(table, "Prom", distance)

        gr.addEdge(analyzer['connections'], origin, destination, table)

    else:
        table = edge['weight']
        sumatory = mp.get(table, "Sumatory")['value'] + int(distance)
        cont = mp.get(table, "Cont")['value'] + 1
        prom = sumatory/cont

        mp.put(table, "Sumatory", sumatory)
        mp.put(table, "Cont", cont)
        mp.put(table, "Prom", prom)
        
    return analyzer



# =============================================================
# Funciones para creacion de datos
# =============================================================



# =============================================================
# Funciones de consulta
# =============================================================

def cleanServiceDuration(service):
    """
    En caso de que el archivo tenga un espacio en la
    distancia, se reemplaza con cero.
    """
    if service['Trip Duration'] == '':
        service['Trip Duration'] = 0


def formatVertex(service):
    """
    Se formatea el nombre del vertice con:
    id de la estación inicial
    """
    nameInit = int(service['Start Station Id'])
    nameFinit = int(float(service['End Station Id']))
    return nameInit, nameFinit

def totalStops(analyzer):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(analyzer['connections'])


def totalConnections(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer['connections'])


# =============================================================
# Funciones de comparacion
# =============================================================

def compareStationIds(station, keyvaluestop):
    """
    Compara dos estaciones
    """
    stationcode = keyvaluestop['key']
    if (station == stationcode):
        return 0
    elif (station > stationcode):
        return 1
    else:
        return -1

def compareroutes(route1, route2):
    """
    Compara dos rutas
    """
    if (route1 == route2):
        return 0
    elif (route1 > route2):
        return 1
    else:
        return -1

def compareIds(Id1, Id2):
    """
    Compara dos Ids
    """
    if (Id1 == Id2):
        return 0
    elif Id1 > Id2:
        return 1
    else:
        return -1


# =============================================================
# Funciones de ordenamiento
# =============================================================

