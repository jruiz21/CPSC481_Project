# sprites
import pygame
import random
from settings import *

class Tile:
    def __init__(self, image, correct_pos, current_pos):
        self.image = image
        self.correct_pos = correct_pos
        self.current_pos = list(current_pos)

    def draw(self, surface):
        x = self.current_pos[0] * TILESIZE
        y = self.current_pos[1] * TILESIZE
        surface.blit(self.image, (x, y))
        pygame.draw.rect(surface, BLACK, (x, y, TILESIZE, TILESIZE), 2)

    def is_correct(self):
        return list(self.current_pos) == list(self.correct_pos)


class Board:
    def __init__(self, image):
        self.tiles = []
        self.blank_pos = [GAME_SIZE - 1, GAME_SIZE - 1]
        self.moves = 0
        self.create_tiles(image)
        self.shuffle()

    def create_tiles(self, image):
        for row in range(GAME_SIZE):
            for col in range(GAME_SIZE):
                if row == GAME_SIZE - 1 and col == GAME_SIZE - 1:
                    continue
                rect = pygame.Rect(col * TILESIZE, row * TILESIZE, TILESIZE, TILESIZE)
                tile_image = image.subsurface(rect).copy()
                tile = Tile(tile_image, (col, row), (col, row))
                self.tiles.append(tile)

    def shuffle(self):
        for _ in range(1000):
            neighbors = self.get_neighbors()
            choice = random.choice(neighbors)
            self.slide(choice)
        self.moves = 0

    def get_neighbors(self):
        neighbors = []
        bx, by = self.blank_pos
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = bx + dx, by + dy
            if 0 <= nx < GAME_SIZE and 0 <= ny < GAME_SIZE:
                neighbors.append([nx, ny])
        return neighbors

    def slide(self, pos):
        tile = self.get_tile_at(pos)
        if tile:
            tile.current_pos = list(self.blank_pos)
            self.blank_pos = list(pos)

    def handle_click(self, mouse_pos):
        col = mouse_pos[0] // TILESIZE
        row = mouse_pos[1] // TILESIZE
        clicked = [col, row]
        if clicked in self.get_neighbors():
            self.slide(clicked)
            self.moves += 1

    def get_tile_at(self, pos):
        for tile in self.tiles:
            if list(tile.current_pos) == list(pos):
                return tile
        return None

    def draw(self, surface):
        for tile in self.tiles:
            tile.draw(surface)

    def is_solved(self):
        return all(tile.is_correct() for tile in self.tiles)
    
    def get_state(self):
        state = [[None] * GAME_SIZE for _ in range(GAME_SIZE)]
        for tile in self.tiles:
            col, row = tile.current_pos
            state[row][col] = tile.correct_pos
        bx, by = self.blank_pos
        state[by][bx] = None
        return tuple(tuple(row) for row in state)
    
    def get_numbered_state(self):
        state = [0] * (GAME_SIZE * GAME_SIZE)
        for tile in self.tiles:
            col, row = tile.current_pos
            index = row * GAME_SIZE + col
            correct_col, correct_row = tile.correct_pos
            number = correct_row * GAME_SIZE + correct_col + 1
            state[index] = number
        return state