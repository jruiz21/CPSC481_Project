from hints import a_star
import pygame
from sprite import *
from settings import *

def chosen_image():
    prompt_font = pygame.font.SysFont("Comic Sans", 28)
    small_font = pygame.font.SysFont("Comic Sans", 20)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    while True:
        screen.fill(DARKGREY)
        title = prompt_font.render("Drag and drop an image", True, WHITE)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40)))
        subtitle = small_font.render("(.png, .jpg, .jpeg, .bmp)", True, LIGHTGREY)
        screen.blit(subtitle, subtitle.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)
            if event.type == pygame.DROPFILE:
                image_path = event.file
                if image_path.lower().endswith((".png", ".jpg", ".jpeg", ".bmp")):
                    return image_path

HIGHSCORE_FILE = "highscore.txt"

def load_highscore():
    try:
        with open(HIGHSCORE_FILE, "r") as f:
            data = f.read().split(",")
            return int(data[0]), int(data[1])
    except:
        return None, None

def save_highscore(moves, hints):
    best_moves, _ = load_highscore()
    if best_moves is None or moves < best_moves:
        with open(HIGHSCORE_FILE, "w") as f:
            f.write(f"{moves},{hints}")

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode ((WIDTH, HEIGHT))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 40)
        self.small_font = pygame.font.SysFont("Arial", 24)

    def new(self, reuse_image=False):
        self.won = False
        self.hint_tile = None
        self.hints_used = 0
        self.used_solve = False
        if not reuse_image or not hasattr(self, 'image'):
            image_path = chosen_image()
            if not image_path:
                pygame.quit()
                quit(0)
            raw_image = pygame.image.load(image_path)
            grid_size = GAME_SIZE * TILESIZE
            self.image = pygame.transform.scale(raw_image, (grid_size, grid_size))
        self.board = Board(self.image)
        
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

        while self.won:
            self.clock.tick(FPS)
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.won = False
        
    def update(self):
        if self.board.is_solved():
            self.won = True
            self.playing = False
            if not self.used_solve:
                save_highscore(self.board.moves, self.hints_used)
        
    def draw(self):
        self.screen.fill(BGCOLOUR)
        self.board.draw(self.screen)
        if self.hint_tile is not None:
            col, row = self.hint_tile
            x = col * TILESIZE
            y = row * TILESIZE
            pygame.draw.rect(self.screen, (255, 255, 0), (x, y, TILESIZE, TILESIZE), 5)
        moves_text = self.font.render(f"Moves: {self.board.moves}", True, WHITE)
        self.screen.blit(moves_text, (GAME_SIZE * TILESIZE + 20, 20))
        hs_moves, hs_hints = load_highscore()
        if hs_moves is not None:
            hs_text = self.small_font.render(f"Best: {hs_moves} moves ({hs_hints} hints)", True, WHITE)
            self.screen.blit(hs_text, (GAME_SIZE * TILESIZE + 20, 70))
        pygame.draw.rect(self.screen, LIGHTGREY, (GAME_SIZE * TILESIZE + 20, 120, 120, 45))
        hint_text = self.small_font.render("Hint", True, BLACK)
        self.screen.blit(hint_text, (GAME_SIZE * TILESIZE + 50, 133))
        pygame.draw.rect(self.screen, LIGHTGREY, (GAME_SIZE * TILESIZE + 20, 180, 120, 45))
        solve_text = self.small_font.render("Solve", True, BLACK)
        self.screen.blit(solve_text, (GAME_SIZE * TILESIZE + 48, 193))
        if self.won:
            self.win_screen()
        pygame.display.flip()
        
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.playing = False
                if event.key == pygame.K_h:
                    curr_state = self.board.get_numbered_state()
                    next_state = a_star(curr_state)
                    self.hint_tile = self.get_tile_to_highlight(curr_state, next_state)
            if event.type == pygame.MOUSEBUTTONDOWN and not self.won:
                hint_rect = pygame.Rect(GAME_SIZE * TILESIZE + 20, 120, 120, 45)
                solve_rect = pygame.Rect(GAME_SIZE * TILESIZE + 20, 180, 120, 45)
                if hint_rect.collidepoint(pygame.mouse.get_pos()):
                    curr_state = self.board.get_numbered_state()
                    next_state = a_star(curr_state)
                    self.hint_tile = self.get_tile_to_highlight(curr_state, next_state)
                    self.hints_used += 1
                elif solve_rect.collidepoint(pygame.mouse.get_pos()):
                    self.solve_puzzle()
                else:
                    self.board.handle_click(pygame.mouse.get_pos())
                    self.hint_tile = None

    def win_screen(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        win_text = self.font.render("Puzzle Solved!", True, WHITE)
        moves_text = self.small_font.render(f"Completed in {self.board.moves} moves", True, WHITE)
        hints_text = self.small_font.render(f"Hints used: {self.hints_used}", True, WHITE)
        restart_text = self.small_font.render("Press R to play again", True, WHITE)
        cx = WIDTH // 2
        self.screen.blit(win_text, win_text.get_rect(center=(cx, HEIGHT // 2 - 50)))
        self.screen.blit(moves_text, moves_text.get_rect(center=(cx, HEIGHT // 2)))
        self.screen.blit(hints_text, hints_text.get_rect(center=(cx, HEIGHT // 2 + 80)))
        self.screen.blit(restart_text, restart_text.get_rect(center=(cx, HEIGHT // 2 + 50)))

    def get_tile_to_highlight(self, curr_state, next_state):
        if next_state is None:
            return None
        for i in range(len(curr_state)):
            if curr_state[i] != next_state[i] and curr_state[i] != 0:
                col = i % GAME_SIZE
                row = i // GAME_SIZE
                return (col, row)
        return None
    
    def solve_puzzle(self):
        self.used_solve = True
        curr_state = self.board.get_numbered_state()
        state = curr_state
        for _ in range(100):
            next_state = a_star(state)
            if next_state is None:
                break
            hint_tile = self.get_tile_to_highlight(state, next_state)
            if hint_tile:
                self.board.handle_click((hint_tile[0] * TILESIZE, hint_tile[1] * TILESIZE))
                self.draw()
                pygame.display.flip()
                pygame.time.delay(200)
            state = self.board.get_numbered_state()
            if self.board.is_solved():
                break

game = Game()
game.new()
game.run()
while True:
        game.new(reuse_image=True)
        game.run()