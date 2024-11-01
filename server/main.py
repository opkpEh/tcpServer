#!/usr/bin/env python3
import socket
from pynput import keyboard
import sys

def on_press(key):
    if key== keyboard.KeyCode.from_char('q'):
        s.close()
        sys.exit()

#start listening for keyboard inputs
listener = keyboard.Listener(on_press=on_press)
listener.start()

s= socket.socket()

#to prevent the socket being left in time wait state
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#the server is listening on port 8080 on any network
s.bind(("0.0.0.0", 8080))

s.listen(10)#server can have a backlog connection requests of 10

#b infront means the string is in bytes not UNICODE
http_response= b"""HTTP/1.1 200 OK\r 
Content-Type: text/plain\r
Content-Length: 10\r
\r\n
Hellllo!\n"""

try:
    while True:
        conn, address = s.accept()  # waiting for a connection
        print(str(conn.recv(4096)))
        conn.send(http_response)
        conn.shutdown(socket.SHUT_RDWR)  # shut down read write
        conn.close()

except KeyboardInterrupt:
    s.close()
    sys.exit()