import socket
import threading
import time
import json

SENDING_DELAY = 0.05
PORT = 9001

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

running = True

# total game state. must be a list, and cannot contain classes. only numbers, lists or dictionaries.
state = [100, 100, 200, 200, {}]

print(json.dumps(state))

# name: [socket, inputs]
clients = {}


# this is where the game logic for updating the state goes
def update_state_on_input():
    for name in clients.keys():
        client_inp = clients[name][1]
        if name not in state[4]:
            state[4][name] = [350, 350]
        if client_inp[0]:
            state[4][name][0] -= 5
        if client_inp[1]:
            state[4][name][0] += 5
        if client_inp[2]:
            state[4][name][1] -= 5
        if client_inp[3]:
            state[4][name][1] += 5
    keys = [key for key in state[4].keys()]
    for name in keys:
        if name not in clients:
            del state[4][name]


# the main game loop thread.
def gameloop():
    while running:
        time.sleep(SENDING_DELAY / 5)
        update_state_on_input()
        # print(clients.keys())


def send_state(name):
    try:
        while running:
            to_send = json.dumps(state)
            clients[name][0].send(to_send.encode())
            # print("sent", to_send)
            time.sleep(SENDING_DELAY)
    except:
        if name in clients:
            del clients[name]


def receive_input(name):
    try:
        while running:
            received = clients[name][0].recv(1024).decode()
            if received == "":
                continue
            # print("received", received)
            # print(clients)
            new_inp = json.loads(received)
            for i in range(len(new_inp)):
                if i < len(clients[name][1]):
                    clients[name][1][i] = new_inp[i]
                else:
                    clients[name][1].append(new_inp[i])
    except:
        if name in clients:
            del clients[name]


gameloop_thread = threading.Thread(target=gameloop, daemon=True)
gameloop_thread.start()

print(socket.gethostbyname(socket.gethostname()))

server_sock.bind(("0.0.0.0", PORT))
while running:
    print("listening...")
    server_sock.listen(5)
    (sock, address) = server_sock.accept()

    name = sock.recv(4096).decode()
    if name in clients:
        sock.close()
        continue
    # set this to the default input
    clients[name] = (sock, [0, 0, 0, 0])
    send_thread = threading.Thread(target=send_state, args=(name,), daemon=True)
    recv_thread = threading.Thread(target=receive_input, args=(name,), daemon=True)
    send_thread.start()
    recv_thread.start()
    print(clients.keys())
