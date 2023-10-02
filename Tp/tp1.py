import argparse
import os
import sys
from multiprocessing import Process, Pipe


def invert_line(line, conn):
    inverted_line = line[::-1]
    conn.send(inverted_line)
    conn.close()


def main():
    parser = argparse.ArgumentParser(description='Invierte las líneas de un archivo de texto')
    parser.add_argument('-f', '--file', type=str, help='Nombre del archivo a invertir', required=True)
    args = parser.parse_args()
    file_name = args.file

    if not os.path.exists(file_name):
        print(f"Error: el archivo {file_name} no existe.")
        sys.exit(1)

    processes = []
    with open(file_name, 'r') as file:
        for i, line in enumerate(file):
            read_conn, write_conn = Pipe()
            process = Process(target=invert_line, args=(line.strip(), read_conn))
            process.start()
            processes.append((write_conn, process))

        for write_conn, process in processes:
            process.join()
            inverted_line = write_conn.recv()
            sys.stdout.write(inverted_line + '\n')

if __name__ == '__main__':
    main()




