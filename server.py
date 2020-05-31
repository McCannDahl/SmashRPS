import time
from threading import Thread
import json
import socket
from helpers.player import Player
from helpers.socket import Socket
from helpers.rec import Rec

serversocket = socket.socket()
host = ''
port = 54545
players = []  # array of player colors, postions, attacks, health
walls = [
    Rec(0, 0, 100, 100)
]

serversocket.bind((host, port))
print('listening ("conrol + c" to stop)')
serversocket.listen()

def listen_for_connections():
    while True:
        clientsocket, addr = serversocket.accept()
        print("got a connection from %s" % str(addr))
        player_id = len(players)+1
        players.append(Player(clientsocket, player_id, disconnected))

def disconnected(player):
    if player in players:
        print('Removing player '+str(player.name))
        players.remove(player)

def update():
    new_time = time.time()
    while True:
        old_time = time.time()
        t = old_time - new_time
        new_time = old_time
        update_state(t)
        time.sleep(0.01)

def update_state(t):
    # go through players and update all states
    for p in players:
        p.update(t)
    # handle player collisions
    for p in players:
        for q in players:
            if p != q:
                handle_player_collision(p, q)
    # handle wall collisions
    for wall in walls:
        for p in players:
            handle_wall_collision(wall, p)

def handle_player_collision(p, q): # only account for p. Move 1/2 the amount.
    if p.velY < 0:
        pass
    elif p.velY > 0:
        pass
    if p.velX < 0:
        pass
    elif p.velX > 0:
        pass

def handle_wall_collision(wall, p):
    if p.velY < 0: # going up
        if (
            (p.y <= wall.y + wall.h and p.y >= wall.y) or # assumming wall is taller than person
            (wall.y + wall.h <= p.y + p.h and wall.y + wall.h >= p.y)
        ): # assuming person is taller than wall
            p.y = wall.y + wall.h
            p.velY = 0
    elif p.velY > 0: # going down
        if (
            (p.y + p.h <= wall.y + wall.h and p.y + p.h >= wall.y) or # assumming wall is taller than person
            (wall.y <= p.y + p.h and wall.y >= p.y)
        ): # assuming person is taller than wall
            p.y = wall.y - p.h
            p.velY = 0
    if p.velX < 0: # going left
        if (
            (p.x <= wall.x + wall.w and p.x >= wall.x) or # assumming wall is taller than person
            (wall.x + wall.w <= p.x + p.w and wall.x + wall.w >= p.x)
        ): # assuming person is taller than wall
            p.x = wall.x + wall.w
            p.velX = 0
    elif p.velX > 0: # going right
        if (
            (p.x + p.w <= wall.x + wall.w and p.x + p.w >= wall.x) or # assumming wall is taller than person
            (wall.x <= p.x + p.w and wall.x >= p.x)
        ): # assuming person is taller than wall
            p.x = wall.x - p.w
            p.velX = 0

def get_data_to_send_to_client(p):
    return p.get_data_to_send_to_client()

def send_state():
    while True:
        simple_players = list(map(get_data_to_send_to_client, players))
        for p in players:
            try:
                message = {'title':'update state', 'data':simple_players} # for now lets just send the players instead of state
                p.sock.send(message)
            except Exception as err:
                print(err)
                print('removing client')
                disconnected(p)
        time.sleep(0.01)

if __name__ == '__main__':
    Thread(target=listen_for_connections, args=[], kwargs=None, daemon=True).start()
    Thread(target=update, args=[], kwargs=None, daemon=True).start()
    Thread(target=send_state, args=[], kwargs=None, daemon=True).start()
    while True:
        time.sleep(10)

