import pygame

# pygame setup
pygame.init()

## display setup
display_ratio = 5/4
display_width = 500
display_height = display_width * display_ratio

edge_padding = 15

window = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()
running = True

while running:

    window.fill("purple")

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
