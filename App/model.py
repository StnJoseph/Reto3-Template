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


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
import datetime
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""


# ==============================
# Construccion de modelos
# ==============================

def newAnalyzer():
    """ Inicializa el analizador

    Crea una lista vacia para guardar todos los crimenes
    Se crean indices (Maps) por los siguientes criterios:
    -Clubs

    Retorna el analizador inicializado.
    """
    analyzer = {'clubsName': None
                }

    analyzer['clubsName'] = mp.newMap(10000,
                                   maptype='CHAINING',
                                   loadfactor=4,
                                   comparefunction=compareClubsName)

    return analyzer


# ==============================
# Funciones para agregar informacion al catalogo
# ==============================

def addPlayer(analyzer, player):
    """
    """
    updateClubIndex(analyzer['clubsName'], player)
    return analyzer


def updateClubIndex(map, player):
    """
    Se toma la fecha del crimen y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de crimenes
    y se actualiza el indice de tipos de crimenes.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de crimenes
    """
    entry = mp.get(map, player['club_name'])                #Obtiene pareja llave valor del HASH para revisar si existe o no#
    if entry is None:           
        datentry = om.newMap(omaptype = 'RBT',              #Creción del mapa#
                            comparefunction = compareDates)
        playerInfo = lt.newList()                           #Creación de la list#
        lt.addLast(playerInfo, player)                      #Adicion de jugador a la lista#
        om.put(datentry, player['club_joined'], playerInfo) #Adicion de la lista con los jugadores al arbol#
    else:
        datentry = me.getValue(entry)                       #Sacamos valor ya existente#
        fecha = om.get(datentry, player['club_joined'])     #Obtenemos la fecha#

        if fecha is None:
            playerInfo = lt.newList()                           #Lista que contiene la info del jugador en el respectivo nodo#
            lt.addLast(playerInfo, player)
            om.put(datentry, player['club_joined'], playerInfo) #Creacion de los nodos#
        else:
            playerInfo = me.getValue(om.get(datentry, player['club_joined']))
            lt.addLast(playerInfo, player)                      #Adicion del jugador con la misma fecha de club_joined#

    return map

# ==============================
# Funciones para creacion de datos
# ==============================


# ==============================
# Funciones de consulta
# ==============================

def playersSize(analyzer):
    """
    Número de jugadores
    """
    return lt.size(analyzer['players'])


def indexHeight(analyzer):
    """
    Altura del arbol
    """
    return om.height(analyzer['clubsName'])


def indexSize(analyzer):
    """
    Numero de elementos en el indice
    """
    return om.size(analyzer['clubsName'])


def minKey(analyzer):
    """
    Llave mas pequena
    """
    return om.minKey(analyzer['clubsName'])


def maxKey(analyzer):
    """
    Llave mas grande
    """
    return om.maxKey(analyzer['clubsName'])


def getCrimesByRange(analyzer, initialDate, finalDate):
    """
    Retorna el numero de crimenes en un rago de fechas.
    """
    lst = om.values(analyzer['dateIndex'], initialDate, finalDate)
    totcrimes = 0
    for lstdate in lt.iterator(lst):
        totcrimes += lt.size(lstdate['lstcrimes'])
    return totcrimes


def getCrimesByRangeCode(analyzer, initialDate, offensecode):
    """
    Para una fecha determinada, retorna el numero de crimenes
    de un tipo especifico.
    """
    crimedate = om.get(analyzer['dateIndex'], initialDate)
    if crimedate['key'] is not None:
        offensemap = me.getValue(crimedate)['offenseIndex']
        numoffenses = mp.get(offensemap, offensecode)
        if numoffenses is not None:
            return mp.size(me.getValue(numoffenses)['lstoffenses'])
    return 0


# ==============================
# Funciones de Comparacion
# ==============================

def compareIds(id1, id2):
    """
    Compara dos crimenes
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1


def compareClubsName(club1, entry):
    """
    Compara dos clubes
    """
    identry = me.getKey(entry)
    if (int(club1) == int(identry)):
        return 0
    elif (int(club1) > int(identry)):
        return 1
    else:
        return -1


def compareOffenses(offense1, offense2):
    """
    Compara dos tipos de crimenes
    """
    offense = me.getKey(offense2)
    if (offense1 == offense):
        return 0
    elif (offense1 > offense):
        return 1
    else:
        return -1

def compareDates(date1, date2):
    """
    Compara dos fechas
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1

# ==============================
# Funciones de ordenamiento
# ==============================
