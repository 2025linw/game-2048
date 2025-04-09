from game import Board

import pygame
import pygame_gui

class GameUI(Board):
    def __init__(self, h=None):
        # Class Initialization
        self.heuristic = h

        # GUI Initialization
        pygame.init()

        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        # Game Initialization
        self.auto = False

        pygame.display.flip()

    def cleanup(self):
        pygame.quit()

    def auto_move(self):
        pass

    def update(self):
        for event in pygame.event.get():
            match event:
                case pygame.QUIT:
                    self.running = False
                case pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_q | pygame.K_ESCAPE:
                            self.running = False

                        case pygame.K_n:
                            self.start_game()

                        case pygame.K_p:
                            self.auto = not self.auto
                        case pygame.K_o:
                            if not self.auto:
                                self.auto_move()

                        case pygame.K_LEFT | pygame.K_a:
                            self.make_move('left')
                        case pygame.K_UP | pygame.K_w:
                            self.make_move('up')
                        case pygame.K_RIGHT | pygame.K_d:
                            self.make_move('right')
                        case pygame.K_DOWN | pygame.K_s:
                            self.make_move('down')

                        case pygame.K_t:
                            print("unimplemented")

        if self.auto and not self.is_terminal():
            self.auto_move()

    def render(self):
        pygame.display.flip()

        self.clock.tick(60)

# Window Dimension
WIN_RATIO = 5/4

WIN_WIDTH = 500
WIN_HEIGHT = WIN_WIDTH * WIN_RATIO

EDGE_WIDTH = 15

# Component Sizes
# BOARD_SIZE = (
#     BOARD_SIZE - 2 * EDGE_WIDTH,
#     BOARD_SIZE - 2 * EDGE_WIDTH
# )


colors = {
    "bg": pygame.Color("#faf8ef"),
    "bd": pygame.Color("#bbada0"),
    0: pygame.Color(205, 192, 181),
    2: pygame.Color("#eee4da"),
    4: pygame.Color("#ede0c8"),
    8: pygame.Color("#f2b179"),
    16: pygame.Color("#f59563"),
    32: pygame.Color("#f67c5f"),
    64: pygame.Color("#f65e3b"),
    128: pygame.Color("#edcf72"),
    256: pygame.Color("#edcc61"),
    512: pygame.Color("#edc850"),
    1024: pygame.Color("#edc53f"),
    2048: pygame.Color("#edc22e"),
}

text_colors = {
    "default": pygame.Color("#776e65"),
    "scr_ll": pygame.Color("#eee4da"),
    "scr": pygame.Color("white"),
    0: pygame.Color(0, 0, 0),
    2: pygame.Color("#776e65"),
    4: pygame.Color("#776e65"),
    8: pygame.Color("#f9f6f2"),
    16: pygame.Color("#f9f6f2"),
    32: pygame.Color("#f9f6f2"),
    64: pygame.Color("#f9f6f2"),
    128: pygame.Color("#f9f6f2"),
    256: pygame.Color("#f9f6f2"),
    512: pygame.Color("#f9f6f2"),
    1024: pygame.Color("#f9f6f2"),
    2048: pygame.Color("#f9f6f2"),
}
