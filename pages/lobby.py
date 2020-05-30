from pages.page import Page
import pygame

class Lobby(Page):
    def __init__(self, s, a):
        super().__init__(s)
        self.action = a
        self.title_font = pygame.font.SysFont('arial', 30)
        self.name_font = pygame.font.SysFont('arial', 20)
        self.name = ''
        self.button_x = 50
        self.button_y = 150
        self.button_width = 160
        self.button_height = 50

    def handle_keydown(self, key):
        key_string = pygame.key.name(key)
        if key_string == 'up':
            self.action({
                'title': 'jump'
            })
        else:
            if key_string == 'backspace':
                self.name = self.name[:-1]
            elif key_string == 'space':
                self.name += ' '
            else:
                self.name += key_string
            print(self.name)
            self.action({
                'title': 'update name',
                'data': self.name
            })

    def handle_mouse_event(self, position):
        x, y = position
        if x >= self.button_x and x <= self.button_x + self.button_width and y >= self.button_y and y <= self.button_y + self.button_height:
            self.action({'title': 'ready to start', 'name': self.name})

    def render(self):
        y = 50

        textsurface = self.title_font.render('Enter you\'re name', False, (0, 0, 0))
        self.screen.blit(textsurface, (self.screen_w/2 - 150, y))
        y += 60
        
        for p in self.state:
            pygame.draw.rect(
                self.screen, 
                (p['color'][0], p['color'][1], p['color'][2]), 
                (self.screen_w/2 - 60 - p['width'], y + p['y'], p['width'], p['height'])
            )
            
            textsurface = self.name_font.render(p['name'], False, (0, 0, 0))
            self.screen.blit(textsurface, (self.screen_w/2 - 50, y))
            y += 50

        self.button_x = self.screen_w/2 - 105
        self.button_y = y
        pygame.draw.rect(self.screen, (60, 120, 120), (self.button_x, self.button_y, self.button_width, self.button_height), 2)
        y += 5

        textsurface = self.title_font.render('Start Game', False, (60, 180, 180))
        self.screen.blit(textsurface, (self.screen_w/2 - 100, y + 5))
