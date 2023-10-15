import asyncio
import utils
import rsa

'''
For sending public key to other clients
e2ek|||CLIENT_ID|||PUBLIC_KEY_ENCODED

For sending message to other clients, encrypted with their public key
e2em|||CLIENT_ID|||MESSAGE
'''

clients = {} # {client_id: {writer, client_name, room_name}}
chat_rooms = {} # {room_id: {room_name, password}}
usernames = []


async def multicast(client_id, room_id, message, new_client=False):
    for cid, values in clients.items():
        if cid != client_id and values["room_id"] == room_id:
            if new_client:
                await send_message(values["writer"], f"{message}\n")
            else:
                await send_message(values["writer"], f"{clients[client_id]['client_name']} > {message}\n")

async def send_message(writer, message):
    writer.write(message.encode())
    await writer.drain()

async def receive_message(reader):
    data = await reader.read(2048)
    return data.decode().strip() 

async def handle_client(reader, writer):
    client_id = utils.generate_user_id()
    client_public_key = await receive_message(reader)

    # get name
    await send_message(writer, f"Welcome to the chat server, {client_id}!\nWhat is your name?\n")
    client_name = await receive_message(reader)

    # check if username is already in use
    while client_name in usernames:
        await send_message(writer, f"Username {client_name} is already in use. Please choose another username.\n")
        client_name = await receive_message(reader)

    usernames.append(client_name)  # add the new username to the list of usernames

    # get room name
    room_names = [room['name'] for room in chat_rooms.values()]
    await send_message(writer, f"Welcome to the chat server, client {client_name}!\nSelect or Create The Chat.\nAvailable Chat Rooms: {room_names}\n")
    room_name = await receive_message(reader)

    if room_name in room_names:
        for key, value in chat_rooms.items():
            if value['name'] == room_name:
                room_id = key
                while True:  # keep asking for password until correct one is entered
                    await send_message(writer, f"Enter password for room {room_name}\n")
                    entered_password = await receive_message(reader)    
                    if entered_password == value['password']:
                        break  # correct password entered, break the loop
                    else:
                        await send_message(writer, f"Incorrect password for room {room_name}. Please try again.\n")


    else: 
        await send_message(writer, f"Enter password for new room {room_name}\n")
        hashed_password = await receive_message(reader)
        room_id = utils.generate_room_id()
        chat_rooms[room_id] = {"name": room_name, "password": hashed_password}


    # add client to clients array
    clients[client_id] = {"writer": writer, "room_id": room_id, "client_name": client_name, "public_key": client_public_key}
    await multicast(client_id, room_id, f"Client {client_name} has joined the chat.", new_client=True)

    # exchange keys
    await multicast(client_id, room_id, f"e2ek|||{client_id}|||{client_public_key}", new_client=True)
    for cid, values in clients.items():
        if cid != client_id and values["room_id"] == room_id:
            await send_message(writer, f"e2ek|||{cid}|||{values['public_key']}")

    try:
        while True:
            message = await receive_message(reader)
            if "e2em|||" in message:
                _, client_id, encrypted_message = message.split("|||")
                await send_message(clients[client_id]["writer"], f"{client_name}: {message}")
            

    except asyncio.CancelledError:
        pass
    finally:
        del clients[client_id]
        usernames.remove(client_name)  # remove the username from the list of usernames
        writer.close()

async def main():
    server = await asyncio.start_server(
        handle_client, 'localhost', 8888
    )
    print("Server listening...")
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())



