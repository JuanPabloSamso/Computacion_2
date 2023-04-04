import argparse
import sys
def main():
    parser = argparse.ArgumentParser(prog='Programa impares')
    parser.add_argument('-n', '--number',type=int, help= 'Elegir un numero entero positivo')
    args = parser.parse_args()
    if args.number<=0:
        raise ValueError('El numero ingresado debe ser un entero positivo')
    else:
        lista = []
        lista.append(1)
        for i in range(args.number-1):
            if args.number==1:
                break
            else:
                lista.append(lista[-1]+2)
        sys.stdout.write(str(lista))
if __name__ == '__main__':
    main()