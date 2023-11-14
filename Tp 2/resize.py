import sys
from PIL import Image
import socket

# Get the scale factor and the image name from the socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind(('localhost', 12346))
    server_socket.listen(1)
    conn, addr = server_socket.accept()
    with conn:
        data = conn.recv(1024)
        scale, image_path = data.decode().split()

try:
    with Image.open(image_path) as image:
        image.thumbnail((int(image.width * float(scale)), int(image.height * float(scale))))
        image.save(image_path)
except Exception as e:
    print(f'Error: {e}')
    sys.exit(1)

# Send a message to the main server to notify that the image processing is done
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect(('localhost', 12345))  # Assuming the main server is listening on localhost:12345
    client_socket.send(b'Image processing done')

