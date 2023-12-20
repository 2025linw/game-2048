from numpy import tile
import game2048
import ai2048

import pygame
import pygame_gui

# Window Dimension
W_SIZE = 500
BANNER_HEIGHT = W_SIZE / 4

PADDING = 15

# Asset Sizes
BOARD_SIZE = (W_SIZE - 2 * PADDING, W_SIZE - 2 * PADDING)
TILE_SIZE = ((W_SIZE - 4 * PADDING - (game2048.N - 1) * PADDING) / game2048.N, (W_SIZE - 4 * PADDING - (game2048.N - 1) * PADDING) / game2048.N)
GAME_OVER_SIZE = (4 * (W_SIZE - 2 * PADDING) / 5, (BANNER_HEIGHT - 2 * PADDING))
SCORE_SIZE = ((W_SIZE - 2 * PADDING) / 5, (BANNER_HEIGHT - 2 * PADDING) / 2)
AUTOPLAY_SIZE = ((W_SIZE - 2 * PADDING) / 5, (BANNER_HEIGHT - 2 * PADDING) / 2)

# Asset Top Left Point
BOARD_TOP_LEFT = (PADDING, BANNER_HEIGHT + PADDING)
TILE_TOP_LEFT = (BOARD_TOP_LEFT[0] + PADDING, BOARD_TOP_LEFT[1] + PADDING)
GAME_OVER_TOP_LEFT = (PADDING, PADDING)
SCORE_TOP_LEFT = (W_SIZE - PADDING - SCORE_SIZE[0], PADDING)
AUTOPLAY_TOP_LEFT = (W_SIZE - PADDING - AUTOPLAY_SIZE[0], BANNER_HEIGHT - AUTOPLAY_SIZE[1])

pygame.init()

# Colors
colors = {
    "background": pygame.Color("#faf8ef"),
    "board": pygame.Color("#bbada0"),
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
    "main": pygame.Color("#776e65"),
    "score_label": pygame.Color("#eee4da"),
    "score": pygame.Color("white"),
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

# Rects
board_rect = pygame.Rect(
    BOARD_TOP_LEFT,
    BOARD_SIZE,
)
score_rect = pygame.Rect(
    SCORE_TOP_LEFT,
    SCORE_SIZE,
)
autoplay_rect = pygame.Rect(
    AUTOPLAY_TOP_LEFT,
    AUTOPLAY_SIZE,
)

# Text Stuff
text_font = {
    "main": pygame.font.Font('./clear-sans/ClearSans-Bold.ttf', 50),
    "score_label": pygame.font.Font('./clear-sans/ClearSans-Bold.ttf', 13),
    "score": pygame.font.Font('./clear-sans/ClearSans-Bold.ttf', 25),
    "s_tile": pygame.font.Font('./clear-sans/ClearSans-Bold.ttf', 55),
    "m_tile": pygame.font.Font('./clear-sans/ClearSans-Bold.ttf', 45),
    "l_tile": pygame.font.Font('./clear-sans/ClearSans-Bold.ttf', 35),
}

game_over_text = text_font["main"].render("Game Over", True, text_colors["main"])
game_over_text_rect = game_over_text.get_rect()
game_over_text_rect.center = (GAME_OVER_TOP_LEFT[0] + GAME_OVER_SIZE[0]/2, GAME_OVER_TOP_LEFT[1] + GAME_OVER_SIZE[1]/2)

score_label_text = text_font["score_label"].render("SCORE", True, text_colors["score_label"])
score_label_text_rect = score_label_text.get_rect()
score_label_text_rect.center = (SCORE_TOP_LEFT[0] + SCORE_SIZE[0]/2, SCORE_TOP_LEFT[1] + SCORE_SIZE[1]/4)

autoplay_text = text_font["score"].render("AUTO", True, text_colors["score_label"])
autoplay_text_rect = autoplay_text.get_rect()
autoplay_text_rect.center = (AUTOPLAY_TOP_LEFT[0] + AUTOPLAY_SIZE[0]/2, AUTOPLAY_TOP_LEFT[1] + AUTOPLAY_SIZE[1]/2)

def main():
    # UI Initialization
    screen = pygame.display.set_mode((W_SIZE, BANNER_HEIGHT + W_SIZE))
    clock = pygame.time.Clock()
    running = True

    auto = False

    # Game Initialization
    # game = game2048.Board()

    game = ai2048.RandomAI()
    # game = ai2048.GreedyAI()
    # game = ai2048.AveragedDLS(3, 8)
    game.start()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_q | pygame.K_ESCAPE: running = False

                    case pygame.K_n: game.start()
                    case pygame.K_p: auto = not auto
                    case pygame.K_s:
                        if not auto:
                            game.make_move()

                    case pygame.K_t:
                        print(game2048.Board.sim_move(game.grid, "left"))

                    case pygame.K_UP: game.move("up")
                    case pygame.K_DOWN: game.move("down")
                    case pygame.K_LEFT: game.move("left")
                    case pygame.K_RIGHT: game.move("right")

        if auto and not game.terminal():
            game.make_move()

        # Background and Board Background
        screen.fill(colors["background"])
        screen.fill(
            colors["board"],
            board_rect
        )

        # Game Over
        if game.terminal(): screen.blit(game_over_text, game_over_text_rect)

        # Score Block
        screen.fill(
            colors["board"],
            score_rect
        )
        screen.blit(score_label_text, score_label_text_rect)

        score_text = text_font["score"].render(
            "{}".format(game.score),
            True,
            text_colors["score"]
        )
        score_text_rect = score_text.get_rect()
        score_text_rect.center = (SCORE_TOP_LEFT[0] + SCORE_SIZE[0]/2, SCORE_TOP_LEFT[1] + 2*SCORE_SIZE[1]/3)
        screen.blit(score_text, score_text_rect)

        # AI Mode Display
        if auto:
            screen.fill(
                colors["board"],
                autoplay_rect,
            )
            screen.blit(autoplay_text, autoplay_text_rect)

        # Tiles
        for r in range(game2048.N):
            for c in range(game2048.N):
                tile_top_left = (
                    TILE_TOP_LEFT[0] + c*(TILE_SIZE[0] + PADDING),
                    TILE_TOP_LEFT[1] + r*(TILE_SIZE[1] + PADDING),
                )

                tile_val = game.grid[r][c]
                if not tile_val:
                    screen.fill(
                        colors[0],
                        pygame.Rect(
                            tile_top_left,
                            TILE_SIZE,
                        )
                    )

                    continue

                color = colors[tile_val if tile_val <= 2048 else 2048]
                screen.fill(
                    color,
                    pygame.Rect(
                        tile_top_left,
                        TILE_SIZE
                    )
                )

                tile_text = text_font["s_tile" if tile_val < 100 else ("m_tile" if tile_val < 1000 else "l_tile")].render(
                    "{}".format(tile_val),
                    True,
                    text_colors[tile_val if tile_val <= 2048 else 2048]
                )
                text_rect = tile_text.get_rect()
                text_rect.center = (tile_top_left[0] + TILE_SIZE[0]/2, tile_top_left[1] + TILE_SIZE[1]/2)
                if tile_val: screen.blit(
                    tile_text,
                    text_rect
                )

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
