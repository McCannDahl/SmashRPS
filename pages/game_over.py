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
        self.img_crown = pygame.image.load('crown.png')
        self.img_crown = pygame.transform.scale(self.img_crown, (20, 15))

    def handle_keydown(self, key):
        key_string = pygame.key.name(key)
        if key_string == 'up':
            self.action({
                'title': 'jump'
            })

    def handle_mouse_event(self, position):
        x, y = position
        if x >= self.button_x and x <= self.button_x + self.button_w and y >= self.button_y and y <= self.button_y + self.button_h:
            self.action({'title': 'lobby'})

    def render(self):
        y = 50

        textsurface = self.title_font.render('Game Over', False, (0, 0, 0))
        self.screen.blit(textsurface, (self.screen_w/2 - 150, y))
        y += 50
        
        for p in self.players:
            pygame.draw.rect(
                self.screen, 
                (p['color'][0], p['color'][1], p['color'][2]),
                (self.screen_w/2 - 60 - p['w'], y + p['y'] + p['h'], p['w'], p['h'])
            )

            if 'winning' in p:
                if p['winning']:
                    self.screen.blit(self.img_crown, (self.screen_w/2 - 60 - p['w'], y + p['y'] + p['h'] - 15))
            
            textsurface = self.name_font.render(p['name'], False, (0, 0, 0))
            self.screen.blit(textsurface, (self.screen_w/2 - 50, y))
            y += 20
            textsurface = self.name_font.render('Kills: '+str(p['kills']), False, (0, 80, 0))
            self.screen.blit(textsurface, (self.screen_w/2 - 50 + 20, y))
            y += 20
            textsurface = self.name_font.render('Deaths: '+str(p['deaths']), False, (80, 0, 0))
            self.screen.blit(textsurface, (self.screen_w/2 - 50 + 20, y))
            y += 20
        
        y += 50
        
        self.button_x = self.screen_w/2 - 105
        self.button_y = y
        pygame.draw.rect(self.screen, (60, 120, 120), (self.button_x, self.button_y, self.button_w, self.button_h), 2)
        y += 5

        textsurface = self.title_font.render('Lobby', False, (60, 180, 180))
        self.screen.blit(textsurface, (self.screen_w/2 - 95, y + 5))
