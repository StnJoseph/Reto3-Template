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
import math


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

def loadData(analyzer):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    playersfile = cf.data_dir + "fifa-players-2022-utf8-small.csv"
    input_file = csv.DictReader(open(playersfile, encoding="utf-8"), delimiter=",")
    for player in input_file:
        model.addPlayer(analyzer, player)
        model.addClubPlayer(analyzer, player)
        model.addPositionPlayer(analyzer, player)
        model.addTagsPlayer(analyzer, player)
        model.addTraitsPlayer(analyzer, player)
        model.addHistogramOverall(analyzer, player)
        model.addHistogramPotential(analyzer, player)
        model.addHistogramValue(analyzer, player)
        model.addHistogramWage(analyzer, player)
        model.addHistogramAge(analyzer, player)
        model.addHistogramHeight(analyzer, player)
        model.addHistogramWeight(analyzer, player)
        model.addHistogramRelease(analyzer, player)
    return analyzer


# ==============================
#  Funciones para consultas
# ==============================

def playersSize(analyzer):
    """
    Numero de jugadores leidos
    """
    return model.playersSize(analyzer)


def indexHeight(analyzer):
    """
    Altura del indice (arbol)
    """
    return model.indexHeight(analyzer)


def indexSize(analyzer):
    """
    Numero de nodos en el arbol
    """
    return model.indexSize(analyzer)

def keySet(analyzer):
    """
    Lista de llaves
    """
    return model.keySet(analyzer)

def valueSet(analyzer):
    """
    Lista de llaves
    """
    return model.valueSet(analyzer)

def minKey(analyzer):
    """
    La menor llave del arbol
    """
    return model.minKey(analyzer)


def maxKey(analyzer):
    """
    La mayor llave del arbol
    """
    return model.maxKey(analyzer)

def Init_Finit_Players(analyzer):
    return model.Init_Finit_Players(analyzer)

def req1(analyzer, clubName):
    return model.req1(analyzer, clubName)

def req2(analyzer, player_positions, overallMin, overallMax, potentialMin, potentialMax, wage_eurMin, wage_eurMax):
    return model.req2(analyzer, player_positions, overallMin, overallMax, potentialMin, potentialMax, wage_eurMin, wage_eurMax)


def req3(analyzer, player_tags, wage_eurMin, wage_eurMax):
    return model.req3(analyzer, player_tags, wage_eurMin, wage_eurMax)

def req4(analyzer, playerTrait, dobMin, dobMax):
    return model.req4(analyzer, playerTrait, dobMin, dobMax)

# ==============================
# Funciones de ordenamiento
# ==============================