from pages.page import Page
import pygame

class Error(Page):
    def __init__(self, s, a):
        super().__init__(s)
        self.action = a
        self.title_font = pygame.font.SysFont('arial', 30)
        self.ipadress_font = pygame.font.SysFont('arial', 20)
        self.button_x = 50
        self.button_y = 150
        self.button_w = 100
        self.button_h = 50

    def handle_mouse_event(self, position):
        x, y = position
        if x >= self.button_x and x <= self.button_x + self.button_w and y >= self.button_y and y <= self.button_y + self.button_h:
            self.action({'title': 'home'})

    def render(self):
        textsurface = self.title_font.render('ERROR', False, (180, 0, 0))
        self.screen.blit(textsurface, (self.screen_w/2 - 50, 50))

        self.button_x = self.screen_w/2 - 45
        pygame.draw.rect(self.screen, (100, 100, 180), (self.button_x, self.button_y, self.button_w, self.button_h), 2)
        
        textsurface = self.title_font.render('Home', False, (100, 100, 180))
        self.screen.blit(textsurface, (self.screen_w/2 - 35, 160))
