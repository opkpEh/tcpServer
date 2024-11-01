import socket

client_socket = socket.socket()

#where we want the client to connect
host='127.0.0.1'
port = 8080

http_request=f"""GET / HTTP/1.1\r\nHost: {host}\r\n\r\n"""

try:
    #trying to connect
    client_socket.connect((host, port))
    print(f"Connected to {host} on port {port}")

    client_socket.send(http_request.encode('utf-8'))
    print("request sent")

    #recieving the data
    while True:
        data=client_socket.recv(4096)
        if not data:
            break

        print(f"Received: {data.decode('utf-8')}")

#a few exceptions
except ConnectionRefusedError:
    print(f"Connection refused to the server at {host}:{port}")

except socket.timeout:
    print(f"Connection timed out")

except KeyboardInterrupt:
    print("Connection closed")