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
import json

# Map sencillo que cuenta las líneas del fichero de entrada y las imprime
def map_v1_0():
    lines = 0
    for line in fileinput.input():
        lines += 1
    return (lines)

# Map básico que ya clasifica las líneas en franjas horarias y procedencia interna y externa de la ULL
def map_v2_0():
    lines = 0
    error = 0
    meses = {"Jan":"01", "Feb":"02", "Mar":"03", "Apr":"04", "May":"05", "Jun":"06", "Jul":"07", "Aug":"08", "Sep":"09", "Oct":"10", "Nov":"11", "Dec":"12"}
    dias = {"00": "00","01": "01","02": "02","03": "03","04": "04","05": "05","06": "06","07": "07","08": "08","09": "09","10": "10","11": "11","12": "12","13": "13","14": "14",
             "15": "15","16": "16","17": "17","18": "18","19": "19","20": "20","21": "21","22": "22","23": "23",
            "24": "24","25": "25","26": "26","27": "27","28": "28","29": "29","30": "30","31": "31"}
    horas = {"00": "00","01": "01","02": "02","03": "03","04": "04","05": "05","06": "06","07": "07","08": "08","09": "09","10": "10","11": "11","12": "12","13": "13","14": "14",
             "15": "15","16": "16","17": "17","18": "18","19": "19","20": "20","21": "21","22": "22","23": "23"}
    for line in fileinput.input():
        lines += 1
        mes = meses.get(line[0:3], "Error")
        dia = dias.get(line[4:6], "Error")
        hora = horas.get(line[7:9], "Error")
        externo = "externo"
        if mes == "Error":
            error += 1
            return("Error mes" + line)
        if dia == "Error":
            error += 1
            return("Error dia " + line)
        if hora == "Error":
            error += 1
            return("Error hora " + line)
        campos = line.split(" ")
        ip = campos[5].split(".")
        if ip[0]=="systemon5":
            externo = "monitorizar"
        else:
            if (ip[0] == "www" and ip[1] == "campusvirtual") or (ip[0] == "ocw" and ip[1] == "ull"):
                externo = "redirigir"
            else:
                if not ip[0].isdigit():
                    return("Error ip1 no es dígito" + line)
                ip1 = int(ip[0])
                if not ip[1].isdigit():
                    return("Error ip2 no es dígito" + line)
                ip2 = int(ip[1])
                if not ip[2].isdigit():
                    return("Error ip3 no es dígito" + line)
                ip3 = int(ip[2])
                if not ip[3].isdigit():
                    return("Error ip4 no es dígito" + line)
                ip4 = int(ip[3])
                if ip1 == 10:
                    externo="interno"
                if ip1 == 172 and ip2 >=16 and ip2 <=31:
                    externo="error"
                    return("Error ip " + campos[5] + 'xxx' + line)
                if ip1 == 192 and ip2 ==168:
                    externo="error"
                    return("Error ip " + campos[5] + 'xxx' + line)
                if ip1 == 193 and ip2==145 and ip3>=96 and ip3<=125:
                    externo="interno"
        # Formato: Mes log, día de log, hora de log, tipo de log("monitorizar","redirigir", "interno", "externo","error"), 1 (valor) 
        output = "{0};{1};{2};{3};1".format(mes, dia, hora, externo)
        print (output)

    return lines

def main():
 
    start_time = time.time()

    output_lines = map_v2_0()

    if str(output_lines).isdigit():
        print >> sys.stderr, 'Map procesadas ' + str(output_lines) + ' líneas'
        total_time = str(time.time() - start_time)
        print >> sys.stderr, 'Map tiempo ' + total_time + ' segundos'
    else:
        print >> sys.stderr, 'Error: brake:  ' + output_lines
    return 0


if __name__ == '__main__':
    main()
