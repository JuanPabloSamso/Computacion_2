import os
import socket
import sys
import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi
import PIL.Image as Image


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'<html><body><h1>TP2 - Procesa imagenes</h1>')
        self.wfile.write(b'<form enctype="multipart/form-data" method="post">')
        self.wfile.write(b'<p>Archivo: <input type="file" name="file"></p>')
        self.wfile.write(b'<p>Escala: <input type="number" name="scale" min="0" max="1" step="0.01"></p>')
        self.wfile.write(b'<p><input type="submit" value="Enviar"></p>')
        self.wfile.write(b'</form></body></html>')

    def do_POST(self):
        # Use cgi to parse the multipart/form-data
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })
        
        # Get the file and the scale factor from the form
        file_item = form['file']
        scale = form['scale'].value
        
        # Save the file to a temporary location
        image_name = 'image.jpg'
        with open(image_name, 'wb') as f:
            f.write(file_item.file.read())
            
        # Create a child process to convert the image to grayscale
        pid = os.fork()
        if pid == 0:  # Child process
            with Image.open(image_name) as image:
                grayscale_image = image.convert('L')
                grayscale_image.save(image_name)
            # Create a socket to send the scale factor and the image name to resize.py
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect(('localhost', 12346))  # Assuming the scaling server is listening on localhost:12346
                client_socket.send(f'{scale} image.jpg'.encode())
            sys.exit(0)  # Exit the child process
        
        # Wait for the child process to finish
        os.waitpid(pid, 0)

        # Create a socket to listen for a message from resize.py
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind(('localhost', 12345))
            server_socket.listen(1)
            conn, addr = server_socket.accept()
            with conn:
                data = conn.recv(1024)
                if data == b'Image processing done':
                    # Send the response 200 and the headers to the client
                    self.send_response(200)
                    self.end_headers()
                    # Send the processed image to the client
                    with open('image.jpg', 'rb') as f:
                        self.wfile.write(f.read())
            # Close the connection with the socket that sent the message
            conn.close()
        # Shutdown the server that listens on port 12345
        server_socket.shutdown(socket.SHUT_RDWR)
                        

                        
        

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

