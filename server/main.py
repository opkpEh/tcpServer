#!/usr/bin/env python3
import errno
import socket
from pynput import keyboard
import os
import sys
import threading

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
        response += b"<h1>404 Not Found</h1>"
        return response

    else:
        response= b"HTTP/1.1 200 OK\r\n"
        response += b"Content-Type: text/html\r\n"
        response += f"Content-Length: {len(content)}\r\n".encode()
        response += b"<h1>200 OK</h1>\r\n"
        response += b"\r\n"
        return response + content

def on_press(key):
    if key== keyboard.KeyCode.from_char('q'):
        server_socket.close()
        sys.exit(0)

server_socket = socket.socket()

def handle_client(client_socket, client_address, response):
    try:
        request = client_socket.recv(1024).decode()
        print(f'Handling connection from {client_address}')

        print(f'Received request from :{client_address}:\n{request}')
        content= get_file_content(response)
        http_response = create_response(content)
        client_socket.send(http_response)

    except Exception as e:
        print(f'Error handling client {client_address}" {str(e)}')

    finally:
        client_socket.close()
        print(f'Client {client_address} closed')


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
            try:
                client_socket, client_address = server_socket.accept()
                print(f'Accepted connection from {client_address}')


                #creating a new thread for client:
                client_thread= threading.Thread(
                    target=handle_client,
                    args=(client_socket,client_address, response)
                )

                client_thread.daemon= True #Thread will close when the main program exits
                client_thread.start()
                print(f'Started thread for client {client_socket}')

            except socket.error as e:
                if e.errno == 9: # Bad file descriptor when socket is closed
                    break
                else:
                    print(f'Error accepting connection {e}')

    except KeyboardInterrupt:
        print("Shutting down the server...")
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