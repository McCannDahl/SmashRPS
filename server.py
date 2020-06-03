import time
from threading import Thread
import json
import socket
from helpers.player import Player
from helpers.socket import Socket
from helpers.rec import Rec
from helpers.constants import *

serversocket = socket.socket()
host = ''
port = 54545
players = []  # array of player colors, postions, attacks, health
playing = False
map_index = 0

serversocket.bind((host, port))
print('listening ("conrol + c" to stop)')
serversocket.listen()

def listen_for_connections():
    while True:
        clientsocket, addr = serversocket.accept()
        print("got a connection from %s" % str(addr))
        player_id = len(players)+1
        players.append(Player(clientsocket, player_id, action))

def action(data):
    if data['title'] == 'disconnected':
        disconnected(data['data'])
    if data['title'] == 'check if everyone is ready':
        everyone_is_ready = True
        for p in players:
            if not p.ready:
                everyone_is_ready = False
        if everyone_is_ready:
            start_game()

def start_game():
    global playing
    setup_game()
    send_message({
        'title': 'start game',
        'data': {
            'map index': map_index
        }
    })
    playing = True

def setup_game():
    setup_map()
    setup_players_positions()

def setup_map():
    global map_index
    map_index = 1

def setup_players_positions():
    pass

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
        time.sleep(sleep_amount)

def update_state(t):
    # go through players and update all states
    for p in players:
        p.update(t)
    # handle player collisions
    if playing:
        for p in players:
            for q in players:
                if p != q:
                    handle_player_collision(p, q)
    # handle wall collisions
    for p in players:
        p.on_ground = False
    for wall in maps[map_index]['walls']:
        for p in players:
            handle_wall_collision(wall, p)

def handle_player_collision(p, q):
    if p.velY < 0:
        if (
                (p.y < q.y + q.h and p.y > q.y) and
                (p.x + p.w > q.x and p.x < q.x + q.w)
        ):
            p.y = q.y + q.h
            temp = p.velY
            p.velY = q.velY*rebound_amount
            q.velY = temp*rebound_amount
    elif p.velY > 0:
        if (
                (p.y + p.h < q.y + q.h and p.y + p.h > q.y) and
                (p.x + p.w > q.x and p.x < q.x + q.w)
        ):
            p.y = q.y - p.h
            temp = p.velY
            p.velY = q.velY*rebound_amount
            q.velY = temp*rebound_amount
            
    if p.velX < 0:
        if (
                (p.x < q.x + q.w and p.x > q.x) and
                (p.y + p.h > q.y and p.y < q.y + q.h)
        ):
            p.x = q.x + q.w
            temp = p.velX
            p.velX = q.velX*rebound_amount
            q.velX = temp*rebound_amount
    elif p.velX > 0:
        if (
                (p.x + p.w < q.x + q.w and p.x + p.w > q.x) and
                (p.y + p.h > q.y and p.y < q.y + q.h)
        ):
            p.x = q.x - p.w
            temp = p.velX
            p.velX = q.velX*rebound_amount
            q.velX = temp*rebound_amount


def handle_wall_collision(wall, p):
    if p.velY < 0: # going up
        if (
            (
                (p.y < wall.y + wall.h and p.y > wall.y) or # assumming wall is taller than person
                (wall.y + wall.h < p.y + p.h and wall.y + wall.h > p.y)
            ) and
            (p.x + p.w > wall.x and p.x < wall.x + wall.w)
        ): # assuming person is taller than wall
            p.y = wall.y + wall.h
            p.velY = -p.velY * rebound_amount
    elif p.velY > 0: # going down
        if (
            (
                (p.y + p.h < wall.y + wall.h and p.y + p.h > wall.y) or # assumming wall is taller than person
                (wall.y < p.y + p.h and wall.y > p.y)
            ) and
            (p.x + p.w > wall.x and p.x < wall.x + wall.w)
        ): # assuming person is taller than wall
            p.y = wall.y - p.h
            if p.velY < on_ground_threshold:
                p.velY = 0
                p.on_ground = True
            else:
                p.velY = -p.velY * rebound_amount
    if p.velX < 0: # going left
        if (
            (
                (p.x < wall.x + wall.w and p.x > wall.x) or # assumming wall is taller than person
                (wall.x + wall.w < p.x + p.w and wall.x + wall.w > p.x)
            ) and
            (p.y + p.h > wall.y and p.y < wall.y + wall.h)
        ): # assuming person is taller than wall
            p.x = wall.x + wall.w
            p.velX = -p.velX * rebound_amount
    elif p.velX > 0: # going right
        if (
            (
                (p.x + p.w < wall.x + wall.w and p.x + p.w > wall.x) or # assumming wall is taller than person
                (wall.x < p.x + p.w and wall.x > p.x)
            ) and
            (p.y + p.h > wall.y and p.y < wall.y + wall.h)
        ): # assuming person is taller than wall
            p.x = wall.x - p.w
            p.velX = -p.velX * rebound_amount

def get_data_to_send_to_client(p):
    return p.get_data_to_send_to_client()

def send_state():
    while True:
        simple_players = list(map(get_data_to_send_to_client, players))
        message = {'title':'update state', 'data':simple_players} # for now lets just send the players instead of state
        send_message(message)
        time.sleep(sleep_amount)

def send_message(message):
    for p in players:
        try:
            p.sock.send(message)
        except Exception as err:
            print(err)
            print('removing client')
            disconnected(p)

if __name__ == '__main__':
    Thread(target=listen_for_connections, args=[], kwargs=None, daemon=True).start()
    Thread(target=update, args=[], kwargs=None, daemon=True).start()
    Thread(target=send_state, args=[], kwargs=None, daemon=True).start()
    while True:
        time.sleep(10)

