""" User Interface module """

import sys
import random
import pygame

BOARD_SIZE = (950, 750)
RED = (255, 0, 0)

def game_top_text():
    """ Displaying K6va text """
    text_font = pygame.font.Font(pygame.font.get_default_font(), 60)
    game_starts = "K6va"
    label = text_font.render(game_starts, 0, RED)
    return label

class UI:
    """ User interface class """
    def __init__(self):
        self.game_active = True
        self.screen = pygame.display.set_mode(BOARD_SIZE)

    def start_game(self):
        """ Texts when game starts """
        pygame.init()
        self.screen.blit(game_top_text(), (250, 15))
        #self.screen.blit(game_start_text(), (210, 250))
        pygame.display.update()
        start_game = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        start_game = True
                        self.points = 0
            if start_game is True:
                break
        self.game_loop()

    def game_loop(self):
        """ Game loop """
        pygame.init()
        self.screen.blit(game_top_text(), (250, 15))

        print("\nGame started")
        while self.game_active:
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    clicked_position = event.pos
                    print("clicked_position:", clicked_position)
