from hints import a_star
import pygame
import random
import time
import tkinter as tk
from sprite import *
from settings import *
from tkinter import filedialog

def chosen_image():
        window = tk.Tk()
        window.withdraw()
        image_path = filedialog.askopenfilename(
                filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")]
        )
        window.destroy()
        return image_path


class Game: 
        def __init__(self):
                pygame.init()
                self.screen = pygame.display.set_mode ((WIDTH, HEIGHT))
                pygame.display.set_caption(tile)
                self.clock = pygame.time.Clock()

        def new(self):
                self.won = False
                image_path = chosen_image()
                if not image_path:
                        pygame.quit()
                        quit(0)
                raw_image = pygame.image.load(image_path)
                grid_size = GAME_SIZE * TILESIZE
                self.image = pygame.transform.scale(raw_image, (grid_size, grid_size))
                self.board = board(self.image)
                self.hint_tile = None
        
        def run(self):
                self.playing = True
                while self.playing:
                        self.clock.tick(FPS)
                        self.events()
                        self.update()
                        self.draw()
        
        def update(self):
                if self.board.is_solved():
                        self.won = True
                        self.playing = False
        
        def draw(self):
                self.screen.fill(BGCOLOUR)
                self.board.draw(self.screen)
                pygame.display.flip()
        
        def events(self):
                for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_h:
                                        curr_state = self.board.get_numbered_state()
                                        next_state = a_star(curr_state)
                                        self.hint_tile = self.get_tile_to_highlight(curr_state, next_state)

                        elif event.type == pygame.QUIT:
                                pygame.quit()
                                quit(0)
        
game = Game()
while True:
        game.new()
        game.run()