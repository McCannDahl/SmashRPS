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
        print('key up '+key_string)
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
        for p in self.state:
            self.render_person(p)
        
    def render_map(self):
        if self.map:
            # borders
            self.ax = self.screen_w/2 - self.map['w']/2
            self.ay = self.screen_h/2 - self.map['h']/2
            pygame.draw.rect(self.screen, (120, 120, 120), (self.ax, self.ay, self.map['w'], self.map['h']), 2)
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

    def set_map(self, map):
        self.map = map