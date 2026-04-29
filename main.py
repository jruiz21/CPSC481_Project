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
            return int(data[0]), int(data[1]), int(data[2])
    except:
        return None, 0, 0

def save_highscore(moves, hints, time):
    best_moves, _, _ = load_highscore()
    if best_moves is None or moves < best_moves:
        with open(HIGHSCORE_FILE, "w") as f:
            f.write(f"{moves},{hints},{time}")

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode ((WIDTH, HEIGHT))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 40)
        self.small_font = pygame.font.SysFont("Arial", 24)
        # Centering
        self.grid_width = GAME_SIZE * TILESIZE
        self.grid_height = GAME_SIZE * TILESIZE
        self.x_offset = (WIDTH - self.grid_width) // 2
        self.y_offset = 150 # ((HEIGHT - self.grid_height) // 2) + 100

    def new(self, reuse_image=False):
        self.won = False
        self.hint_tile = None
        self.hints_used = 0
        self.used_solve = False
        self.start_time = pygame.time.get_ticks()
        if not reuse_image or not hasattr(self, 'image'):
            image_path = chosen_image()
            if not image_path:
                pygame.quit()
                quit(0)
            raw_image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(raw_image, (self.grid_width, self.grid_height))
        self.board = Board(self.image)
        self.initial_state = self.board.get_numbered_state()
        self.optimal_moves = None
        
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
            self.elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
            self.optimal_moves = self._get_optimal_moves(self.initial_state)
            if not self.used_solve:
                save_highscore(self.board.moves, self.hints_used, self.elapsed_time)
        
    def draw(self):
        # Puzzle centering and extra alignment variables
        center_x = WIDTH // 2
        puzzle_bottom = self.y_offset + self.grid_height
        button_y = puzzle_bottom + 30
        self.screen.fill(BGCOLOUR)
        self.board.draw(self.screen, self.x_offset, self.y_offset)
        # Hint Highlights
        if self.hint_tile is not None:
            col, row = self.hint_tile
            hx = self.x_offset + (col * TILESIZE)
            hy = self.y_offset + (row * TILESIZE)
            pygame.draw.rect(self.screen, (255, 255, 0), (hx, hy, TILESIZE, TILESIZE), 5)
        # Top UI
        moves_text = self.font.render(f"Moves: {self.board.moves}", True, WHITE)
        self.screen.blit(moves_text, moves_text.get_rect(center=(center_x, 40)))

        hs_moves, hs_hints, hs_time = load_highscore()
        if hs_moves is not None:
            hs_minutes = hs_time // 60
            hs_seconds = hs_time % 60
            hs_line1 = self.small_font.render(f"Best: {hs_moves} moves, using {hs_hints} hints", True, WHITE)
            hs_line2 = self.small_font.render(f"Time: {hs_minutes:02d}:{hs_seconds:02d}", True, WHITE)
            self.screen.blit(hs_line1, hs_line1.get_rect(center=(center_x, 85)))
        # Bottom UI
        elapsed = (pygame.time.get_ticks() - self.start_time) // 1000
        # minutes = elapsed // 60
        # seconds = elapsed % 60
        # timer_text = self.small_font.render(f"Time: {minutes:02d}:{seconds:02d}", True, WHITE)
        timer_text = self.small_font.render(f"Time: {elapsed//60:02d}:{elapsed%60:02d}", True, WHITE)
        # self.screen.blit(timer_text, (center_x, 340))
        self.screen.blit(timer_text, timer_text.get_rect(center=(center_x, 115)))

        # pygame.draw.rect(self.screen, LIGHTGREY, (ui_x, 220, 120, 45))
        # hint_text = self.small_font.render("Hint", True, BLACK)
        # self.screen.blit(hint_text, (ui_x, 233))

        # pygame.draw.rect(self.screen, LIGHTGREY, (ui_x, 280, 120, 45))
        # solve_text = self.small_font.render("Solve", True, BLACK)
        # self.screen.blit(solve_text, (ui_x, 293))

        hint_rect = pygame.Rect(center_x - 130, button_y, 120, 45)
        solve_rect = pygame.Rect(center_x + 10, button_y, 120, 45)
        
        pygame.draw.rect(self.screen, LIGHTGREY, hint_rect)
        pygame.draw.rect(self.screen, LIGHTGREY, solve_rect)
        
        h_text = self.small_font.render("Hint", True, BLACK)
        s_text = self.small_font.render("Solve", True, BLACK)
        self.screen.blit(h_text, h_text.get_rect(center=hint_rect.center))
        self.screen.blit(s_text, s_text.get_rect(center=solve_rect.center))
        
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
                mouse_pos = pygame.mouse.get_pos()
                center_x = WIDTH // 2
                button_y = self.y_offset + self.grid_height + 30
                hint_rect = pygame.Rect(center_x - 130, button_y, 120, 45)
                solve_rect = pygame.Rect(center_x + 10, button_y, 120, 45)
                if hint_rect.collidepoint(mouse_pos):
                    curr_state = self.board.get_numbered_state()
                    next_state = a_star(curr_state)
                    self.hint_tile = self.get_tile_to_highlight(curr_state, next_state)
                    self.hints_used += 1
                elif solve_rect.collidepoint(mouse_pos):
                    self.solve_puzzle()
                else:
                    grid_x = mouse_pos[0] - self.x_offset
                    grid_y = mouse_pos[1] - self.y_offset
                    if 0 <= grid_x < self.grid_width and 0 <= grid_y < self.grid_height:
                        self.board.handle_click((grid_x, grid_y))
                        self.hint_tile = None

    def win_screen(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        win_text = self.font.render("Puzzle Solved!", True, WHITE)
        moves_text = self.small_font.render(f"Completed in {self.board.moves} moves", True, WHITE)
        optimal_text = self.small_font.render(f"Optimal moves: {self.optimal_moves}", True, WHITE)
        hints_text = self.small_font.render(f"Hints used: {self.hints_used}", True, WHITE)
        restart_text = self.small_font.render("Press R to play again", True, WHITE)
        cx = WIDTH // 2
        minutes = self.elapsed_time // 60
        seconds = self.elapsed_time % 60
        time_text = self.small_font.render(f"Time: {minutes:02d}:{seconds:02d}", True, WHITE)
        self.screen.blit(time_text, time_text.get_rect(center=(cx, HEIGHT // 2 + 120)))
        self.screen.blit(win_text, win_text.get_rect(center=(cx, HEIGHT // 2 - 50)))
        self.screen.blit(moves_text, moves_text.get_rect(center=(cx, HEIGHT // 2)))
        self.screen.blit(optimal_text, optimal_text.get_rect(center=(cx, HEIGHT // 2 + 25)))
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
        temp_moves = self.board.moves
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
                self.hints_used = (self.board.moves - temp_moves)
                break

    def _get_optimal_moves(self, initial_state):
        state = initial_state
        count = 0
        while True:
            next_state = a_star(state)
            if next_state is None:
                break
            state = next_state
            count += 1
            if state == list(range(1, 9)) + [0]:
                break
        return count

game = Game()
game.new()
game.run()
while True:
        game.new(reuse_image=True)
        game.run()