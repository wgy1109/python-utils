import socket

s = socket.socket()
host = "127.0.0.1"
port = 11223
s.bind((host, port))

s.listen(5)
while True:
    c,addr = s.accept()
    print("连接地址：", addr)
    while True:
        data = c.recv(1024)
        print("recive : ", data.decode())
        c.send(data.upper())
    c.close()