import socket, sys

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class Client:

    def listen(self, host='localhost', port=9999):
        try:
            # Connect to server and send data
            sock.connect((host, port))

            # continuously send and receive from the server
            self.data = ''
            while self.data != 'quit':
                self.received = -1
                self.data = self.send()
                sock.sendall(bytes(self.data + '\n', 'utf-8'))

                # Receive data from the server and shut down
                self.received = sock.recv(1024).decode('utf-8')
                print(f'Received: {self.received}')
        finally:
            sock.close()

    def send(self):
        return input('>>> ')

if __name__ == '__main__':
    c = Client()
    c.listen()