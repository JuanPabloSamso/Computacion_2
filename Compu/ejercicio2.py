#Escribir un programa en Python que acepte dos argumentos de línea de comando: una cadena de texto, un número entero. El programa debe imprimir una repetición de la cadena de texto tantas veces como el número entero.

import argparse
import sys

def main():
    parser = argparse.ArgumentParser()  
    parser.add_argument('-s','--string',type=str, help='string to be multiplied')
    parser.add_argument('-n','--number',type=int, help='times that the string will be multiplied')
    args = parser.parse_args()
    if args.number>0:
        sys.stdout.write(str(args.string*args.number))
    else:
        raise ValueError("Por favor ingresar un número entero positivo")

if __name__ == '__main__':
    main()