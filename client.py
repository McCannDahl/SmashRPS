from threading import Thread
import socket
import sys
import pygame
from pages.page import Page
from pages.connect import Connect


class Game:
    def __init__(self):
        self.socket = Socket()
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
        self.current_page: Page = self.pages[0]
    
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
            # todo change pages

class Socket:
    def __init__(self,host="localhost",port=54545):
        self.sock = socket.socket()
        try:
            self.sock.connect((host, port))
            print('Established connection')
            self.t1 = Thread(target=self.get_data)
            self.t1.daemon = True
            self.t1.start()
        except:
            print('server not active')

    def get_data(self):
        while True:
            try:
                print(self.sock.recv(1024).decode("utf-8"))
            except:
                self.sock.close()

if __name__ == '__main__':
    g = Game()