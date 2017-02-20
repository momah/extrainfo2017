#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import sys
import csv
import fileinput
import collections
import time
from sets import Set
from operator import itemgetter

def read_mapper_output(file):
    for line in file:
        yield line.rstrip().split('\t\t', 1)


def reduce_v1_0():
    lines = 0
    valores = dict()


    for line in fileinput.input():
        lines += 1
        campos = line.split(";")
        anyo = campos[0]        
        acceso= campos[1]
        conexion= campos[2]
        valor = campos[3]
        clave = anyo+"-"+acceso+"-"+conexion
        if clave in valores:
            valores[clave] += int(valor)
        else:
            valores[clave]=0
            valores[clave]+= int(valor)
    print("Año-acceso-conexión;Num_logs")
    for indice, valor in valores.items():
        # Formato: Año-acceso-conexión de log, num logs 
        output = "{0};{1};".format(indice, valor)
        print(output)

    return lines

def main():

    start_time = time.time()

    val = reduce_v1_0()

    if str(val).isdigit():
        print >> sys.stderr, 'Reduce procesadas ' + str(val) + ' líneas'
        total_time = str(time.time() - start_time)
        print >> sys.stderr, 'Reduce tiempo ' + total_time + ' segundos'
    else:
        print >> sys.stderr, 'Error: brake:  ' + val
    return 0

if __name__ == '__main__':
    main()
