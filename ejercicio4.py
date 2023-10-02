#Realizar un programa que implemente fork junto con el parseo de argumentos. Deberá realizar relizar un fork si -f aparece entre las opciones al ejecutar el programa. El proceso padre deberá calcular la raiz cuadrada positiva de un numero y el hijo la raiz negativa.

import numpy
import argparse
import os 
import sys 

parser = argparse.ArgumentParser()  
parser.add_argument('-n','--number',type=float, help='radicand')
parser.add_argument('-f','--fork',help='fork process', action='store_true')
args = parser.parse_args()

if args.number<0:
    raise ValueError('Ingresar un número no negativo')

if args.fork == True:
    ret = os.fork()
    if ret > 0:
        raiz = numpy.sqrt(args.number)
        sys.stdout.write(str(raiz))
    
    elif ret == 0:
        if args.number == 0.0:
            sys.stdout.write('\n0.0')
        else:
            raiz = numpy.sqrt(args.number)
            sys.stdout.write(f'\n-{raiz}')
else:
    sys.stdout.write(f'Seleccionaste el número: {args.number}')