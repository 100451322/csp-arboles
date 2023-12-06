#!/bin/python
# -*- coding: utf-8 -*-

import constraint as c
import sys


def leer_archivo(archivo):
    """Lee el archivo de entrada y devuelve las dimensiones del mapa,
    el número de tiendas que debe haber en las filas y en las columnas, y
    las posiciones de los arboles"""

    with open(archivo, "r") as f:
        lineas = list(linea.strip() for linea in f.readlines())

        # Tomamos la informacion de las primeras 3 lineas
        # Los guiones los sustituimos por un sys.maxsize para
        # poder reconocerlos facilmente pero que sean numeros
        dimensiones = tuple(map(int, lineas[0].split("x")))
        tiendas_columnas = tuple(map(int, lineas[1].replace("-", str(sys.maxsize)).split(" ")))
        tiendas_filas = tuple(map(int, lineas[2].replace("-", str(sys.maxsize)).split(" ")))

        # Juntamos el resto de lineas en un solo string
        # para poder buscar los arboles marcados con una x
        mapa = "".join(lineas[3:])
        arboles = []
        for (idx, ch) in enumerate(mapa):
            if ch == "x":
                arboles.append(idx)

        return dimensiones, tiendas_columnas, tiendas_filas, arboles


def calcular_dominio(dimensiones, arboles):
    """Calcula los dominios de las variables de forma naive: las posiciones
    a la izquierda, derecha, arriba y abajo de cada arbol"""

    X, Y = dimensiones
    dominios = {}
    for i in arboles:
        posibles = [i-1, i+1, i-X, i+X]
        x = i % X
        y = i // X

        # Si está en la primera columna, no puede ponerse a la izquierda
        if x == 0:
            posibles.remove(i-1)
        # Si está en la ultima columna, no puede ponerse a la derecha
        if x == X-1:
            posibles.remove(i+1)

        # Si está en la primera fila, no puede ponerse encima
        if y == 0:
            posibles.remove(i-X)
        # Si está en la ultima fila, no puede ponerse debajo
        if y == Y-1:
            posibles.remove(i+X)

        # No puede ponerse encima de otro arbol
        for j in arboles:
            if j in posibles:
                posibles.remove(j)

        dominios[i] = posibles
    return dominios


def suma_vertical(dimensiones, tiendas_columnas, lista_tiendas):
    """Compriueba que la suma de las tiendas en cada columna sea correcta"""
    X, _ = dimensiones
    tiendas = list(tiendas_columnas)
    for i in lista_tiendas:
        if tiendas_columnas[i % X] == sys.maxsize:
            # No nos importa cuantas tiendas haya en las columnas con un -
            # (representado por sys.maxsize)
            continue
        tiendas[i % X] -= 1

    for i in range(X):
        if tiendas_columnas[i] == sys.maxsize:
            tiendas[i] = 0

    return all(i == 0 for i in tiendas)


def suma_horizontal(dimensiones, tiendas_filas, lista_tiendas):
    """Comprueba que la suma de las tiendas en cada fila sea correcta"""
    X, Y = dimensiones
    tiendas = list(tiendas_filas)
    for i in lista_tiendas:
        if tiendas_filas[i // X] == sys.maxsize:
            # No nos importa cuantas tiendas haya en las filas con un -
            # (representado por sys.maxsize)
            continue
        tiendas[i // X] -= 1

    for i in range(Y):
        if tiendas_filas[i] == sys.maxsize:
            tiendas[i] = 0

    return all(i == 0 for i in tiendas)


def contiguas(dimensiones, *tiendas):
    """Comprueba que se cumple que las tiendas no son contiguas
    en horizontal ni en vertical"""

    X, _ = dimensiones
    for i in tiendas:
        x1 = i % X
        y1 = i // X
        for j in tiendas:
            if i == j:
                continue
            x2 = j % X
            y2 = j // X
            if (x1 == x2 and abs(y1-y2) == 1):  # Vertical
                return False
            if (y1 == y2 and abs(x1-x2) == 1):  # Horizontal
                return False

    return True


def diagonal(dimensiones, *tiendas):
    """Comprueba que se cumple que las tiendas no se tocan en diagonal"""

    X, _ = dimensiones
    for i in tiendas:
        x1 = i % X
        y1 = i // X
        for j in tiendas:
            if i == j:
                continue
            x2 = j % X
            y2 = j // X
            if (abs(x1-x2) == 1 and abs(y1-y2) == 1):
                return False

    return True


def diagonal_func(dimensiones, *tiendas):
    """Version de 'programacion funcional' de la funcion diagonal"""
    return (abs(i % dimensiones[0] - j % dimensiones[0]) == 1 and
            abs(i // dimensiones[0] - j // dimensiones[0]) == 1
            for i in tiendas for j in tiendas if i != j)


def formatear_solucion(solucion, arboles, dimensiones, tiendas_columnas,
                       tiendas_filas):
    """Imprime la solucion en forma de matriz, usando ascii art"""
    # Quitar el sys.maxsize de las tiendas y poner un espacio
    tiendas_columnas = [i if i != sys.maxsize else " " for i in tiendas_columnas]
    tiendas_filas = [i if i != sys.maxsize else " " for i in tiendas_filas]

    print("    " + "   ".join(map(str, tiendas_columnas)))
    print("  " + "+---" * dimensiones[0] + "+")
    for i in range(dimensiones[1]):
        print(tiendas_filas[i], end=" ")
        for j in range(dimensiones[0]):
            if i*dimensiones[0] + j in arboles:
                print("| ◻ ", end="")
            elif i*dimensiones[0] + j in solucion.values():
                print("| △ ", end="")
            else:
                print("|   ", end="")
        print("|")
    print("  " + "+---" * dimensiones[0] + "+")
    print()


(X, Y), TIENDAS_COLUMNAS, TIENDAS_FILAS, ARBOLES = leer_archivo(sys.argv[1])

# Definimos el problema
problem = c.Problem()


# Definimos las variables
DOMINIOS = calcular_dominio((X, Y), ARBOLES)
for i in ARBOLES:
    problem.addVariable(i, DOMINIOS[i])

# Definimos las restricciones
# Las tiendas no pueden estar en la misma posicion
problem.addConstraint(c.AllDifferentConstraint(), ARBOLES)

# Las tiendas no pueden estar contiguas ni en diagonal
# Hacemos 3 restricciones porque es más rápido
for i in ARBOLES:
    for j in ARBOLES:
        if i != j:
            # Contiguas horizontal
            problem.addConstraint(c.FunctionConstraint(
                lambda i, j: not (i % X == j % X and abs(i // X - j // X) == 1)), (i, j))
            # Contiguas vertical
            problem.addConstraint(c.FunctionConstraint(
                lambda i, j: not (i // X == j // X and abs(i % X - j % X) == 1)), (i, j))
            # Diagonal
            problem.addConstraint(c.FunctionConstraint(
                lambda i, j: not (abs(i % X - j % X) == 1 and abs(i // X - j // X)) == 1),
                                  (i, j))

# La suma de las tiendas en cada columna debe ser correcta
problem.addConstraint(c.FunctionConstraint(
    lambda *tiendas: suma_vertical((X, Y), TIENDAS_COLUMNAS, tiendas)), ARBOLES)

# La suma de las tiendas en cada fila debe ser correcta
problem.addConstraint(c.FunctionConstraint(
    lambda *tiendas: suma_horizontal((X, Y), TIENDAS_FILAS, tiendas)), ARBOLES)


# Resolvemos el problema
solucion = problem.getSolution()
if not solucion:
    print("No hay solucion")
else:
    formatear_solucion(solucion, ARBOLES, (X, Y), TIENDAS_COLUMNAS, TIENDAS_FILAS)
    # print(solucion)
