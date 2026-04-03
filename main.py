import pygame
import random
import time
from sprite import *
from settings import *

class Game: 
        def __init__(self):
                pygame.init()
                self.screen = pygame.display.set_mode ((width, height))
                pygame.display.set_caption(tile)
                self.clock = pygame.time.Clock()

        def new(self):
                pass
        
        def run(self):
                self.playing = True
                while self.playing:
                        self.clock.tick(FPS)
                        self.events()
                        self.draw()
                pass
        
        def update(self):
                pass
        
        def draw(self):
                pass
        
        def events(self):
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                pygame.quit()
                                quit(0)
        
game = Game()
while True:
        game.new()
        game.run()