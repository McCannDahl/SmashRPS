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
    global playing, state, game_time
    setup_game()
    state = 1
    for p in players:
        p.kills = 0
        p.deaths = 0
        p.winning = None
        respawn(p)
    playing = True
    game_time = final_game_time

def setup_game():
    setup_map()
    setup_players_positions()

def setup_map():
    global map_index
    map_index = 1

def setup_players_positions():
    pass

def disconnected(player):
    global state, game_time, map_index, playing
    if player in players:
        print('Removing player '+str(player.name))
        players.remove(player)
    if len(players) == 0:
        state = 0
        game_time = 0
        map_index = 0
        playing = False

def update():
    new_time = time.time()
    while True:
        old_time = time.time()
        t = old_time - new_time
        new_time = old_time
        update_state(t)
        time.sleep(sleep_amount)

def end_game():
    global state, map_index, playing
    state = 2
    map_index = 0
    playing = False
    for p in players:
        p.ready = False
        p.x = 0
        p.y = 0
        p.velX = 0
        p.velY = 0
        p.last_hit_by = None
        p.left = False
        p.right = False

def update_state(t):
    global game_time
    # go through players and update all states
    for p in players:
        p.update(t)
    # handle wall collisions
    for p in players:
        p.on_ground = False
    for wall in maps[map_index]['walls']:
        for p in players:
            handle_wall_collision(wall, p)
    # handle player collisions
    if playing:
        for p in players:
            for q in players:
                if p != q:
                    handle_player_collision(p, q)
    # die
    for p in players:
        check_for_dealths(p)

    
    if playing:
        game_time -= t
        if game_time <= 0:
            game_time = 0
            end_game()

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
        max_score = -999
        people_winning = []
        for m in players:
            m.winning = False
            score = m.kills - m.deaths
            if score == max_score:
                people_winning.append(m)
            if score > max_score:
                people_winning = [m]
                max_score = score
        if len(people_winning) != len(players):
            for n in people_winning:
                n.winning = True

def respawn(p):
    p.y = 0
    p.x = random.randint(0, maps[map_index]['w'])
    p.health = 1
    p.last_hit_by = None
    p.velX = 0
    p.velY = 0

def handle_player_collision(p, q):
    has_collided = False
    if p.velY < 0:
        if (
                (p.y < q.y + q.h and p.y > q.y) and
                (p.x + p.w > q.x and p.x < q.x + q.w)
        ):
            p.y = q.y + q.h
            temp = p.velY
            p.velY = q.velY*rebound_amount
            q.velY = temp*rebound_amount
            if not has_collided:
                attack(p, q, 'up')
            has_collided = True

    elif p.velY > 0:
        if (
                (p.y + p.h < q.y + q.h and p.y + p.h > q.y) and
                (p.x + p.w > q.x and p.x < q.x + q.w)
        ):
            p.y = q.y - p.h
            temp = p.velY
            p.velY = q.velY*rebound_amount
            q.velY = temp*rebound_amount
            if not has_collided:
                attack(p, q, 'down')
            has_collided = True

    if p.velX < 0:
        if (
                (p.x < q.x + q.w and p.x > q.x) and
                (p.y + p.h > q.y and p.y < q.y + q.h)
        ):
            p.x = q.x + q.w
            temp = p.velX
            p.velX = q.velX*rebound_amount
            q.velX = temp*rebound_amount
            if not has_collided:
                attack(p, q, 'left')
            has_collided = True

    elif p.velX > 0:
        if (
                (p.x + p.w < q.x + q.w and p.x + p.w > q.x) and
                (p.y + p.h > q.y and p.y < q.y + q.h)
        ):
            p.x = q.x - p.w
            temp = p.velX
            p.velX = q.velX*rebound_amount
            q.velX = temp*rebound_amount
            if not has_collided:
                attack(p, q, 'right')
            has_collided = True

def attack(p: Player, q: Player, p_direction):
    if p.attack_is_active and q.attack_is_active:
        if p.attack != q.attack:
            if p.attack == 'r' and q.attack == 'p': # q wins
                hit(p, q, opposite(p_direction), True)
            elif p.attack == 'p' and q.attack == 's': # q wins
                hit(p, q, opposite(p_direction), True)
            elif p.attack == 's' and q.attack == 'r': # q wins
                hit(p, q, opposite(p_direction), True)
            elif p.attack == 's' and q.attack == 'p': # p wins
                hit(q, p, p_direction, True)
            elif p.attack == 'r' and q.attack == 's': # p wins
                hit(q, p, p_direction, True)
            elif p.attack == 'p' and q.attack == 'r': # p wins
                hit(q, p, p_direction, True)

    elif not p.attack_is_active and q.attack_is_active:
        hit(p, q, opposite(p_direction))
    elif p.attack_is_active and not q.attack_is_active:
        hit(q, p, p_direction)

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
        p.velX += amount * (random.randint(0, 1) * 2 - 1) # -1 or 1
        p.velY -= amount * .3
    if direction == 'down':
        p.velX += amount * (random.randint(0, 1) * 2 - 1) # -1 or 1
        p.velY += amount * .3
    if direction == 'left':
        p.velX -= amount
        p.velY -= amount * .3
    if direction == 'right':
        p.velX += amount
        p.velY -= amount * .3
    p.last_hit_by = q
    p.attack_is_active = False
    q.attack_is_active = False

def handle_wall_collision(wall, p):
    has_collided = False
    if p.velY > 0: # going down
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
            has_collided = True
    if p.velY < 0 and not has_collided: # going up
        if (
            (
                (p.y < wall.y + wall.h and p.y > wall.y) or # assumming wall is taller than person
                (wall.y + wall.h < p.y + p.h and wall.y + wall.h > p.y)
            ) and
            (p.x + p.w > wall.x and p.x < wall.x + wall.w)
        ): # assuming person is taller than wall
            p.y = wall.y + wall.h
            p.velY = -p.velY * rebound_amount
            has_collided = True
    if p.velX < 0 and not has_collided: # going left
        if (
            (
                (p.x < wall.x + wall.w and p.x > wall.x) or # assumming wall is taller than person
                (wall.x + wall.w < p.x + p.w and wall.x + wall.w > p.x)
            ) and
            (p.y + p.h > wall.y and p.y < wall.y + wall.h)
        ): # assuming person is taller than wall
            p.x = wall.x + wall.w
            p.velX = -p.velX * rebound_amount
            has_collided = True
    if p.velX > 0 and not has_collided: # going right
        if (
            (
                (p.x + p.w < wall.x + wall.w and p.x + p.w > wall.x) or # assumming wall is taller than person
                (wall.x < p.x + p.w and wall.x > p.x)
            ) and
            (p.y + p.h > wall.y and p.y < wall.y + wall.h)
        ): # assuming person is taller than wall
            p.x = wall.x - p.w
            p.velX = -p.velX * rebound_amount
            has_collided = True

def get_data_to_send_to_client(p):
    return p.get_data_to_send_to_client()

def send_state():
    while True:
        simple_players = list(map(get_data_to_send_to_client, players))
        data = {
            'state': state,
            'players': simple_players,
            'time': int(round(game_time)),
            'map index': map_index
        }
        message = {'title':'update state', 'data':data} # for now lets just send the players instead of state
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

