import sys
from PIL import Image
import socket
import argparse

def main():
    parser = argparse.ArgumentParser(description='Redimensiona una imagen y la convierte a escala de grises',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog='''Ejemplo de uso:
                                             python resize.py -f image.jpg -s 0.5''')
    parser.add_argument('-f', '--file', type=str, required=True, help='Archivo de imagen a procesar')
    parser.add_argument('-s', '--scale', type=float, required=True, help='Factor de escala para redimensionar la imagen')
    args = parser.parse_args()

    try:
        image_path = args.file
        scale = args.scale
        with Image.open(image_path).convert('L') as image:
            image.thumbnail((int(image.width * scale), int(image.height * scale)))
            image.save(image_path)
        
        # Send a message to the main server to notify that the image processing is done
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect(('localhost', 12345))  # Assuming the main server is listening on localhost:12345
            client_socket.send(b'Image processing done')
    except Exception as e:
        print(f'Error: {e}')
        sys.exit(1)

if __name__ == '__main__':
    main()



