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


from genericpath import exists
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
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
    analyzer['clubsName'] = mp.newMap(184,
                                   maptype='PROBING',
                                   loadfactor=4,
                                   comparefunction=compareClubsName)
    analyzer['overallPlayer'] = mp.newMap(184,
                                   maptype='PROBING',
                                   loadfactor=4,
                                   comparefunction=comparePlayerPosition)
    analyzer['tagsPlayer'] = mp.newMap(184,
                                   maptype='PROBING',
                                   loadfactor=4,
                                   comparefunction=compareClubsName)
    analyzer['traitsPlayer'] = mp.newMap(184,
                                   maptype='PROBING',
                                   loadfactor=4,
                                   comparefunction=compareClubsName)
    analyzer['overall'] = om.newMap(omaptype = 'RBT',                  
                                    comparefunction = compareIntValues)
    analyzer['potential'] = om.newMap(omaptype = 'RBT',                  
                                    comparefunction = compareIntValues)
    analyzer['value_eur'] = om.newMap(omaptype = 'RBT',                  
                                    comparefunction = compareIntValues)
    analyzer['wage_eur'] = om.newMap(omaptype = 'RBT',                  
                                    comparefunction = compareIntValues)
    analyzer['age'] = om.newMap(omaptype = 'RBT',                  
                                    comparefunction = compareIntValues)
    analyzer['height_cm'] = om.newMap(omaptype = 'RBT',                  
                                    comparefunction = compareIntValues)
    analyzer['weight_kg'] = om.newMap(omaptype = 'RBT',                  
                                    comparefunction = compareIntValues)
    analyzer['release_clause_eur'] = om.newMap(omaptype = 'RBT',                  
                                    comparefunction = compareIntValues)
    return analyzer


# ==============================
# Funciones para agregar informacion al catalogo
# ==============================

def addPlayer(analyzer, player):                                #_Init_#
    lt.addLast(analyzer['players'], player)
    return analyzer

def addClubPlayer(analyzer, player):                            #Req1#
    updateClubIndex(analyzer['clubsName'], player)
    return analyzer

def addPositionPlayer(analyzer, player):                        #Req2#
    updateOverallPlayer(analyzer['overallPlayer'], player)
    return analyzer

def addTagsPlayer(analyzer, player):                            #Req3#
    updateTagsPlayer(analyzer['tagsPlayer'], player)
    return analyzer

def addTraitsPlayer(analyzer, player):                          #Req4#
    updateTraitsPlayer(analyzer['traitsPlayer'], player)
    return analyzer

def addHistogramOverall(analyzer, player):                      #Req5#
    updateOverall(analyzer['overall'], player)
    return analyzer

def addHistogramPotential(analyzer, player):                    #Req5#
    updatePotential(analyzer['potential'], player)
    return analyzer

def addHistogramValue(analyzer, player):                        #Req5#
    updateValue(analyzer['value_eur'], player)
    return analyzer

def addHistogramWage(analyzer, player):                         #Req5#
    updateWage(analyzer['wage_eur'], player)
    return analyzer

def addHistogramAge(analyzer, player):                          #Req5#
    updateAge(analyzer['age'], player)
    return analyzer

def addHistogramHeight(analyzer, player):                       #Req5#
    updateHeight(analyzer['height_cm'], player)
    return analyzer

def addHistogramWeight(analyzer, player):                       #Req5#
    updateWeight(analyzer['weight_kg'], player)
    return analyzer

def addHistogramRelease(analyzer, player):                      #Req5#
    updateRelease(analyzer['release_clause_eur'], player)
    return analyzer



def updateClubIndex(map, player):                               #Req1#
    date = datetime.date.fromisoformat(player['club_joined'])
    
    if player['club_name'] != "":
        club_name = player['club_name'].replace(" ", "").split(sep=',')
        
        for llave in club_name:
            entry = mp.get(map, llave) 

            if entry is None:           
                datentry = om.newMap(omaptype = 'RBT',                  #Creción del mapa#
                                    comparefunction = compareDates)
                
                mp.put(map, llave, datentry)                            
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

def updateOverallPlayer(map, player):                           #Req2#
    overall = int(player['overall'])        
    if player['player_positions'] != "":
        player_positions = player['player_positions'].replace(" ", "").split(sep=',')
        
        for llave in player_positions:
            entry = mp.get(map, llave) 

            if entry is None:           
                datentry = om.newMap(omaptype = 'RBT',                  
                                    comparefunction = compareIntValues)
                
                mp.put(map, llave, datentry)                            
                playerInfo = lt.newList()                               
                lt.addLast(playerInfo, player)                          
                om.put(datentry, overall, playerInfo)
            else:
                datentry = me.getValue(entry)                           
                position = om.contains(datentry, overall)             

                if position == False:
                    playerInfo = lt.newList()                           
                    lt.addLast(playerInfo, player)
                    om.put(datentry, overall, playerInfo)               
                else:
                    playerInfo = me.getValue(om.get(datentry, overall))
                    lt.addLast(playerInfo, player)                      

    return map

def updateTagsPlayer(map, player):                              #Req3#
    wage_eur = int(float(player['wage_eur']))    
    if player['player_tags'] != "":
        player_tags = player['player_tags'].replace(" ", "").split(sep=',')
        
        for llave in player_tags:
            entry = mp.get(map, llave)   
            if llave != "":
                if entry is None:           
                    datentry = om.newMap(omaptype = 'RBT',                  
                                        comparefunction = compareWages)
                    mp.put(map, llave, datentry)            
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

def updateTraitsPlayer(map, player):                            #Req4#
    dob = datetime.date.fromisoformat(player['dob'])
    if player['player_traits'] != "":
        player_traits = player['player_traits'].split(sep=', ')
        
        for llave in player_traits:
            entry = mp.get(map, llave) 
            if llave != "":                  
                if entry is None:           
                    datentry = om.newMap(omaptype = 'RBT',                  
                                        comparefunction = compareDates)
                    
                    mp.put(map, llave, datentry)                            
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

def updateOverall(map, player):                                 #Req5#
    overall = int(player['overall'])
    exists = om.contains(map, overall) 

    if exists == False:
        playerInfo = lt.newList()                               
        lt.addLast(playerInfo, player)                          
        om.put(map, overall, playerInfo)
    else:
        playerInfo = om.get(map, overall)['value']
        lt.addLast(playerInfo, player)

    return map

def updatePotential(map, player):                               #Req5#
    potential = int(player['potential'])
    exists = om.contains(map, potential) 

    if exists == False:
        playerInfo = lt.newList()                               
        lt.addLast(playerInfo, player)                          
        om.put(map, potential, playerInfo)
    else:
        playerInfo = om.get(map, potential)['value']
        lt.addLast(playerInfo, player)

    return map

def updateValue(map, player):                                   #Req5#
    if player['value_eur'] != "":
        value_eur = int(float(player['value_eur']))
    else:
        value_eur = 0
    exists = om.contains(map, value_eur) 

    if exists == False:
        playerInfo = lt.newList()                               
        lt.addLast(playerInfo, player)                          
        om.put(map, value_eur, playerInfo)
    else:
        playerInfo = om.get(map, value_eur)['value']
        lt.addLast(playerInfo, player)

    return map

def updateWage(map, player):                                    #Req5#
    wage_eur = int(float(player['wage_eur']))
    exists = om.contains(map, wage_eur) 

    if exists == False:
        playerInfo = lt.newList()                               
        lt.addLast(playerInfo, player)                          
        om.put(map, wage_eur, playerInfo)
    else:
        playerInfo = om.get(map, wage_eur)['value']
        lt.addLast(playerInfo, player)

    return map

def updateAge(map, player):                                     #Req5#
    age = int(float(player['age']))
    exists = om.contains(map, age) 

    if exists == False:
        playerInfo = lt.newList()                               
        lt.addLast(playerInfo, player)                          
        om.put(map, age, playerInfo)
    else:
        playerInfo = om.get(map, age)['value']
        lt.addLast(playerInfo, player)

    return map

def updateHeight(map, player):                                  #Req5#
    height_cm = int(float(player['height_cm']))
    exists = om.contains(map, height_cm) 

    if exists == False:
        playerInfo = lt.newList()                               
        lt.addLast(playerInfo, player)                          
        om.put(map, height_cm, playerInfo)
    else:
        playerInfo = om.get(map, height_cm)['value']
        lt.addLast(playerInfo, player)

    return map

def updateWeight(map, player):                                  #Req5#
    weight_kg = int(float(player['weight_kg']))
    exists = om.contains(map, weight_kg) 

    if exists == False:
        playerInfo = lt.newList()                               
        lt.addLast(playerInfo, player)                          
        om.put(map, weight_kg, playerInfo)
    else:
        playerInfo = om.get(map, weight_kg)['value']
        lt.addLast(playerInfo, player)

    return map

def updateWeight(map, player):                                  #Req5#
    weight_kg = int(float(player['weight_kg']))
    exists = om.contains(map, weight_kg) 

    if exists == False:
        playerInfo = lt.newList()                               
        lt.addLast(playerInfo, player)                          
        om.put(map, weight_kg, playerInfo)
    else:
        playerInfo = om.get(map, weight_kg)['value']
        lt.addLast(playerInfo, player)

    return map

def updateRelease(map, player):                                 #Req5#
    if player['release_clause_eur'] != "":
        release_clause_eur = int(float(player['release_clause_eur']))
    else:
        release_clause_eur = 0
    exists = om.contains(map, release_clause_eur) 

    if exists == False:
        playerInfo = lt.newList()                               
        lt.addLast(playerInfo, player)                          
        om.put(map, release_clause_eur, playerInfo)
    else:
        playerInfo = om.get(map, release_clause_eur)['value']
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

        initList.append(firstPlayer['long_name'])
        initList.append(firstPlayer['age'])
        initList.append(firstPlayer['height_cm'])
        initList.append(firstPlayer['weight_kg'])
        initList.append(firstPlayer['nationality_name'])
        initList.append(firstPlayer['overall'])
        initList.append(firstPlayer['value_eur'])
        initList.append(firstPlayer['wage_eur'])
        initList.append(firstPlayer['release_clause_eur'])
        initList.append(firstPlayer['league_name'])
        initList.append(firstPlayer['club_name'])
        initList.append(firstPlayer['club_joined'])
        initList.append(firstPlayer['club_position'])

        if firstPlayer['player_tags'] == "" or firstPlayer['player_tags'] == " ":
            initList.append("Unknown")
        else:
            initList.append(firstPlayer['player_tags'])

        initList.append(firstPlayer['player_traits'])
        initList.append(firstPlayer['player_url'])

        list_first.append(initList)

    for indey in range((int(playersSize(analyzer))-4),(int(playersSize(analyzer)+1))):
        finitList = []
        lastPlayer = lt.getElement(analyzer['players'], indey)

        finitList.append(lastPlayer['long_name'])
        finitList.append(lastPlayer['age'])
        finitList.append(lastPlayer['height_cm'])
        finitList.append(lastPlayer['weight_kg'])
        finitList.append(lastPlayer['nationality_name'])
        finitList.append(lastPlayer['overall'])
        finitList.append(lastPlayer['value_eur'])
        finitList.append(lastPlayer['wage_eur'])
        finitList.append(lastPlayer['release_clause_eur'])
        finitList.append(lastPlayer['league_name'])
        finitList.append(lastPlayer['club_name'])
        finitList.append(lastPlayer['club_joined'])
        finitList.append(lastPlayer['club_position'])

        if lastPlayer['player_tags'] == "" or lastPlayer['player_tags'] == " ":
            finitList.append("Unknown")
        else:
            finitList.append(lastPlayer['player_tags'])

        finitList.append(lastPlayer['player_tags'])
        finitList.append(lastPlayer['player_traits'])
        finitList.append(lastPlayer['player_url'])

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
                
            info.append(arbol['info']['short_name'])
            info.append(arbol['info']['age'])
            info.append(arbol['info']['dob'])
            info.append(arbol['info']['overall'])
            info.append(arbol['info']['nationality_name'])
            info.append(arbol['info']['value_eur'])
            info.append(arbol['info']['wage_eur'])
            info.append(arbol['info']['release_clause_eur'])
            info.append(arbol['info']['club_joined'])
            info.append(arbol['info']['player_positions'])
            info.append(arbol['info']['club_position'])
            info.append(arbol['info']['player_traits'])

            if arbol['info']['player_tags'] == "" or arbol['info']['player_tags'] == " ":
                info.append('Unknown') 
            else:
                info.append(arbol['info']['player_tags']) 

            completeInfo.append(info)
            cont+=1

            if arbol['next'] != None:
                arbol = arbol['next']
                info = []
                league_name = arbol['info']['league_name']
                league_level = arbol['info']['league_level']
                    
                info.append(arbol['info']['short_name'])
                info.append(arbol['info']['age'])
                info.append(arbol['info']['dob'])
                info.append(arbol['info']['overall'])
                info.append(arbol['info']['nationality_name'])
                info.append(arbol['info']['value_eur'])
                info.append(arbol['info']['wage_eur'])
                info.append(arbol['info']['release_clause_eur'])
                info.append(arbol['info']['club_joined'])
                info.append(arbol['info']['player_positions'])
                info.append(arbol['info']['club_position'])
                info.append(arbol['info']['player_traits'])

                if arbol['info']['player_tags'] == "" or arbol['info']['player_tags'] == " ":
                    info.append('Unknown') 
                else:
                    info.append(arbol['info']['player_tags']) 

                completeInfo.append(info)
                cont+=1
        else:
            break

    return league_name, league_level, completeInfo

def req2(analyzer, player_positions, overallMin, overallMax, potentialMin, potentialMax, wage_eurMin, wage_eurMax):
    arbol = mp.get(analyzer['overallPlayer'], player_positions)['value']
    valores = om.values(arbol, overallMin, overallMax)
    completeInfo = []
        
    for i in lt.iterator(valores):
        data = i['first']['info']

        if int(data['potential']) >= potentialMin and int(data['potential']) <= potentialMax and int(float(data['wage_eur'])) >= wage_eurMin and int(float(data['wage_eur'])) <= wage_eurMax:
            info = []
                        
            info.append(data['short_name'])
            info.append(data['age'])
            info.append(data['dob'])
            info.append(data['nationality_name'])
            info.append(data['value_eur'])
            info.append(data['wage_eur'])
            info.append(data['release_clause_eur'])
            info.append(data['potential'])
            info.append(data['overall'])
            info.append(data['player_positions'])
            info.append(data['player_traits'])

            if data['player_tags'] == "" or data['player_tags'] == " ":
                info.append('Unknown') 
            else:
                info.append(data['player_tags']) 

            completeInfo.append(info)
    return completeInfo

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
                                
        info.append(data['long_name'])
        info.append(data['age'])
        info.append(data['dob'])
        info.append(data['nationality_name'])
        info.append(data['value_eur'])
        info.append(data['wage_eur'])
        info.append(data['club_name'])
        info.append(data['league_name'])
        info.append(data['potential'])
        info.append(data['overall'])
        info.append(data['player_positions'])
        info.append(data['player_traits'])

        if data['player_tags'] == "" or data['player_tags'] == " ":
                info.append('Unknown') 
        else:
            info.append(data['player_tags'])

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
                
        info.append(data['long_name'])
        info.append(data['age'])
        info.append(data['dob'])
        info.append(data['nationality_name'])
        info.append(data['value_eur'])
        info.append(data['wage_eur'])
        info.append(data['club_name'])
        info.append(data['league_name'])
        info.append(data['potential'])
        info.append(data['overall'])
        info.append(data['player_positions'])
        info.append(data['player_traits'])

        if data['player_tags'] == "" or data['player_tags'] == " ":
                info.append('Unknown') 
        else:
            info.append(data['player_tags'])

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
    return om.minKey(analyzer)

def maxKey(analyzer):
    """
    Llave mas grande
    """
    return om.maxKey(analyzer)


# ==============================
# Funciones de Comparacion
# ==============================

def compareClubsName(club1, entry):
    """
    Compara el nombre de dos clubes
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

def compareIntValues(value1, value2):
    """
    Compara dos valores enteros
    """
    if (value1 == value2):
        return 0
    elif (value1 > value2):
        return 1
    else:
        return -1

def compareWages(wage1, wage2):
    """
    Compara dos salarios
    """
    if (int(wage1) == int(wage2)):
        return 0
    elif (int(wage1) > int(wage2)):
        return 1
    else:
        return -1

def comparePlayers(player1, player2):
    """
    Compara dos jugadores
    """
    if (player1 == player2):
        return 0
    elif player1 > player2:
        return 1
    else:
        return -1

# ==============================
# Funciones de ordenamiento
# ==============================

