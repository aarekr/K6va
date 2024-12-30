""" User Interface module """

import sys
import random
import pygame

#width = screen.get_width()
#height = screen.get_height()
BOARD_SIZE = (1000, 750)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 170, 0)

CARDS = []
CARD_IMAGE_SIZE = (100, 130)
CARD_LIST = [(6, "c", "cards/6_of_clubs.png"), (6, "d", "cards/6_of_diamonds.png"),
            (6, "h", "cards/6_of_hearts.png"), (6, "s", "cards/6_of_spades.png"),
            (7, "c", "cards/7_of_clubs.png"), (7, "d", "cards/7_of_diamonds.png"),
            (7, "h", "cards/7_of_hearts.png"), (7, "s", "cards/7_of_spades.png"),
            (8, "c", "cards/8_of_clubs.png"), (8, "d", "cards/8_of_diamonds.png"),
            (8, "h", "cards/8_of_hearts.png"), (8, "s", "cards/8_of_spades.png"),
            (9, "c", "cards/9_of_clubs.png"), (9, "d", "cards/9_of_diamonds.png"),
            (9, "h", "cards/9_of_hearts.png"), (9, "s", "cards/9_of_spades.png"),
            (10, "c", "cards/10_of_clubs.png"), (10, "d", "cards/10_of_diamonds.png"),
            (10, "h", "cards/10_of_hearts.png"), (10, "s", "cards/10_of_spades.png"),
            (11, "c", "cards/jack_of_clubs.png"), (11, "d", "cards/jack_of_diamonds.png"),
            (11, "h", "cards/jack_of_hearts.png"), (11, "s", "cards/jack_of_spades.png"),
            (12, "c", "cards/queen_of_clubs.png"), (12, "d", "cards/queen_of_diamonds.png"),
            (12, "h", "cards/queen_of_hearts.png"), (12, "s", "cards/queen_of_spades.png"),
            (13, "c", "cards/king_of_clubs.png"), (13, "d", "cards/king_of_diamonds.png"),
            (13, "h", "cards/king_of_hearts.png"), (13, "s", "cards/king_of_spades.png"),
            (14, "c", "cards/ace_of_clubs.png"), (14, "d", "cards/ace_of_diamonds.png"),
            (14, "h", "cards/ace_of_hearts.png"), (14, "s", "cards/ace_of_spades.png")
            ]
for i in range(len(CARD_LIST)):
    image = pygame.image.load((CARD_LIST[i][2]))
    image = pygame.transform.scale(image, CARD_IMAGE_SIZE)
    CARDS.append(image)
print("CARDS:", CARDS)

def game_top_text():
    """ Displaying K6va text """
    text_font = pygame.font.Font(pygame.font.get_default_font(), 60)
    game_starts = "Kõva"
    label = text_font.render(game_starts, 0, RED)
    return label

def how_many_players_text():
    """ Displaying how many players in game question text """
    text_font = pygame.font.Font(pygame.font.get_default_font(), 30)
    game_starts = "How many players? 3 or 4?"
    label = text_font.render(game_starts, 0, BLUE)
    return label

class UI:
    """ User interface class """
    def __init__(self):
        self.screen = pygame.display.set_mode(BOARD_SIZE)
        self.game_active = True
        self.players = 3
        self.round = 0
        self.players_hand = []
        self.points = 0

    def start_game(self):
        """ Texts when game starts """
        pygame.init()
        self.screen.blit(game_top_text(), (400, 15))
        self.screen.blit(how_many_players_text(), (260, 250))
        pygame.display.update()
        start_game = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_3:
                        start_game = True
                        self.points = 0
                    elif event.key == pygame.K_4:
                        start_game = True
                        self.players = 4
                        self.points = 0
            if start_game is True:
                break
        print("number of players:", self.players)
        self.game_loop()

    def deal_cards(self):
        self.round += 1
        print("dealing cards, round:", self.round)
        self.screen.fill(GREEN)
        self.screen.blit(game_top_text(), (370, 15))
        random.shuffle(CARDS)
        self.players_hand = []
        for _ in range(self.round):
            card = CARDS.pop()
            self.players_hand.append(card)
        pygame.display.update()

    def game_loop(self):
        """ Game loop """
        pygame.init()
        self.screen.fill(GREEN)
        self.screen.blit(game_top_text(), (370, 15))
        pygame.display.update()

        print("\nGame started")
        while self.game_active:
            if self.round == 0:
                pass
            elif self.round == 1:
                self.screen.blit(self.players_hand[0], (400, 600))
            elif self.round == 2:
                self.screen.blit(CARDS[4], (330, 600))
                self.screen.blit(CARDS[5], (450, 600))
            pygame.draw.rect(self.screen, BLUE,[100, 100,140,40])
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    clicked_position = event.pos
                    print("clicked_position:", clicked_position)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:
                        self.deal_cards()

