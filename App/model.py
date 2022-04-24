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
    analyzer = {'players': None, 
                'clubsName': None
                }
    
    analyzer['players'] =  lt.newList('SINGLE_LINKED', comparePlayers)
    analyzer['clubsName'] = mp.newMap(185,
                                   maptype='PROBING',
                                   loadfactor=4,
                                   comparefunction=compareClubsName)

    return analyzer


# ==============================
# Funciones para agregar informacion al catalogo
# ==============================

def addPlayer(analyzer, player):
    lt.addLast(analyzer['players'], player)
    return analyzer

def addClubPlayer(analyzer, player):
    updateClubIndex(analyzer['clubsName'], player)
    return analyzer


def updateClubIndex(map, player):
    entry = mp.get(map, player['club_name'])                    #Obtiene pareja llave valor del HASH para revisar si existe o no#
    if entry is None:           
        datentry = om.newMap(omaptype = 'RBT',                  #Creción del mapa#
                            comparefunction = compareDates)
        
        mp.put(map, player['club_name'], datentry)                            
        playerInfo = lt.newList()                               #Creación de la list#
        lt.addLast(playerInfo, player)                          #Adicion de jugador a la lista#
        om.put(datentry, player['club_joined'], playerInfo)     #Adicion de la lista con los jugadores al arbol#
    else:
        datentry = me.getValue(entry)                           #Sacamos valor ya existente#
        fecha = om.get(datentry, player['club_joined'])         #Obtenemos la fecha#

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

def Init_Finit_Players(analyzer):
    #sizePlayers = playersSize(analyzer)
    list = []
    list_first = []
    list_last = []

    for index in range(1,6):
        initList = []
        firstPlayer = lt.getElement(analyzer['players'], index)

        name = firstPlayer['long_name']
        age = firstPlayer['age']
        height_cm = firstPlayer['height_cm']
        weight_kg = firstPlayer['weight_kg']
        nationality_name = firstPlayer['nationality_name']

        overall = firstPlayer['overall']

        value_eur = firstPlayer['value_eur']
        wage_eur = firstPlayer['wage_eur']
        release_clause_eur = firstPlayer['release_clause_eur']

        league_name = firstPlayer['league_name']
        club_name = firstPlayer['club_name']
        club_joined = firstPlayer['club_joined']

        #club_position = firstPlayer['club_position']
        #player_tags = firstPlayer['player_tags']
        #player_traits = firstPlayer['player_traits']
        #player_url = firstPlayer['player_url']

        initList.append(name)
        initList.append(age)
        initList.append(height_cm)
        initList.append(weight_kg)
        initList.append(nationality_name)

        initList.append(overall)

        initList.append(value_eur)
        initList.append(wage_eur)
        initList.append(release_clause_eur)

        initList.append(league_name)
        initList.append(club_name)
        initList.append(club_joined)

        #initList.append(club_position)
        #initList.append(player_tags)
        #initList.append(player_traits)
        #initList.append(player_url)

        list_first.append(initList)

    for indey in range((int(playersSize(analyzer))-4),(int(playersSize(analyzer)+1))):
        finitList = []
        lastPlayer = lt.getElement(analyzer['players'], indey)

        name = lastPlayer['long_name']
        age = lastPlayer['age']
        height_cm = lastPlayer['height_cm']
        weight_kg = lastPlayer['weight_kg']
        nationality_name = lastPlayer['nationality_name']

        overall = lastPlayer['overall']

        value_eur = lastPlayer['value_eur']
        wage_eur = lastPlayer['wage_eur']
        release_clause_eur = lastPlayer['release_clause_eur']

        league_name = lastPlayer['league_name']
        club_name = lastPlayer['club_name']
        club_joined = lastPlayer['club_joined']

        #club_position = lastPlayer['club_position']
        #player_tags = lastPlayer['player_tags']
        #player_traits = lastPlayer['player_traits']
        #player_url = lastPlayer['player_url']

        finitList.append(name)
        finitList.append(age)
        finitList.append(height_cm)
        finitList.append(weight_kg)
        finitList.append(nationality_name)

        finitList.append(overall)

        finitList.append(value_eur)
        finitList.append(wage_eur)
        finitList.append(release_clause_eur)

        finitList.append(league_name)
        finitList.append(club_name)
        finitList.append(club_joined)

        #finitList.append(club_position)
        #finitList.append(player_tags)
        #finitList.append(player_traits)
        #finitList.append(player_url)

        list_last.append(finitList)

    list.append(list_first)
    list.append(list_last)

    return list

def req1(analyzer, clubName):
    completeInfo = []
    cont = 0

    for i in lt.iterator(keySet(mp.get(analyzer['clubsName'], clubName)['value'])):
        if cont <5:
            arbol = om.get(mp.get(analyzer['clubsName'], clubName)['value'], i)['value']['first']
            info = []
                
            league_name = arbol['info']['league_name']
            league_level = arbol['info']['league_level']

            short_name = arbol['info']['short_name']
            age = arbol['info']['age']
            dob = arbol['info']['dob']
            overall = arbol['info']['overall']
            nationality_name = arbol['info']['nationality_name']
            value_eur = arbol['info']['value_eur']
            wage_eur = arbol['info']['wage_eur']
            release_clause_eur = arbol['info']['release_clause_eur']
            club_joined = arbol['info']['club_joined']
            player_positions = arbol['info']['player_positions']
            club_position = arbol['info']['club_position']
            player_traits = arbol['info']['player_traits']
            player_tags = arbol['info']['player_tags']
                
            info.append(short_name)
            info.append(age)
            info.append(dob)
            info.append(overall)
            info.append(nationality_name)
            info.append(value_eur)
            info.append(wage_eur)
            info.append(release_clause_eur)
            info.append(club_joined)
            info.append(player_positions)
            info.append(club_position)
            info.append(player_traits)
            info.append(player_tags) 
            completeInfo.append(info)
            cont+=1

            if arbol['next'] != None:
                arbol = arbol['next']

                info = []
                
                league_name = arbol['info']['league_name']
                league_level = arbol['info']['league_level']

                short_name = arbol['info']['short_name']
                age = arbol['info']['age']
                dob = arbol['info']['dob']
                overall = arbol['info']['overall']
                nationality_name = arbol['info']['nationality_name']
                value_eur = arbol['info']['value_eur']
                wage_eur = arbol['info']['wage_eur']
                release_clause_eur = arbol['info']['release_clause_eur']
                club_joined = arbol['info']['club_joined']
                player_positions = arbol['info']['player_positions']
                club_position = arbol['info']['club_position']
                player_traits = arbol['info']['player_traits']
                player_tags = arbol['info']['player_tags']
                    
                info.append(short_name)
                info.append(age)
                info.append(dob)
                info.append(overall)
                info.append(nationality_name)
                info.append(value_eur)
                info.append(wage_eur)
                info.append(release_clause_eur)
                info.append(club_joined)
                info.append(player_positions)
                info.append(club_position)
                info.append(player_traits)
                info.append(player_tags) 
                completeInfo.append(info)
                cont+=1
        else:
            break

    return league_name, league_level, completeInfo

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
    return om.size(analyzer)

def keySet(analyzer):
    """
    Lista de llaves
    """
    return om.keySet(analyzer)

def valueSet(analyzer):
    """
    Lista de llaves
    """
    return om.valueSet(analyzer)

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


# ==============================
# Funciones de Comparacion
# ==============================

def compareIds(id1, id2):
    """
    Compara dos crimenes
    """
    if (id1 == id2):
        return 0
    elif id1 < id2:
        return 1
    else:
        return -1


def compareClubsName(club1, entry):
    """
    Compara dos clubes
    """
    identry = me.getKey(entry)
    if (club1 == identry):
        return 0
    elif (club1 < identry):
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

def comparePlayers(player1, player2):
    if (player1 == player2):
        return 0
    elif player1 > player2:
        return 1
    else:
        return -1

# ==============================
# Funciones de ordenamiento
# ==============================

