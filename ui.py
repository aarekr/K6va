""" User Interface module """

import sys
import random
import pygame

BOARD_SIZE = (950, 750)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 170, 0)

CARDS = []
CARD_IMAGE_SIZE = (100, 130)
CARD_LIST = ["cards/6_of_spades.png", "cards/6_of_clubs.png", "cards/6_of_diamonds.png", "cards/6_of_hearts.png",
            "cards/7_of_spades.png", "cards/7_of_clubs.png", "cards/7_of_diamonds.png", "cards/7_of_hearts.png"]
for i in range(8):
    image = pygame.image.load((CARD_LIST[i]))
    image = pygame.transform.scale(image, CARD_IMAGE_SIZE)
    CARDS.append(image)
print("CARDS:", CARDS)

def game_top_text():
    """ Displaying K6va text """
    text_font = pygame.font.Font(pygame.font.get_default_font(), 60)
    game_starts = "Kõva"
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
        self.screen.blit(game_top_text(), (370, 15))
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
        self.screen.fill(GREEN)
        self.screen.blit(game_top_text(), (370, 15))
        pygame.display.update()

        print("\nGame started")
        while self.game_active:
            self.screen.blit(CARDS[4], (330, 600))
            self.screen.blit(CARDS[5], (450, 600))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    clicked_position = event.pos
                    print("clicked_position:", clicked_position)
