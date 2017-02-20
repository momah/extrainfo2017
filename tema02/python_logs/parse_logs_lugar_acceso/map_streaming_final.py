#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import sys
import csv
import os
import fileinput
import re
import time
from datetime import datetime


def read_input(file):
    for line in file:
        yield line


def create_ips_scheme():
    dict = {}
    with open('ips_esquema.csv', 'r') as f:
        next(f)
        reader = csv.reader(f)
        for rows in reader:
            dict[rows[0]] = [rows[1], rows[2]]
    return dict


# Map básico que ya clasifica las líneas en franjas horarias y procedencia interna y externa de la ULL
def map_v1_0():
    lines = 0
    scheme = create_ips_scheme()

    data = read_input(sys.stdin)
    for line in data:
        lines += 1
        campos = line.replace('  ', ' ').replace(' - - ', ' ').replace(' "-" "-"', ' ').split(' ')

        if campos:
            date = datetime.strptime(line[line.find('[')+1 : line.find(' +')], '%d/%b/%Y:%H:%M:%S')
            year, mes, dia, hora = date.strftime('%Y'), date.strftime('%m'), date.strftime('%d'), date.strftime('%H')
            ip = campos[5]
            acceso, tipo = "Externo ULL", "Externo ULL"

            if ip[0].isdigit():
                ip_split = ip.split('.')

                ip_base = ip_split[0] + '.' + ip_split[1] + '.' + ip_split[2] + ".0/24"
                if scheme.get(ip_base):
                    acceso, tipo = scheme[ip_base][0], scheme[ip_base][1]
                else:
                    ip_base = ip_split[0] + '.' + ip_split[1] + ".0.0/16"
                    if scheme.get(ip_base):
                        acceso, tipo = scheme[ip_base][0], scheme[ip_base][1]
                    else:
                        ip_base = ip_split[0] + ".0.0.0/8"
                        if scheme.get(ip_base):
                            acceso, tipo = scheme[ip_base][0], scheme[ip_base][1]

            elif ip.startswith("systemon5"):
                acceso, tipo = "Monitorizar", "Cableado"
            elif ip.startswith("www.campusvirtual") or ip.startswith("ocw.ull"):
                acceso, tipo = "Redirigir", "Cableado"

            # Formato: Año log, lugar de acceso ("Interno ULL", "Externo ULL"), tipo de conexión ("wifi","cableado"), 1 (valor) 
            output = "{0};{1};{2};1".format(year, acceso, tipo)
            print (output)

    return lines

def main():
 
    start_time = time.time()

    output_lines = map_v1_0()

    if str(output_lines).isdigit():
        print >> sys.stderr, 'Map procesadas ' + str(output_lines) + ' líneas'
        total_time = str(time.time() - start_time)
        print >> sys.stderr, 'Map tiempo ' + total_time + ' segundos'
    else:
        print >> sys.stderr, 'Error: brake:  ' + output_lines
    return 0


if __name__ == '__main__':
    main()
