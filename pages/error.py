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
        self.button_width = 100
        self.button_height = 50

    def handle_mouse_event(self, position):
        x, y = position
        if x >= self.button_x and x <= self.button_x + self.button_width and y >= self.button_y and y <= self.button_y + self.button_height:
            self.action({'title': 'home'})

    def render(self):
        textsurface = self.title_font.render('ERROR', False, (180, 0, 0))
        self.screen.blit(textsurface, (50, 50))

        pygame.draw.rect(self.screen, (100, 100, 180), (self.button_x, self.button_y, self.button_width, self.button_height), 2)
        textsurface = self.title_font.render('Home', False, (100, 100, 180))
        self.screen.blit(textsurface, (60, 160))
