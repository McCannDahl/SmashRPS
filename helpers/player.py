
from helpers.socket import Socket

class Player:
    sock = None
    velX = 0
    velY = 0
    id = None

    name = 'Player'
    color = [0, 0, 0]
    attack = None # or 'r' or 'p' or 's'
    x = 0
    y = 0
    w = 20
    h = 20
    health = 100

    # todo put this somewhere else
    colors = [
        [0,0,0],
        [255,0,0],
        [255,127,0],
        [255,255,0],
        [0,255,0],
        [0,0,255],
        [75,0,130],
        [148,0,211]
    ]

    def __init__(self, sock, player_num, server_disconnected):
        self.sock = Socket(self.got_data, self.disconnected, sock)
        self.id = player_num
        self.name = 'Player '+str(self.id)
        if self.id < 8:
            self.color = self.colors[self.id]
        self.server_disconnected = server_disconnected

    def disconnected(self):
        self.server_disconnected(self)

    def got_data(self, data):
        if data['title'] == 'update name':
            self.name = data['data']
        if data['title'] == 'jump':
            self.jump()

    def jump(self):
        self.velY = -10

    def set_attack(self):
        pass

    def update(self, t):
        self.fall(t)
        self.update_positions(t)
        self.update_attack(t)
    
    def fall(self, t):
        self.velY += 9.81 * t
    
    def update_positions(self, t):
        self.x += self.velX * t
        self.y += self.velY * t

    def update_attack(self,t):
        pass

    def get_data_to_send_to_client(self):
        return {
            'name': self.name,
            'color': self.color,
            'attack': self.attack,
            'x': self.x,
            'y': self.y,
            'width': self.w,
            'height': self.h
        }
