from threading import Thread
import sys
import pygame
from pages.page import Page
from pages.connect import Connect
from pages.lobby import Lobby
from pages.error import Error
from helpers.socket import Socket


class Game:
    def __init__(self):
        self.display = Display()
        self.display.start()

class Display:
    pages = []
    current_page = None

    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((640, 480))
        self.clock = pygame.time.Clock()
        # add pages
        self.pages.append(Connect(self.screen, self.action))
        self.pages.append(Lobby(self.screen, self.action))
        self.pages.append(Error(self.screen, self.action))
        self.current_page: Page = self.pages[0]
        self.socket = Socket()
        self.ip = ''
    
    def start(self):
        print("start display")
        while True:
            self.handle_inputs()
            self.render()
            self.clock.tick(60)
    
    def handle_inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if self.current_page != None:
                    self.current_page.handle_keydown(event.key)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                position = event.pos
                if self.current_page != None:
                    self.current_page.handle_mouse_event(position)

    def render(self):
        self.screen.fill((255, 255, 255))
        if self.current_page != None:
            self.current_page.render()
        pygame.display.flip()

    def action(self,data):
        if data['title'] == 'join':
            print(data['ip'])
            self.ip = data['ip']
            t1 = Thread(target=self.join)
            t1.daemon = True
            t1.start()
        elif data['title'] == 'home':
            self.current_page = self.pages[0] # home
            self.current_page.restart()
    
    def join(self):
        self.socket.connect(self.ip)
        if self.socket.isconnected:
            self.current_page = self.pages[1] # lobby
            self.socket.start()
        else:
            self.current_page = self.pages[2] # error

if __name__ == '__main__':
    g = Game()