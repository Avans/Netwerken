import SocketServer, threading

def start():
    class BasicTCPHandler(SocketServer.BaseRequestHandler):
        def handle(self):
            while True:
                print self.request.recv(1024)

    server = SocketServer.TCPServer(('0.0.0.0', 9998), BasicTCPHandler)

    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
