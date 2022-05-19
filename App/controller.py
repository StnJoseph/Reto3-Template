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
 """

import config as cf
from App import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


# ==============================
#  Inicializacion del catalogo
# ==============================

def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # catalog es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer


# ==============================
#  Funciones para la carga de datos y almacenamiento de datos en los modelos
# ==============================


def loadServices(analyzer, servicesfile):
    """
    Carga los datos de los archivos CSV en el modelo.
    Se crea un arco entre cada par de estaciones que
    pertenecen al mismo servicio y van en el mismo sentido.

    addRouteConnection crea conexiones entre diferentes rutas
    servidas en una misma estación.
    """
    servicesfile = cf.data_dir + servicesfile
    input_file = csv.DictReader(open(servicesfile, encoding="utf-8"), delimiter=",")
    lastservice = None
    
    for service in input_file:
        model.addStation(analyzer, service)
        if lastservice is not None:
            sameEndStation = lastservice['End Station Id'] == service['End Station Id']
            sameStation = lastservice['Start Station Id'] == service['Start Station Id']
            if sameEndStation and not sameStation:
                model.addStationConnection(analyzer, service)
        lastservice = service
    model.addRouteConnections(analyzer)
    return analyzer
    # TODO joseph


# ==============================
#  Funciones para consultas
# ==============================

def totalStops(analyzer):
    """
    Total de paradas de autobus
    """
    return model.totalStops(analyzer)


def totalConnections(analyzer):
    """
    Total de enlaces entre las paradas
    """
    return model.totalConnections(analyzer)


def connectedComponents(analyzer):
    """
    Numero de componentes fuertemente conectados
    """
    return model.connectedComponents(analyzer)


def minimumCostPaths(analyzer, initialStation):
    """
    Calcula todos los caminos de costo minimo de initialStation a todas
    las otras estaciones del sistema
    """
    return model.minimumCostPaths(analyzer, initialStation)


def hasPath(analyzer, destStation):
    """
    Informa si existe un camino entre initialStation y destStation
    """
    return model.hasPath(analyzer, destStation)


def minimumCostPath(analyzer, destStation):
    """
    Retorna el camino de costo minimo desde initialStation a destStation
    """
    return model.minimumCostPath(analyzer, destStation)


def searchPaths(analyzer, initialStation, searchMethod):
    """
    Calcula todos los recorridos por "dfs" o "bfs" de initialStation a
    todas las otras estaciones del sistemas
    """
    return model.searchPaths(analyzer, initialStation, searchMethod)


def hasSearchPath(analyzer, destStation, searchMethod):
    """
    Informa si existe un camino entre initialStation y destStation segun
    el metodo de busqueda ("bfs" o "dfs")
    """
    return model.hasSearchPath(analyzer, destStation, searchMethod)


def searchPathTo(analyzer, destStation, searchMethod):
    """
    Retorna el camino de busqueda entre initialStation y destStation
    """
    return model.searchPathTo(analyzer, destStation, searchMethod)

def servedRoutes(analyzer):
    """
    Retorna el camino de costo minimo desde initialStation a destStation
    """
    maxvert, maxdeg = model.servedRoutes(analyzer)
    return maxvert, maxdeg


# ==============================
# Funciones de ordenamiento
# ==============================