import socketserver

class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print(f'{self.client_address[0]} sent: {self.data}')
        # just send back the same data
        self.request.sendall(self.data)

if __name__ == '__main__':
    HOST, PORT = 'localhost', 9999

    # create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
    # interrupt the program with Ctrl-C
    server.serve_forever()