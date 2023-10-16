# Chat Application with End-to-End Encryption

This is a simple chat application implemented in Python that provides end-to-end encryption (e2e) for secure communication between clients. The application uses the RSA encryption algorithm to secure messages exchanged between clients.

## Features

- **End-to-End Encryption:** Messages are encrypted before transmission and decrypted upon reception, ensuring secure communication.
- **Multi-User Chat:** Clients can join chat rooms, send messages, and interact with other users securely.
- **Password-Protected Rooms:** Chat rooms can be password-protected, adding an extra layer of security.
- **Dynamic Key Exchange:** Public keys are exchanged among clients for secure communication within the chat room.

## Getting Started

### Prerequisites

- Python 3.x

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Eljan404/Python_Chatroom_Asyncio_Endtoendencryption.git
   cd Python_Chatroom_Asyncio_Endtoendencryption

### Usage

1. Run the server:
   ```bash
   python server.py
   
2. Run multiple instances of the client:
   ```bash
   python client.py
   
Follow the on-screen prompts to enter your name, select/create a chat room, and start chatting securely.

### Configuration

- Modify server.py and client.py to customize server settings, encryption methods, and more.

### Acknowledgments

- Thanks to the creators of the RSA encryption algorithm.
- Inspiration for this project came from the need for a secure and private chat application.
