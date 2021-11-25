from models import GameManager
import pygame
import os
import settings
import sys


pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'
screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

game_manager = GameManager()
while True:
    # get mouse position
    pos = pygame.mouse.get_pos()

    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        game_manager.handle_event(event=event, pos=pos)

    # draw on canvass
    game_manager.draw(screen=screen, cursor_pos=pos)
