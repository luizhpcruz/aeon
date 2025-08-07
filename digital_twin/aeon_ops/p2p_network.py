import socket
import threading

class P2PNode:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.peers = []

    def start(self):
        threading.Thread(target=self.listen_for_connections).start()

    def listen_for_connections(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)
            print(f"Node listening on {self.host}:{self.port}")

            while True:
                client_socket, address = server_socket.accept()
                print(f"Connection from {address}")
                threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        with client_socket:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                print(f"Received: {data.decode('utf-8')}")

    def connect_to_peer(self, peer_host, peer_port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as peer_socket:
            try:
                peer_socket.connect((peer_host, peer_port))
                self.peers.append((peer_host, peer_port))
                print(f"Connected to peer {peer_host}:{peer_port}")
            except ConnectionRefusedError:
                print(f"Failed to connect to peer {peer_host}:{peer_port}")

# Example usage
if __name__ == "__main__":
    node = P2PNode('127.0.0.1', 5000)
    node.start()

    # To connect to another peer, use:
    # node.connect_to_peer('127.0.0.1', 5001)
