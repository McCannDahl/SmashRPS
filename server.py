import time
from threading import Thread
import json
import socket
from helpers.player import Player
from helpers.socket import Socket
from helpers.rec import Rec
from helpers.constants import *
import random

serversocket = socket.socket()
host = ''
port = 54545
players = []  # array of player colors, postions, attacks, health
playing = False
map_index = 0
game_time = 0
state = 0 # 0 = lobby, 1 = game, 2 = game over

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
    global playing, state
    setup_game()
    state = 1
    for p in players:
        respawn(p)
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
    global game_time
    new_time = time.time()
    while True:
        old_time = time.time()
        t = old_time - new_time
        new_time = old_time
        update_state(t)
        time.sleep(sleep_amount)
        if playing:
            game_time += t
            if game_time > final_game_time:
                end_game()

def end_game():
    state = 2

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
    # go through players and update all states
    for p in players:
        check_for_dealths(p)

def check_for_dealths(p):
    map = maps[map_index]
    death_left = map['w']/2 - map['w']*death/2
    death_right = map['w']/2 + map['w']*death/2
    death_up = map['h']/2 - map['h']*death/2
    death_down = map['h']/2 + map['h']*death/2
    if (
        p.x < death_left or
        p.y < death_up or
        p.x + p.w > death_right or
        p.y + p.h > death_down
    ):
        p.die()
        respawn(p)

def respawn(p):
    p.y = 0
    p.x = random.randint(0, maps[map_index]['w'])
    p.health = 1
    p.last_hit_by = None
    p.velX = 0
    p.velY = 0

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
            attack(p, q, 'up')

    elif p.velY > 0:
        if (
                (p.y + p.h < q.y + q.h and p.y + p.h > q.y) and
                (p.x + p.w > q.x and p.x < q.x + q.w)
        ):
            p.y = q.y - p.h
            temp = p.velY
            p.velY = q.velY*rebound_amount
            q.velY = temp*rebound_amount
            attack(p, q, 'down')
            
    if p.velX < 0:
        if (
                (p.x < q.x + q.w and p.x > q.x) and
                (p.y + p.h > q.y and p.y < q.y + q.h)
        ):
            p.x = q.x + q.w
            temp = p.velX
            p.velX = q.velX*rebound_amount
            q.velX = temp*rebound_amount
            attack(p, q, 'left')

    elif p.velX > 0:
        if (
                (p.x + p.w < q.x + q.w and p.x + p.w > q.x) and
                (p.y + p.h > q.y and p.y < q.y + q.h)
        ):
            p.x = q.x - p.w
            temp = p.velX
            p.velX = q.velX*rebound_amount
            q.velX = temp*rebound_amount
            attack(p, q, 'right')

def attack(p: Player, q: Player, p_direction):
    if p.attack and q.attack:
        if p.attack != q.attack:
            if p.attack == 'r' and q.attack == 'p': # q wins
                hit(p, q, opposite(p_direction), True)
            elif p.attack == 'p' and q.attack == 's': # q wins
                hit(p, q, opposite(p_direction), True)
            elif p.attack == 's' and q.attack == 'r': # q wins
                hit(p, q, opposite(p_direction), True)
            elif p.attack == 's' and q.attack == 'p': # p wins
                hit(q, q, p_direction, True)
            elif p.attack == 'r' and q.attack == 's': # p wins
                hit(q, q, p_direction, True)
            elif p.attack == 'p' and q.attack == 'r': # p wins
                hit(q, q, p_direction, True)

    elif not p.attack and q.attack:
        hit(p, q, opposite(p_direction))
    elif p.attack and not q.attack:
        hit(q, q, p_direction)

def opposite(direction):
    if direction == 'down':
        return 'up'
    elif direction == 'up':
        return 'down'
    elif direction == 'left':
        return 'right'
    elif direction == 'right':
        return 'left'
    else:
        return None

def hit(p, q, direction, mega=False):
    if p.health > health_reduction:
        p.health -= health_reduction
    else:
        p.health = 0.01
    amount = hit_amount / p.health
    if mega:
        amount = amount * hit_multiplyer
    if direction == 'up':
        p.velY -= amount
    if direction == 'down':
        p.velY += amount
    if direction == 'left':
        p.velX -= amount
    if direction == 'right':
        p.velX += amount
    p.last_hit_by = q

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
        data = {
            'state': state,
            'players': simple_players,
            'time': game_time,
            'map index': map_index
        }
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

