__author__ = 'Simon'
from config import *

clock = pygame.time.Clock()
game = GameScreen(screen)
while running:
    screen.fill(black)
    game.draw()
    game.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
            game.handle_events(event)
    pygame.display.flip()
    clock.tick(100)