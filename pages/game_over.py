from pages.page import Page
import pygame

class GameOver(Page):
    def __init__(self, s, a):
        super().__init__(s)
        self.action = a
        self.title_font = pygame.font.SysFont('arial', 30)
        self.name_font = pygame.font.SysFont('arial', 20)
        self.name = ''
        self.button_x = 0
        self.button_y = 0
        self.button_w = 170
        self.button_h = 50

        self.button2_x = 0
        self.button2_y = 0
        self.button2_w = 200
        self.button2_h = 60

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
        if x >= self.button_x and x <= self.button_x + self.button_w and y >= self.button_y and y <= self.button_y + self.button_h:
            self.action({'title': 'ready to start'})
            
        if x >= self.button2_x and x <= self.button2_x + self.button2_w and y >= self.button2_y and y <= self.button2_y + self.button2_h:
            self.action({'title': 'change color'})

    def render(self):
        y = 50

        textsurface = self.title_font.render('Game Over', False, (0, 0, 0))
        self.screen.blit(textsurface, (self.screen_w/2 - 120, y))
        y += 50
        
        for p in self.state:
            pygame.draw.rect(
                self.screen, 
                (p['color'][0], p['color'][1], p['color'][2]),
                (self.screen_w/2 - 60 - p['w'], y + p['y'] + p['h'], p['w'], p['h'])
            )
            
            textsurface = self.name_font.render(p['name'], False, (0, 0, 0))
            self.screen.blit(textsurface, (self.screen_w/2 - 50, y))
            y += 40
        
        y += 50

        self.button2_x = self.screen_w/2 - 120
        self.button2_y = y
        pygame.draw.rect(self.screen, (120, 60, 120), (self.button2_x, self.button2_y, self.button2_w, self.button2_h), 2)
        y += 5
        
        self.button_x = self.screen_w/2 - 105
        self.button_y = y
        pygame.draw.rect(self.screen, (60, 120, 120), (self.button_x, self.button_y, self.button_w, self.button_h), 2)
        y += 5

        if not p['ready']:
            textsurface = self.title_font.render('Play Again', False, (60, 180, 180))
            self.screen.blit(textsurface, (self.screen_w/2 - 100, y + 5))
