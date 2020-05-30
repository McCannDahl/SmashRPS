import time
from threading import Thread
import json
import socket
from helpers.player import Player

serversocket = socket.socket()
host = 'localhost'
port = 54545
t1 = None
t2 = None
players = []  # array of player colors, postions, attacks, health

serversocket.bind(('', port))
print('listening ("conrol + c" to stop)')

serversocket.listen()

def listen_for_connections():
    while True:
        clientsocket, addr = serversocket.accept()
        print("got a connection from %s" % str(addr))
        player_id = len(players)+1
        players.append(Player(clientsocket, player_id))
        Thread(target=get_data, args=[player_id], kwargs=None, daemon=True).start()

def update():
    new_time = time.time()
    while True:
        old_time = time.time()
        t = old_time - new_time
        new_time = old_time
        update_state(t)
        time.sleep(0.01)

def update_state(t):
    pass

def get_data_to_send_to_client(p):
    return p.get_data_to_send_to_client()

def send_state():
    while True:
        simple_players = list(map(get_data_to_send_to_client, players))
        for p in players:
            try:
                message = {'title':'update state', 'data':simple_players} # for now lets just send the players instead of state
                messagestr = '<<<'+json.dumps(message)+'>>>'
                p.sock.send(messagestr.encode('ascii'))
            except Exception as err:
                print(err)
                print('removing client')
                players.remove(p)
        time.sleep(0.01)


def get_data(player_id):
    player = None
    for p in players:
        if p.id == player_id:
            player = p
    while p in players:
        try:
            teststr = player.sock.recv(1024).decode("utf-8")
            if teststr.endswith('>>>'): # last message is complete
                teststr = teststr.split("<<<")[-1]
            else: # last message is incomplete
                teststr = teststr.split("<<<")[-2]
            teststr = teststr.replace('>>>','')
            # print(teststr)
            test = json.loads(teststr)
            got_data(player, test)
        except Exception as err:
            print('There was a problem getting client data. Closing socket. '+str(err))
            player.sock.close()
            players.remove(player)

def got_data(player, data):
    if data['title'] == 'update name':
        player.name = data['data']

if __name__ == '__main__':
    t1 = Thread(target=listen_for_connections)
    t1.daemon = True
    t2 = Thread(target=update)
    t2.daemon = True
    t3 = Thread(target=send_state)
    t3.daemon = True
    t1.start()
    t2.start()
    t3.start()
    while True:
        time.sleep(10)