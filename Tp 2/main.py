import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
import socket
import os
import subprocess
import threading

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            with open('image.jpg', 'wb') as f:
                f.write(post_data)
            subprocess.check_call(['./resize.py', 'image.jpg'])
            
            # Create a socket to listen for a message from resize.py
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                server_socket.bind(('localhost', 12345))
                server_socket.listen(1)
                conn, addr = server_socket.accept()
                with conn:
                    data = conn.recv(1024)
                    if data == b'Image processing done':
                        with open('image.jpg', 'rb') as f:
                            self.send_response(200)
                            self.end_headers()
                            self.wfile.write(f.read())
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b'Error al procesar la imagen')

def main():
    parser = argparse.ArgumentParser(description='Tp2 - procesa imagenes',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog='''Ejemplo de uso:
                                             python main.py -i 127.0.0.1 -p 8000''')
    parser.add_argument('-i', '--ip', type=str, required=True, help='Direccion de escucha')
    parser.add_argument('-p', '--port', type=int, required=True, help='Puerto de escucha')
    args = parser.parse_args()

    try:
        server = HTTPServer((args.ip, args.port), RequestHandler)
        print(f'Server running on {args.ip}:{args.port}')
        server.serve_forever()
    except Exception as e:
        print(f'Error: {e}')
    finally:
        if server:
            server.server_close()

if __name__ == '__main__':
    main()

