from threading import Thread
import sys
import pygame
from pages.page import Page
from pages.connect import Connect
from pages.lobby import Lobby
from pages.error import Error
from pages.game import Game
from pages.game_over import GameOver
from helpers.socket import Socket
import json
from helpers.constants import *


class Display:
    pages = []
    current_page = None

    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((640, 480), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        # add pages
        self.pages.append(Connect(self.screen, self.action))
        self.pages.append(Lobby(self.screen, self.action))
        self.pages.append(Error(self.screen, self.action))
        self.pages.append(Game(self.screen, self.action))
        self.pages.append(GameOver(self.screen, self.action))
        self.current_page: Page = self.pages[0]
        self.screen_size = pygame.display.get_surface().get_size()
        self.set_all_pages_screen_sizes()

        self.socket = Socket(self.got_data, self.disconnected)

    def set_all_pages_screen_sizes(self):
        for p in self.pages:
            p.set_screen_size(self.screen_size)

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
                
            if event.type == pygame.VIDEORESIZE:
                self.screen_size = event.size
                self.set_all_pages_screen_sizes()
                self.screen = pygame.display.set_mode(self.screen_size, pygame.RESIZABLE)

            if event.type == pygame.KEYDOWN:
                if self.current_page != None:
                    self.current_page.handle_keydown(event.key)

            if event.type == pygame.KEYUP:
                if self.current_page != None:
                    self.current_page.handle_keyup(event.key)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                position = event.pos
                if self.current_page != None:
                    self.current_page.handle_mouse_event(position)

    def render(self):
        self.screen.fill((255, 255, 255))
        if self.current_page != None:
            self.current_page.render()
        pygame.display.flip()

    def action(self, data):
        if data['title'] == 'join':
            print(data['data'])
            Thread(target=self.join, args=[data['data']], kwargs=None, daemon=True).start()
        elif data['title'] == 'home':
            self.current_page = self.pages[0] # home
            self.current_page.restart()
            self.socket.restart()
        else:
            self.socket.send_data(data)

    def disconnected(self):
        self.current_page = self.pages[0] # home
        self.current_page.restart()
        self.socket.restart()
    
    def got_data(self, data):
        if data['title'] == 'update state':
            self.current_page.update_state(data['data'])
        elif data['title'] == 'start game':
            data = data['data']
            map = maps[data['map index']]
            self.current_page = self.pages[3] # game
            self.current_page.set_map(map)

    def join(self, ip):
        self.socket.connect(ip)
        if self.socket.isconnected:
            self.current_page = self.pages[1] # lobby
            self.socket.start_listening()
        else:
            self.current_page = self.pages[2] # error

if __name__ == '__main__':
    display = Display()
    display.start()