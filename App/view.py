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
    print("3- Req. 2")
    print("4- Req. 3")
    print("5- Req. 4")
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

        #print(mp.get(cont['clubsName'], clubName)['value'])
        #print(controller.indexSize(mp.get(cont['clubsName'], clubName)['value']))

        #print(om.get(mp.get(cont['clubsName'], clubName)['value'], "2021-06-30"))
        #print()
        #print(om.get(mp.get(cont['clubsName'], clubName)['value'], "2021-06-30")['value']['first']) #Esctuctura tipo TAD list#

        #print(controller.keySet(mp.get(cont['clubsName'], clubName)['value']))
        #keys = controller.keySet(mp.get(cont['clubsName'], clubName)['value'])
        #print(controller.valueSet(mp.get(cont['clubsName'], clubName)['value']))

        #om.get(mp.get(cont['clubsName'], clubName)['value'], )

        #print(cont['clubsName'])
        #fecha = om.get(datentry, player['club_joined'])     #Obtenemos la fecha#


    else:
        sys.exit(0)
