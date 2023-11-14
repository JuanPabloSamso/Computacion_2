import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
import os, socket
from PIL import Image
from multiprocessing import Process, Queue, Event
from urllib.parse import parse_qs

def convert_to_grayscale(image_path, q, event):
    with Image.open(image_path) as image:
        grayscale_image = image.convert('L')
        q.put(grayscale_image)
    event.set()

def create_process(imagen_cliente, q, event):
    p = Process(target=convert_to_grayscale, args=(imagen_cliente, q, event))
    p.start()
    event.wait()  # Espera hasta que la conversiÃ³n de la imagen haya terminado
    p.join()

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        q = Queue()
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = parse_qs(post_data.decode())

        imagen_recibida = data.get('imagen', [''])[0]
        print(imagen_recibida)
        
        event = Event() 
        create_process(imagen_recibida, q, event)
        imagen_convertida = q.get()
        
        imagen_convertida.save('imagen_convertida.jpg')
     
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
        
        self.send_response(200)
        self.end_headers()


def main():
   
    parser = argparse.ArgumentParser(description='Tp2 - procesa imagenes',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog='''Ejemplo de uso:
                                             python main.py -i 127.0.0.1 -p 8000''')
    parser.add_argument('-i', '--ip', type=str, default="0.0.0.0", help='Direccion de escucha')
    parser.add_argument('-p', '--port', type=int, default=8080, help='Puerto de escucha')
    args = parser.parse_args()
    
    try:
        with HTTPServer(("0.0.0.0", 8080), RequestHandler) as httpd:
            print("Escuchado en puerto", 8080)
            padre=os.getpid()
            print(f"Soy el proceso padre - PID: {padre}")
            print("----------------------------------------")
            httpd.serve_forever()
    except Exception as e:
        print(f"Error al iniciar el servidor: {e}")

if __name__ == '__main__':
    main()