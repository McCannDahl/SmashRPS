import socket

class Player:
    sock = None
    velX = 0
    velY = 0
    id = None

    name = 'Player'
    color = [0, 0, 0]
    action = None # or 'r' or 'p' or 's'
    x = 0
    y = 0
    width = 10
    height = 10

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

    def __init__(self, sock, player_num):
        self.sock = sock
        self.id = player_num
        self.name = 'Player '+str(self.id)
        if self.id < 8:
            self.color = self.colors[self.id]


    def jump(self):
        pass

    def set_action(self):
        pass

    def update(self):
        self.fall()
        self.update_action()
    
    def fall(self):
        pass

    def update_action(self):
        pass

    def get_data_to_send_to_client(self):
        return {
            'name': self.name,
            'color': self.color,
            'action': self.action,
            'x': self.x,
            'y': self.y,
            'width': self.width,
            'height': self.height
        }
