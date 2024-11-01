import socket
s = socket.socket()
s.connect(("127.0.0.0", 8080))
s.send(b'hey')
print(str(s.recv(4069)))