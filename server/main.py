#!/usr/bin/env python3
import socket
from pynput import keyboard
import os
import sys
import _thread

def get_file_content(filename):
    try:
        with open(filename, 'rb') as file:
            return file.read()
    except FileNotFoundError:
        return None

def create_response(content):
    if content is None:
        response= b"HTTP/1.1 404 Not Found\r\n"
        response += b"Content-Type: text/html\r\n"
        response += b"Content-Length: 23\r\n"
        response += b"\r\n"
        response += b"<h1>404 Not Found</h1>\r\n"
        return response

    else:
        response= b"HTTP/1.1 200 OK\r\n"
        response += b"Content-Type: text/html\r\n"
        response += f"Content-Length: {len(content)}\r\n".encode()
        response += b"<h1>200 OK</h1>\r\n"
        response += b"\r\n"
        response += content
        return response

def on_press(key):
    if key== keyboard.KeyCode.from_char('q'):
        server_socket.close()
        sys.exit()

server_socket = socket.socket()

def start_server(host='0.0.0.0', port=8080, response="response.html"):
    global server_socket

    #to prevent the socket being left in time wait state
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        #the server is listening on port 8080 on any network
        server_socket.bind(("0.0.0.0", 8080))

        server_socket.listen(5)#server can have a backlog connection requests of 10
        print(f'Server listening on {host}:{port}')

        while True:
            client_socket, client_address = server_socket.accept()
            print(f'Accepted connection from {client_address}')

            request = client_socket.recv(1024).decode()
            print(f'Received {request}')

            content = get_file_content(response)

            response= create_response(content)
            client_socket.send(response)

            client_socket.close()

    except KeyboardInterrupt:
        print("Shutting down the server")
    finally:
        server_socket.close()

if __name__ == '__main__':

    if not os.path.exists('response.html'):
        with open('response.html', 'w') as f:
            f.write("""
            <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <title>response</title>
    </head>
    <body>
      <h1>
        Hello this is server generated default response
      </h1>
    </body>
    </html>
            """)

    # start listening for keyboard inputs
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    start_server()