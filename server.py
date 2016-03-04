from socket import *
import thread, threading

def handler(clientsock,addr):
    while True:
        data = clientsock.recv(1024)
        if not data:
            clientsock.close()
            break

def start():
    ADDR = ('0.0.0.0', 31512)
    serversock = socket(AF_INET, SOCK_STREAM)
    serversock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serversock.bind(ADDR)
    serversock.listen(5)
    while 1:
        clientsock, addr = serversock.accept()
        thread.start_new_thread(handler, (clientsock, addr))

def start_background():
    thread = threading.Thread(target=start)
    thread.daemon = True
    thread.start()
