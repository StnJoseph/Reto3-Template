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
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import dfs as dfs
from DISClib.Algorithms.Graphs import bfs as bfs
from DISClib.Utils import error as error
assert config

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de Toronto Bikeshare")
    print("3- Comparar bicicletas para las estaciones con más viajes de origen.")
    print("4- Reconocer los componentes fuertemente conectado del sistema")
    print("5- Planear una ruta rápida para el usuario.")
    print("6- Reportar rutas en un rango de fechas para los usuarios anuales")
    print("7- Planear el mantenimiento preventivo de bicicletas")
    print("8-  La estación más frecuentada por los visitantes")
    print("0- Salir")
    print("*******************************************")

cont = None

def thread_cycle():
    while True:
        printMenu()
        inputs = input('Seleccione una opción para continuar\n>')

        if int(inputs) == 1:
            print("Inicializando....")

            #cont = controller.init()

        elif int(inputs) == 2:
            #Requerimiento sin parametros#
            pass

        elif int(inputs) == 3:
            intiStation = input('Nombre estación de inicio: ')
            diponibility = input('Disponibilidad: ')
            minRuteStops = int(input('Número minimo de estaciones de parada para la ruta: '))
            maxNumRutes = int(input('Maximo número de rutas de respuesta: '))

        elif int(inputs) == 4:
            #Requerimiento sin parametros#
            pass

        elif int(inputs) == 5:
            initStation = input('Estación de inicio: ')
            finitStation = input('Estacion de destino: ')

        elif int(inputs) == 6:
            initDate = input('Fecha inicial de consulta: ')
            finitDate = input('Fecha final de consulta: ')

        elif int(inputs) == 7:
            bike_id = int(input('Identificador de la bicicleta en el sistema: '))

        elif int(inputs) == 8:
            nameStation = input('Nombre de la estacion: ')
            initDate = input('Fecha inicial de consulta: ')
            finitDate = input('Fecha final de consulta: ')

        else:
            break #sys.exit(0)
    #sys.exit(0)

# Construccion de modelos

# Funciones para agregar informacion al catalogo

# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
