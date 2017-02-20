#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import argparse
import sys
import csv
import os
import glob
import fileinput
import time

# reduce sencillo suma las líneas de entrada y da la salida sumada
def reduce_v1_0():
    lines = 0
    total_lineas = 0
    for line in fileinput.input():
        lines += 1
        total_lineas += int(line)
    print(total_lineas)
    return(lines)

# Map básico que ya clasifica las líneas en franjas horarias y procedencia interna y externa de la ULL
def reduce_v2_0():
    lines = 0
    valores = dict()

    lugar = {"monitorizar": 0,"redirigir": 1, "interno": 2, "externo": 3}

    for line in fileinput.input():
        lines += 1
        campos = line.split(";")
        mes = campos[0]
        dia = campos[1]
        hora = campos[2]
        externo = campos[3]
        valor = campos[4]
        clave = mes+dia+hora
        if clave in valores:
            valores[clave][lugar[externo]] += int(valor)
        else:
            valores[clave]=[0,0,0,0]
            valores[clave][lugar[externo]] += int(valor)

    print("Mes;Día;Hora;Logs_Monitorizar;Logs_Redirigir;Logs_Interno;Logs_Externo")
    for indice, valor in valores.items():
        # Formato: Mes log, día de log, hora de log, num logs "monitorizar", num logs "redirigir",
        #                                            num logs "interno", num logs "externo"
        output = "{0};{1};{2};{3};{4};{5};{6};".format(indice[0:2], indice[2:4], indice[4:6], valor[0], valor[1], valor[2], valor[3])
        print(output)

    return lines


def main():

    start_time = time.time()

    val = reduce_v2_0()

    if str(val).isdigit():
        print >> sys.stderr, 'Reduce procesadas ' + str(val) + ' líneas'
        total_time = str(time.time() - start_time)
        print >> sys.stderr, 'Reduce tiempo ' + total_time + ' segundos'
    else:
        print >> sys.stderr, 'Error: brake:  ' + val
    return 0

if __name__ == '__main__':
    main()

