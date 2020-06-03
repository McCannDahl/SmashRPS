from pages.page import Page
import pygame
from helpers.constants import *

class Game(Page):
    def __init__(self, s, a):
        super().__init__(s)
        self.action = a
        self.name_font = pygame.font.SysFont('arial', 10)
        self.map = None
        self.ax = 0
        self.ay = 0
    
        self.img_s = pygame.image.load('images/s.png')
        self.img_s = pygame.transform.scale(self.img_s, (20, 20))
        self.img_r = pygame.image.load('images/r.png')
        self.img_r = pygame.transform.scale(self.img_r, (20, 20))
        self.img_p = pygame.image.load('images/p.png')
        self.img_p = pygame.transform.scale(self.img_p, (20, 20))

    def handle_keydown(self, key):
        key_string = pygame.key.name(key)
        if key_string == 'up':
            self.action({
                'title': 'jump'
            })
        elif key_string == 's':
            self.action({
                'title': 'attack',
                'data': 's'
            })
        elif key_string == 'd':
            self.action({
                'title': 'attack',
                'data': 'r'
            })
        elif key_string == 'f':
            self.action({
                'title': 'attack',
                'data': 'p'
            })
        elif key_string == 'left':
            self.action({
                'title': 'left down'
            })
        elif key_string == 'right':
            self.action({
                'title': 'right down'
            })

    def handle_keyup(self, key):
        key_string = pygame.key.name(key)
        if key_string == 'left':
            self.action({
                'title': 'left up'
            })
        elif key_string == 'right':
            self.action({
                'title': 'right up'
            })

    def render(self):
        self.render_map()
        for p in self.players:
            self.render_person(p)
        
    def render_map(self):
        if self.map:
            # borders
            self.ax = self.screen_w/2 - self.map['w']/2
            self.ay = self.screen_h/2 - self.map['h']/2
            #pygame.draw.rect(self.screen, (120, 120, 120), (self.ax, self.ay, self.map['w'], self.map['h']), 2)
            
            x = self.screen_w/2 - self.map['w']*death/2
            y = self.screen_h/2 - self.map['h']*death/2
            pygame.draw.rect(self.screen, (220, 220, 220), (x, y, self.map['w']*death, self.map['h']*death), 2)
            
            #walls
            for wall in self.map['walls']:
                x = wall.x + self.ax
                y = wall.y + self.ay
                pygame.draw.rect(self.screen, (120, 120, 120), (x, y, wall.w, wall.h))


    def render_person(self, p):
        x = p['x'] + self.ax
        y = p['y'] + self.ay
        pygame.draw.rect(self.screen, (p['color'][0], p['color'][1], p['color'][2]), (x, y, p['w'], p['h']))
        
        pygame.draw.rect(self.screen, (255, 0, 0), (x, y - 6, p['w']*(p['health']), 3))

        if p['attack'] == 's':
            self.screen.blit(self.img_s, (x, y))
        if p['attack'] == 'p':
            self.screen.blit(self.img_p, (x, y))
        if p['attack'] == 'r':
            self.screen.blit(self.img_r, (x, y))

        #textsurface = self.name_font.render(p['name'], False, (0, 0, 0))
        #self.screen.blit(textsurface, (x, y - 10))

    def set_map(self, map):
        self.map = map