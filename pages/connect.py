from pages.page import Page
import pygame

class Connect(Page):
    def __init__(self, s, a):
        super().__init__(s)
        self.action = a
        self.title_font = pygame.font.SysFont('arial', 30)
        self.ipadress_font = pygame.font.SysFont('arial', 20)
        self.ipaddress = ''
        self.button_x = 50
        self.button_y = 150
        self.button_width = 80
        self.button_height = 50

    def handle_keydown(self, key):
        key_string = pygame.key.name(key)
        if key_string == '.' or key_string == '1' or key_string == '2' or key_string == '3' or key_string == '4' or key_string == '5' or key_string == '6' or key_string == '7' or key_string == '8' or key_string == '9' or key_string == '0':
            self.ipaddress += key_string
        if key_string == 'backspace':
            self.ipaddress = self.ipaddress[:-1]
        print(self.ipaddress)

    def handle_mouse_event(self, position):
        x, y = position
        if x >= self.button_x and x <= self.button_x + self.button_width and y >= self.button_y and y <= self.button_y + self.button_height:
            self.action({'title': 'join', 'ip': self.ipaddress})

    def render(self):
        textsurface = self.title_font.render('Enter the server IP address', False, (0, 0, 0))
        self.screen.blit(textsurface, (50, 50))

        textsurface = self.ipadress_font.render(self.ipaddress, False, (0, 0, 0))
        self.screen.blit(textsurface, (50, 100))

        pygame.draw.rect(self.screen, (100, 100, 180), (self.button_x, self.button_y, self.button_width, self.button_height), 2)
        textsurface = self.title_font.render('Join', False, (100, 100, 180))
        self.screen.blit(textsurface, (60, 160))
