import socket

s = socket.socket()
host = "127.0.0.1"
port = 11223

s.connect((host, port))
i = 1
while True:
    msg = " hello ， 欢迎 "
    s.send(msg.encode('utf-8'))
    data = s.recv(1024)
    print("recv : ", data.decode())
s.close()