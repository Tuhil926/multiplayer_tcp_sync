import socket
import threading
import time
import json
import pygame

pygame.init()

SENDING_DELAY = 0.05
PORT = 9001

client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

running = True

# total game state
state = [100, 100, 200, 200]
inp = [0, 0, 0, 0]


def send_input():
    while running:
        to_send = json.dumps(inp)
        client_sock.send(to_send.encode())
        print("sent", to_send)
        time.sleep(SENDING_DELAY)


def receive_state():
    while running:
        received = client_sock.recv(1024).decode()
        if received == "":
            continue
        if "][" in received:
            received = received[: received.find("][") + 1]
        print("received", received)
        new_state = json.loads(received)
        while len(state) > len(new_state):
            state.pop()
        for i in range(len(new_state)):
            if i < len(state):
                state[i] = new_state[i]
            else:
                state.append(new_state[i])
        print(state)


username = ""


def login(name):
    global username
    try:
        print("Trying to connect...")
        # change the ip address to a public one if you host your server
        client_sock.connect(("127.0.0.1", PORT))
        client_sock.send(name.encode())
        send_thread = threading.Thread(target=send_input, daemon=True)
        recv_thread = threading.Thread(target=receive_state, daemon=True)
        send_thread.start()
        recv_thread.start()
        username = name
    except BrokenPipeError:
        print("try a different name bruh")
        return False
    return True


# you can call this login function somewhere inside the game loop as well, probably with a thread. please call only once tho
print("Enter your name")
login(input())

screen = pygame.display.set_mode((1000, 700))
# Game loop
while running:
    time.sleep(SENDING_DELAY)
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    inp[0] = int(keys[pygame.K_a])
    inp[1] = int(keys[pygame.K_d])
    inp[2] = int(keys[pygame.K_w])
    inp[3] = int(keys[pygame.K_s])
    if len(state) >= 5:
        # if username in state[4]:
        #     pygame.draw.circle(screen, (255, 255, 255), state[4][username], 20)
        for name in state[4]:
            pygame.draw.circle(screen, (255, 255, 255), state[4][name], 20)

    pygame.display.update()
