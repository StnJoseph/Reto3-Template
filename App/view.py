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
from DISClib.ADT import graph as gr
import sys
import controller
import threading
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
servicefile = 'Bikeshare-ridership-2021-utf8-small.csv'
initialStation = None
searchMethod = None

# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("**************************************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de buses de singapur")
    print("3- Calcular componentes conectados")
    print("4- Establecer estación base:")
    print("5- Establecer metodo de busqueda:")
    print("6- Hay camino entre estacion base y estación: ")
    print("7- Ruta de costo mínimo desde la estación base y estación: ")
    print("8- Estación que sirve a mas rutas: ")
    print("9- Existe un camino de busqueda entre base y estación: ")
    print("10- Ruta de busqueda entre la estación base y estación: ")
    print("0- Salir")
    print("**************************************************************")
    print()


def optionTwo(cont):
    print("========== LOADING DATA ==========")
    print("Cargando información del archivo ....")
    print()
    controller.loadServices(cont, servicefile)
    numedges = controller.totalConnections(cont)
    numvertex = controller.totalStops(cont)
    print("========== LOADED DATA ==========")
    print('Numero de vertices: ' + str(numvertex))
    print('Numero de arcos: ' + str(numedges))
    #print(gr.edges(cont['connections']))
    #print(cont['station'])
    #print(cont['vertex'])
    #print(cont['connections'])
    print(controller.printDic())
    
    """vertex = gr.vertices(cont['connections'])
    index = 1
    for v in lt.iterator(vertex):
        if index < 6:
            dataInit = lt.getElement(cont['vertex'], index)
        
            print(dataInit['Start Station Id'])
            print(dataInit['Start Station Name'])

            print(gr.degree(cont['connections'], v))
            print(gr.outdegree(cont['connections'], v))
            print()
        index+=1"""


    """list_First = []
    for index in range(1,6):
        listInit = []
        dataInit = lt.getElement(cont['vertex'], index)
        listInit.append(dataInit['Start Station Id'])
        listInit.append(dataInit['Start Station Name'])
        list_First.append(listInit)
    for i in list_First:
        print(i)
        print()"""
    #print(list_End)
    #print('El limite de recursion actual: ' + str(sys.getrecursionlimit()))
    print()


def optionThree(cont):
    print('El número de componentes conectados es: ' +
          str(controller.connectedComponents(cont)))


def optionFour(cont, initialStation):
    print('Calculando costo de caminos')
    controller.minimumCostPaths(cont, initialStation)
    print("FIN!")


def optionFive(cont, initialStation, searchMethod):
    controller.searchPaths(cont, initialStation, searchMethod)


def optionSix(cont, destStation):
    haspath = controller.hasPath(cont, destStation)
    print('Hay camino entre la estación base : ' +
          'y la estación: ' + destStation + ': ')
    print(haspath)


def optionSeven(cont, destStation):
    path = controller.minimumCostPath(cont, destStation)
    if path is not None:
        pathlen = stack.size(path)
        print('El camino es de longitud: ' + str(pathlen))
        while (not stack.isEmpty(path)):
            stop = stack.pop(path)
            print(stop)
    else:
        print('No hay camino')


def optionEight(cont):
    maxvert, maxdeg = controller.servedRoutes(cont)
    print('Estación: ' + maxvert + '  Total rutas servidas: '
          + str(maxdeg))


def optionNine(cont, destStation, searchMethod):
    haspath = controller.hasSearchPath(cont, destStation, searchMethod)
    print(haspath)


def optionTen(cont, destStation, searchMethod):
    path = controller.hasSearchPath(cont, destStation, searchMethod)
    if path is not False:
        pila = controller.searchPathTo(cont, destStation, searchMethod)
        
        while (not stack.isEmpty(pila)):
            rutas = stack.pop(pila)
            print(rutas)
    else:
        print('No hay camino')


"""
Menu principal
"""


def thread_cycle():
    while True:
        printMenu()
        inputs = input('Seleccione una opción para continuar\n>')

        if int(inputs) == 1:
            print("\nInicializando....")
            # cont es el controlador que se usará de acá en adelante
            cont = controller.init()

        elif int(inputs) == 2:
            optionTwo(cont)

        elif int(inputs) == 3:
            optionThree(cont)

        elif int(inputs) == 4:
            msg = "Estación Base: BusStopCode-ServiceNo (Ej: 75009-10): "
            initialStation = input(msg)
            optionFour(cont, initialStation)

        elif int(inputs) == 5:
            searchMethod = input("Digite el metodo a implementar: ")
            optionFive(cont, initialStation, searchMethod)

        elif int(inputs) == 6:
            destStation = input("Estación destino (Ej: 15151-10): ")
            optionSix(cont, destStation)

        elif int(inputs) == 7:
            destStation = input("Estación destino (Ej: 15151-10): ")
            optionSeven(cont, destStation)

        elif int(inputs) == 8:
            optionEight(cont)

        elif int(inputs) == 9:
            optionNine(cont, destStation, searchMethod)

        elif int(inputs) == 10:
            optionTen(cont, destStation, searchMethod)

        else:
            sys.exit(0)
    sys.exit(0)


if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 20)
    thread = threading.Thread(target=thread_cycle)
    thread.start()
