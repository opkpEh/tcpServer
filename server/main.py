#!/usr/bin/env python3
import socket
from pynput import keyboard
import sys
import _thread

def on_press(key):
    if key== keyboard.KeyCode.from_char('q'):
        server_socket.close()
        sys.exit()

#start listening for keyboard inputs
listener = keyboard.Listener(on_press=on_press)
listener.start()

server_socket= socket.socket()

#to prevent the socket being left in time wait state
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#the server is listening on port 8080 on any network
server_socket.bind(("0.0.0.0", 8080))

server_socket.listen(10)#server can have a backlog connection requests of 10

#b infront means the string is in bytes not UNICODE
http_response = b"""HTTP/1.1 200 OK\r\n
Content-Type: text/plain\r\n
Content-Length: 10\r\n
\r\n
Hellllo!\n"""

def respond(conn):
    request= str(conn.recv(4096))
    print(request)
    conn.send(http_response)
    conn.shutdown(socket.SHUT_RDWR)  # shut down read write
    conn.close()

try:
    while True:
        conn, address = server_socket.accept()  # waiting for a connection
        _thread.start_new_thread(respond, (conn,))

except KeyboardInterrupt:
    server_socket.close()
    sys.exit()