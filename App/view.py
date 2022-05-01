"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
import datetime
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print()
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Reportar las cinco adquisiciones más recientes de un club")
    print("3- Reportar los jugadores de cierta posición en un rango de desempeño, potencial y salario")
    print("4- Reportar los jugadores en un rango salarial y con cierta etiqueta")
    print("5- Reportar los jugadores con un rasgo característico en un periodo de tiempo")
    print("6- Req. 5")
    print("7- Req. 6")
    print("0- Salir")
    print()

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1: 
        print()
        print("========== LOADING DATA ==========")
        print("Cargando información del archivo ....")
        print()
        cont = controller.init() 
        controller.loadData(cont)
        print("========== LOADED DATA ==========")
        print("El total de jugadores cargados es: " + str(controller.playersSize(cont)))
        print()
        print('Los 5 primeros jugadores cargados son: ' + str(controller.Init_Finit_Players(cont)[0]))
        print()
        print('Los 5 ultimos jugadores cargados son: ' + str(controller.Init_Finit_Players(cont)[1]))
        print()

    elif int(inputs[0]) == 2:
        print("========== Req. 1 Input ==========")
        clubName = input("Nombre del club: ")
        print()
        print("========== Req. 1 Output ==========")
        print("El club " + str(clubName) + " tiene " + str(controller.indexSize(mp.get(cont['clubsName'], clubName)['value'])) + " adquisiciones.")
        print()
        print("---League Details---")
        print("Nombre: " + str(controller.req1(cont, clubName)[0]))
        print("Categoria: " + str(controller.req1(cont, clubName)[1]))
        print()
        print(controller.req1(cont, clubName)[2])
        print()


    elif int(inputs[0]) == 3:
        print("========== Req. 2 Input ==========")
        player_positions = input("Posicion del jugador: ").upper()
        overallMin = int(input("Desempeño minimo: "))
        overallMax = int(input("Desempeño maximo: "))
        potentialMin = int(input("Potencial minimo: "))
        potentialMax = int(input("Potencial maximo: "))
        wage_eurMin = int(float(input("Salario minimo: ")))
        wage_eurMax = int(float(input("Salario maximo: ")))
        print()
        print("========== Req. 2 Output ==========")
        print("Jugadores encontrados en el rango de " + str(player_positions) + " son: ")
        print()
        print(str(controller.req2(cont, player_positions, overallMin, overallMax, potentialMin, potentialMax, wage_eurMin, wage_eurMax)))
        print()


    elif int(inputs[0]) == 4:
        print("========== Req. 3 Input ==========")
        wage_eurMin = int(float(input("Salario minimo: ")))
        wage_eurMax = int(float(input("Salario maximo: ")))
        player_tags = input("Caracteristica de los jugadores: ")
        print()
        print("========== Req. 3 Output ==========")
        print("Los jugadores de FIFA encontrados entre el rango " + str(wage_eurMin) + " y " + str(wage_eurMax) + " son: " + str(controller.req3(cont, player_tags, wage_eurMin, wage_eurMax)[0]))
        print()
        print("Los " + str(controller.req3(cont, player_tags, wage_eurMin, wage_eurMax)[0]) + " jugadores encontrados son: ")
        print()
        print(str(controller.req3(cont, player_tags, wage_eurMin, wage_eurMax)[1]))
        print()
        

    elif int(inputs[0]) == 5:
        print("========== Req. 4 Input ==========")
        playerTrait = input("Caracteristica de los jugadores: ")
        dobMin = datetime.date.fromisoformat(input("Fecha de nacimiento minima: "))
        dobMax = datetime.date.fromisoformat(input("Fecha de nacimiento maxima: "))
        print()
        print("========== Req. 4 Output ==========")
        print("Los jugadores de FIFA encontrados entre el rango " + str(dobMin) + " y " + str(dobMax) + " son: " + str(controller.req4(cont, playerTrait, dobMin, dobMax)))
        print()
        print("Los " + str(controller.req4(cont, playerTrait, dobMin, dobMax)[0]) + " jugadores encontrados son: ")
        print()
        print(str(controller.req4(cont, playerTrait, dobMin, dobMax)[1]))
        print()
  

    elif int(inputs[0]) == 6:
        print("========== Req. 5 Input ==========")
        N = int(float(input("Numero de segmentos del rango: ")))
        x = int(float(input("Numero de niveles de jugadores: ")))
        propierty = input("Propiedad del histograma: ").lower()
        print()
        print("========== Req. 5 Output ==========")
        min = om.minKey(cont[propierty])
        max = om.maxKey(cont[propierty])
        add = (max-min)/N
        listSegments = []
        listPlayers = []
        listPoints = []
        conta = 0
        numTotalPlayer = 0
        
        for i in range(0,N):
            listSegments.append([round(min+(add*i), 3), round(min+(add*(i+1)), 3)])

        for k in lt.iterator(om.keySet(cont[propierty])):
            numPlayers = lt.size(om.get(cont[propierty], k)['value'])

            if k <= listSegments[conta][1]:
                numTotalPlayer += numPlayers
            if k > listSegments[conta][1]:
                listPlayers.append(numTotalPlayer)
                numTotalPlayer = 0
                numTotalPlayer += numPlayers
                conta+=1
        
        while len(listPlayers)<N:
            listPlayers.append(lt.size(om.get(cont[propierty], k)['value']))

        for j in range(0,N):
            listPoints.append(listPlayers[j]//x)
                    
        print("+---------------------------------------+")
        print("|bin            | count  |  lvl|  mark  |")
        print("+=======================================+")
        for l in range(0, N):
            print("|"+str(listSegments[l])+ "|" +str(listPlayers[l])+"  |"+str(listPoints[l])+"  |"+str((listPoints[l]*"*"))+"|")
            print("+---------------------------------------+")
        print()


    elif int(inputs[0]) == 7:
        print("COMING SOON...")

    else:
        sys.exit(0)