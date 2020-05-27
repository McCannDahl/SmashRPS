from pages.page import Page
import pygame
    
class Connect(Page):
    def __init__(self, s):
        super().__init__(s)
    def handle_keydown(self, key):
        if key == pygame.K_s:
            print('rock')
        elif key == pygame.K_d:
            print('papger')
        elif key == pygame.K_f:
            print('sizzors')
    def handle_mouse_event(self, position):
        print(position)
    def render(self):
        pass