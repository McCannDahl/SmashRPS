from pages.page import Page
import pygame

class Game(Page):
    def __init__(self, s, a):
        super().__init__(s)
        self.action = a
        self.name_font = pygame.font.SysFont('arial', 10)

    def handle_keydown(self, key):
        key_string = pygame.key.name(key)
        if key_string == 'up':
            self.action({
                'title': 'jump'
            })

    def render(self):
        self.render_map()
        for p in self.state:
            self.render_person(p)
        
    def render_map(self):
        pass

    def render_person(self, p):
        pass