import socket
import threading
import rsa
import sys
import hashlib

global fdata
public_key, private_key = rsa.newkeys(2048)
clients = {} # {client_id: public_key}
def hash_password(password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password.encode()

def receive_messages(client_socket):
    while True:
        data = client_socket.recv(2048)
        message = data.decode().strip()
        global fdata
        fdata=message
        if "e2em|||" in message:
            parts = message.split("|||")
            if len(parts) == 3:
                name, client_id, encrypted_message = parts
            decrypted_message = rsa.decrypt(eval(encrypted_message), private_key).decode()
            print(f"<# {name[:-4]}{decrypted_message}") # prints with e2e
        elif "e2ek|||" in message:
            parcalanmis = message.split("e2ek|||")
            for parca in parcalanmis[1:]:
                parts = parca.split("|||")
                client_id, public_key_encoded = parts
                clients[client_id] = rsa.PublicKey.load_pkcs1(public_key_encoded)
        else:
            print(f"<$ {message}") # prints without e2e

def send_messages(client_socket):
    
    while True:
        message = input("> ")
        if message.lower() == 'exit': break
        
        if len(clients) == 0:
            if 'password' in fdata:
                password=message
                client_socket.send(hash_password(password))
            else: 
                client_socket.send(message.encode())

        else: # we are in room with other clients 
            if 'password' in fdata:
                password=message
                client_socket.send(hash_password(password))
            else:
                for client_id, public_key in clients.items():
                    encrypted_message = rsa.encrypt(message.encode(), public_key)
                    client_socket.send(f"e2em|||{client_id}|||{encrypted_message}".encode())

def send_public_key(client_socket):
    client_socket.send(public_key.save_pkcs1())

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 8888)
    client_socket.connect(server_address)

    # Create separate threads for receiving and sending messages
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    send_thread = threading.Thread(target=send_messages, args=(client_socket,))

    # Send public key to server
    send_public_key(client_socket)

    # Start the threads
    receive_thread.start()
    send_thread.start()

    # Wait for both threads to finish
    receive_thread.join()
    send_thread.join()

    # Close the socket when done
    client_socket.close()

if __name__ == "__main__":
    main()
