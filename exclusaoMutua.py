import socket
import time


class Coordinator:
    def __init__(self, host, port): 
        self.host = host
        self.port = port
        self.clients_queue = [] 

    def handle_client(self, client_socket, address):
        print(f"Connection from {address}")
        self.clients_queue.append(client_socket)
        if len(self.clients_queue) == 1:
            self.serve_next_client()

    def serve_next_client(self): #Função recursiva utilizada para atender os clientes da fila
        if self.clients_queue:
            next_client = self.clients_queue.pop(0)
            next_client.send("You're next in line.".encode())
            time.sleep(3)  # Adicionando um pequeno atraso antes de fechar a conexão
            next_client.close()

            # Serve o próximo cliente na fila
            self.serve_next_client()

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(10)
        print(f"Coordinator listening on {self.host}:{self.port}")

        while True: #Loop infinito que aceita as conexões dos clientes. 
            client_socket, address = server_socket.accept()
            self.handle_client(client_socket, address)

class Client:
    def __init__(self, host, port): 
        self.host = host
        self.port = port
    def consumir_recurso(self):  
        own_hostname = socket.gethostname()
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        with open("file.txt", "a") as file:
            file.write(f"Hostname do cliente: {own_hostname}, Timestamp: {timestamp}\n")
        print(f"Hostname do cliente: {own_hostname}, Timestamp: {timestamp}")

    def connect(self): 
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.host, self.port))
        message = client_socket.recv(1024).decode() 
        print(message)
        self.consumir_recurso()
        client_socket.close()

if __name__ == "__main__":
    ip_local = socket.gethostbyname(socket.gethostname()) 
    coordinator_host = '172.21.0.6'  
    coordinator_port = 5555 
    

    if ip_local == coordinator_host: 
        coordinator = Coordinator(coordinator_host, coordinator_port)
        coordinator.start()
    else: 
        print(f"Eu sou um cliente com o IP: {ip_local}")
        client = Client(coordinator_host, coordinator_port)
        client.connect()
