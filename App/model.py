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
                'clubsName': None,
                'positionPlayer': None,
                'tagsPlayer': None,
                'traitsPlayer': None
                }
    
    analyzer['players'] =  lt.newList('SINGLE_LINKED', comparePlayers)
    analyzer['clubsName'] = mp.newMap(1000,
                                   maptype='PROBING',
                                   loadfactor=4,
                                   comparefunction=compareClubsName)
    analyzer['positionPlayer'] = mp.newMap(1000,
                                   maptype='PROBING',
                                   loadfactor=4,
                                   comparefunction=comparePlayerPosition)
    analyzer['tagsPlayer'] = mp.newMap(1000,
                                   maptype='PROBING',
                                   loadfactor=4,
                                   comparefunction=compareClubsName)
    analyzer['traitsPlayer'] = mp.newMap(1000,
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

def addPositionPlayer(analyzer, player):
    updatePositionPlayer(analyzer['positionPlayer'], player)
    return analyzer

def addTagsPlayer(analyzer, player):
    updateTagsPlayer(analyzer['tagsPlayer'], player)
    return analyzer

def addTraitsPlayer(analyzer, player):
    updateTraitsPlayer(analyzer['traitsPlayer'], player)
    return analyzer

def updateClubIndex(map, player):
    date = datetime.date.fromisoformat(player['club_joined'])
    entry = mp.get(map, player['club_name'])                    #Obtiene pareja llave valor del HASH para revisar si existe o no#
    
    if entry is None:           
        datentry = om.newMap(omaptype = 'RBT',                  #Creción del mapa#
                            comparefunction = compareDates)
        
        mp.put(map, player['club_name'], datentry)                            
        playerInfo = lt.newList()                               #Creación de la list#
        lt.addLast(playerInfo, player)                          #Adicion de jugador a la lista#
        om.put(datentry, date, playerInfo)                         #Adicion de la lista con los jugadores al arbol#
    else:
        datentry = me.getValue(entry)                           #Sacamos valor ya existente#
        fecha = om.contains(datentry, date)                        #Obtenemos la fecha#

        if fecha == False:
            playerInfo = lt.newList()                           #Lista que contiene la info del jugador en el respectivo nodo#
            lt.addLast(playerInfo, player)
            om.put(datentry, date, playerInfo)                     #Creacion de los nodos#
        else:
            playerInfo = me.getValue(om.get(datentry, date))
            lt.addLast(playerInfo, player)                      #Adicion del jugador con la misma fecha de club_joined#

    return map

def updatePositionPlayer(map, player):                          #Tabla de hash con llave posicion y con arbol como value#
    overall = int(player['overall'])                            #Llave para el arbol de OVERALL#
    #potential = int(player['potential'])                        #Llave para el arbol de OVERALL#
    #wage_eur = int(player['wage_eur'])                          #Llave para el arbol de OVERALL#

    entry = mp.get(map, player['player_positions'])             #Obtiene pareja llave valor del HASH para revisar si existe o no#
    if entry is None:           
        datentry = om.newMap(omaptype = 'RBT',                  #Creción del mapa OVERALL#
                            comparefunction = compareOveralls)
        
        mp.put(map, player['player_positions'], datentry)                            
        """playerInfo = om.newMap(omaptype = 'RBT',             #Creción del mapa de POTENTIAL#
                            comparefunction = compareDates)                            
        om.put(playerInfo, player)                              #Player es el POTENTIAL#
        om.put(datentry, p, playerInfo)                         #p ahora es player['overall']#"""
        playerInfo = lt.newList()                               
        lt.addLast(playerInfo, player)                          
        om.put(datentry, overall, playerInfo)

    else:
        datentry = me.getValue(entry)                           #Sacamos valor ya existente#
        position = om.contains(datentry, overall)               #Obtenemos la posicion#

        if position == False:
            playerInfo = lt.newList()                           #Lista que contiene la info del jugador en el respectivo nodo#
            lt.addLast(playerInfo, player)
            om.put(datentry, overall, playerInfo)               #Creacion de los nodos#
        else:
            playerInfo = me.getValue(om.get(datentry, overall))
            lt.addLast(playerInfo, player)                      #Adicion del jugador con la misma fecha de club_joined#

    return map

def updateTagsPlayer(map, player):                          
    wage_eur = int(float(player['wage_eur']))                            
    entry = mp.get(map, player['player_tags'])             
    
    if entry is None:           
        datentry = om.newMap(omaptype = 'RBT',                  
                            comparefunction = compareWages)
        
        mp.put(map, player['player_tags'], datentry)            
        playerInfo = lt.newList()                               
        lt.addLast(playerInfo, player)                          
        om.put(datentry, wage_eur, playerInfo)
    else:
        datentry = me.getValue(entry)                           
        wageKey = om.contains(datentry, wage_eur)               

        if wageKey == False:
            playerInfo = lt.newList()                           
            lt.addLast(playerInfo, player)
            om.put(datentry, wage_eur, playerInfo)               
        else:
            playerInfo = me.getValue(om.get(datentry, wage_eur))
            lt.addLast(playerInfo, player)                      

    return map

def updateTraitsPlayer(map, player):                          
    dob = datetime.date.fromisoformat(player['dob'])
    entry = mp.get(map, player['player_traits'])                    
    
    if entry is None:           
        datentry = om.newMap(omaptype = 'RBT',                  
                            comparefunction = compareDates)
        
        mp.put(map, player['player_traits'], datentry)                            
        playerInfo = lt.newList()                               
        lt.addLast(playerInfo, player)                          
        om.put(datentry, dob, playerInfo)                       
    else:
        datentry = me.getValue(entry)                           
        fecha = om.contains(datentry, dob)                        

        if fecha == False:
            playerInfo = lt.newList()                           
            lt.addLast(playerInfo, player)
            om.put(datentry, dob, playerInfo)                    
        else:
            playerInfo = me.getValue(om.get(datentry, dob))
            lt.addLast(playerInfo, player)                      

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

        club_position = firstPlayer['club_position']
        player_tags = firstPlayer['player_tags']

        if player_tags == "" or player_tags == " ":
            player_tags = "Unknown"

        player_traits = firstPlayer['player_traits']
        player_url = firstPlayer['player_url']

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

        initList.append(club_position)
        initList.append(player_tags)
        initList.append(player_traits)
        initList.append(player_url)

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

        club_position = lastPlayer['club_position']
        player_tags = lastPlayer['player_tags']

        if player_tags == "" or player_tags == " ":
            player_tags = "Unknown"

        player_traits = lastPlayer['player_traits']
        player_url = lastPlayer['player_url']

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

        finitList.append(club_position)
        finitList.append(player_tags)
        finitList.append(player_traits)
        finitList.append(player_url)

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

            if player_tags == "" or player_tags == " ":
                player_tags = "Unknown"
                
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

                if player_tags == "" or player_tags == " ":
                    player_tags = "Unknown"
                    
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

def req3(analyzer, player_tags, wage_eurMin, wage_eurMax):
    mapa = mp.get(analyzer['tagsPlayer'], player_tags)['value']
    rangeKeys = om.keys(mapa, wage_eurMin, wage_eurMax)
    rangeValues = om.values(mapa, wage_eurMin, wage_eurMax)
    completeInfo = []
    contador=0

    for i in lt.iterator(rangeKeys):
        contador+=1

    playersNum = contador

    for j in lt.iterator(rangeValues):
        data = j['first']['info']
        info = []
                
        long_name = data['long_name']
        age = data['age']
        dob = data['dob']
        nationality_name = data['nationality_name']
        value_eur = data['value_eur']
        wage_eur = data['wage_eur']
        club_name = data['club_name']
        league_name = data['league_name']
        potential = data['potential']
        overall = data['overall']
        player_positions = data['player_positions']
        player_traits = data['player_traits']
        player_tags = data['player_tags']

        if player_tags == "" or player_tags == " ":
            player_tags = "Unknown"
                
        info.append(long_name)
        info.append(age)
        info.append(dob)
        info.append(nationality_name)
        info.append(value_eur)
        info.append(wage_eur)
        info.append(club_name)
        info.append(league_name)
        info.append(potential)
        info.append(overall)
        info.append(player_positions)
        info.append(player_traits)
        info.append(player_tags) 
        completeInfo.append(info)

    return playersNum, completeInfo

def req4(analyzer, playerTrait, dobMin, dobMax):
    mapa = mp.get(analyzer['traitsPlayer'], playerTrait)['value']
    rangeKeys = om.keys(mapa, dobMin, dobMax)
    rangeValues = om.values(mapa, dobMin, dobMax)
    completeInfo = []
    contador=0

    for i in lt.iterator(rangeKeys):
        contador+=1

    playersNum = contador

    for j in lt.iterator(rangeValues):
        data = j['first']['info']
        info = []
                
        long_name = data['long_name']
        age = data['age']
        dob = data['dob']
        nationality_name = data['nationality_name']
        value_eur = data['value_eur']
        wage_eur = data['wage_eur']
        club_name = data['club_name']
        league_name = data['league_name']
        potential = data['potential']
        overall = data['overall']
        player_positions = data['player_positions']
        player_traits = data['player_traits']
        player_tags = data['player_tags']
                
        info.append(long_name)
        info.append(age)
        info.append(dob)
        info.append(nationality_name)
        info.append(value_eur)
        info.append(wage_eur)
        info.append(club_name)
        info.append(league_name)
        info.append(potential)
        info.append(overall)
        info.append(player_positions)
        info.append(player_traits)
        info.append(player_tags) 
        completeInfo.append(info)

    return playersNum, completeInfo


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

def comparePlayerPosition(position1, entry):
    """
    Compara dos posiciones
    """
    identry = me.getKey(entry)
    if (position1 == identry):
        return 0
    elif (position1 < identry):
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

def compareOveralls(overall1, overall2):
    """
    Compara dos fechas
    """
    if (overall1 == overall2):
        return 0
    elif (overall1 > overall2):
        return 1
    else:
        return -1

def compareWages(wage1, wage2):
    """
    Compara dos fechas
    """
    if (int(wage1) == int(wage2)):
        return 0
    elif (int(wage1) > int(wage2)):
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

