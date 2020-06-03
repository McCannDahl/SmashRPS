
from helpers.socket import Socket
from helpers.constants import *

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
    health = 1
    ready = False
    on_ground = False
    attack_time = 0
    attack_is_active = False

    def __init__(self, sock, player_num, action):
        self.sock = Socket(self.got_data, self.disconnected, sock)
        self.id = player_num
        self.name = 'Player '+str(self.id)
        if self.id < 8:
            self.color = colors[self.id]
        self.action = action
        self.left = False
        self.right = False
        self.on_ground = False
        self.last_hit_by = None
        self.kills = 0
        self.deaths = 0
        self.winning = False

    def disconnected(self):
        self.action({
            'title': 'disconnected',
            'data': self
        })

    def got_data(self, data):
        if data['title'] == 'update name':
            self.name = data['data']
        elif data['title'] == 'jump':
            self.jump()
        elif data['title'] == 'attack':
            self.set_attack(data['data'])
        elif data['title'] == 'left down':
            self.left = True
        elif data['title'] == 'right down':
            self.right = True
        elif data['title'] == 'left up':
            self.left = False
        elif data['title'] == 'right up':
            self.right = False
        elif data['title'] == 'change color':
            color_index = colors.index(self.color)
            color_index += 1
            if color_index >= len(colors):
                color_index = 0
            self.color = colors[color_index]
        elif data['title'] == 'ready to start':
            self.ready = True
            self.action({
                'title': 'check if everyone is ready'
            })

    def jump(self):
        # print('on ground = '+str(self.on_ground))
        # if not self.attack:
            # if self.on_ground:
        self.velY = jump_speed * -1

    def set_attack(self, attack):
        if not self.attack:
            self.attack = attack
            self.attack_time = 0
            self.attack_is_active = True

    def update(self, t):
        self.fall(t)
        self.move(t)
        self.update_positions(t)
        self.update_attack(t)
    
    def fall(self, t):
        self.velY += gravity * t

    def move(self, t):
        if self.velX > -1 * player_max_speed:
            if self.left:
                self.velX -= player_acc * t
        if self.velX < player_max_speed:
            if self.right:
                self.velX += player_acc * t

        if self.left == False and self.right == False:
            # if self.on_ground:
            if self.velX > 0:
                if self.velX > friction_de_acc * t:
                    self.velX -= friction_de_acc * t
                else:
                    self.velX = 0
            elif self.velX < 0:
                if self.velX < -1 * (friction_de_acc * t):
                    self.velX += friction_de_acc * t
                else:
                    self.velX = 0

        # if self.velX < player_max_speed * -1:
        #    self.velX = player_max_speed * -1
        # if self.velX > player_max_speed:
        #    self.velX = player_max_speed

    def update_positions(self, t):
        self.x += self.velX * t
        self.y += self.velY * t

    def update_attack(self,t):
        if self.attack:
            self.attack_time += t
            if self.attack_time >= attack_total_time:
                self.attack = None
                self.attack_is_active = None

    def get_data_to_send_to_client(self):
        return {
            'name': self.name,
            'color': self.color,
            'attack': self.attack,
            'x': self.x,
            'y': self.y,
            'w': self.w,
            'h': self.h,
            'ready': self.ready,
            'health': self.health,
            'deaths': self.deaths,
            'kills': self.kills,
            'winning': self.winning
        }
    
    def die(self):
        if self.last_hit_by:
            self.last_hit_by.kills += 1
        self.deaths += 1
