""" User Interface module """

import sys
import random
import pygame

from ui_helper import *

#width = screen.get_width()
#height = screen.get_height()
BOARD_SIZE = (1000, 750)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 170, 0)

CARDS = []
CARD_INDECES = list(range(36))
CARD_IMAGE_SIZE = (100, 130)

players_cards = []
opponents_attempts = []

for i in range(len(CARD_LIST)):
    image = pygame.image.load((CARD_LIST[i][2]))
    image = pygame.transform.scale(image, CARD_IMAGE_SIZE)
    CARDS.append(image)

class UI:
    """ User interface class """
    def __init__(self):
        self.screen = pygame.display.set_mode(BOARD_SIZE)
        self.game_active = True
        self.players = 3                    # change to 4 if 4 players playing
        self.round = 0                      # rounds 1->12->1 if 3 players, 1->9->1 if 4 players
        self.players_hands = [[],[],[],[]]  # holds cards dealt during each round
        self.card_indeces = [[],[],[],[]]   # card indeces in players' hands
        self.points = [[],[],[],[]]         # holds cumulative points per player during the game

    def start_game(self):
        """ Texts when game starts """
        pygame.init()
        self.screen.blit(game_top_text(), (420, 15))
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

    def draw_letter_buttons(self, BUTTONS):
        """ Drawing text buttons """
        for button, text in BUTTONS:
            button_text = box_text(text)
            button_text_rect = button_text.get_rect(center=(button.x + 20, button.y + 20))
            pygame.draw.rect(self.screen, BLACK, button, 2)
            self.screen.blit(button_text, button_text_rect)

    def empty_hands(self):
        """ Emptying hands before next round """
        self.players_hands[0] = []
        self.players_hands[1] = []
        self.players_hands[2] = []
        self.players_hands[3] = []
        self.card_indeces[0] = []
        self.card_indeces[1] = []
        self.card_indeces[2] = []
        self.card_indeces[3] = []

    def deal_cards(self):
        """ Shuffle and deal cards to players """
        self.round += 1
        print("****************************************************************")
        print("dealing cards, round:", self.round)
        self.screen.fill(GREEN)
        #self.screen.blit(game_top_text(), (420, 15))
        self.screen.blit(game_points_text(self.points), (20,15))
        self.draw_letter_buttons(BUTTONS)
        random.shuffle(CARD_INDECES)  # numbers 0-35 are shuffled
        print("CARD_INDECES shuffled:", CARD_INDECES)
        self.empty_hands()
        index_pointer = 0  # index in CARD_INDECES which determines a card in CARDS
        # each player gets self.round number of cards
        print("PLAYER")
        for i in range(self.round):
            print("i:", i, "- p:", index_pointer, " - INDECES:", CARD_INDECES[index_pointer])
            self.players_hands[0].append(CARDS[CARD_INDECES[index_pointer]])
            self.card_indeces[0].append(CARD_INDECES[index_pointer])
            index_pointer += 1

        print("OPPONENT 1")
        for i in range(self.round):
            print("i:", i, "- p:", index_pointer, " - INDECES:", CARD_INDECES[index_pointer])
            self.players_hands[1].append(CARDS[CARD_INDECES[index_pointer]])
            self.card_indeces[1].append(CARD_INDECES[index_pointer])
            index_pointer += 1
        opponent_1_hand_value = round(self.opponent_hand_value(1))
        print("opponent_1_hand_value:", opponent_1_hand_value)

        print("OPPONENT 2")
        for i in range(self.round):
            print("i:", i, "- p:", index_pointer, " - INDECES:", CARD_INDECES[index_pointer])
            self.players_hands[2].append(CARDS[CARD_INDECES[index_pointer]])
            self.card_indeces[2].append(CARD_INDECES[index_pointer])
            index_pointer += 1
        opponent_2_hand_value = round(self.opponent_hand_value(2))
        print("opponent_2_hand_value:", opponent_2_hand_value)

        if self.players == 4:
            print("OPPONENT 3")
            for i in range(self.round):
                print("i:", i, "- p:", index_pointer, " - INDECES:", CARD_INDECES[index_pointer])
                self.players_hands[3].append(CARDS[CARD_INDECES[index_pointer]])
                self.card_indeces[3].append(CARD_INDECES[index_pointer])
                index_pointer += 1
            opponent_3_hand_value = round(self.opponent_hand_value(3))
            print("opponent_3_hand_value:", opponent_3_hand_value)

        self.show_cards_on_table()
        self.show_trump_card()
        pygame.display.update()
        return [opponent_1_hand_value, opponent_2_hand_value, opponent_3_hand_value]

    def opponent_hand_value(self, player_index):
        """ Counting opponents' hand and attempt values """
        hand = {"c": [], "d": [], "h": [], "s": []}
        hand_value = 0
        for i in self.card_indeces[player_index][-(self.round+1):]:
            hand[CARD_LIST[i][1]].append(CARD_LIST[i][0])
        print("hand:", hand)
        for key, value in hand.items():
            if key == CARD_LIST[CARD_INDECES[-1]][1] and len(value) > 0:  # trump in hand
                for card in value:  # point for every trump card
                    print("card in value:", card)
                    if (key == "c" and value == 7) or (key == "s" and value == 7):  # c7,s7
                        continue
                    hand_value += 1
                #if hand_value > self.round/2:  # max half of the round points
                #    hand_value = self.round/2
            else:
                for v in value:
                    if v >= 13:  # non-trump kings and aces
                        hand_value += 0.2
            if (key == "c" and 7 in value) or (key == "s" and 7 in value):
                hand_value += 1
        return hand_value

    def show_trump_card(self):
        """ Showing trump card in the right upper corner """
        if (self.players == 3 and self.round < 12) or (self.players == 4 and self.round < 9):
            self.screen.blit(CARDS[CARD_INDECES[-1]], (870, 20))

    def show_cards_on_table(self):
        """ Drawing cards on the table """
        if self.round == 1:
            self.screen.blit(self.players_hands[0][0], (450, 600))
            card = pygame.Rect(450, 600, 100, 130)
            players_cards.append(card)
            self.screen.blit(self.players_hands[1][0], (50, 300))
            self.screen.blit(self.players_hands[2][0], (850, 300))
            if self.players == 4:
                self.screen.blit(self.players_hands[3][0], (450, 50))
        elif self.round == 2:
            self.screen.blit(self.players_hands[0][0], (390, 600))
            self.screen.blit(self.players_hands[0][1], (510, 600))
            self.screen.blit(self.players_hands[1][0], (50, 300))
            self.screen.blit(self.players_hands[1][1], (70, 300))
            self.screen.blit(self.players_hands[2][0], (830, 300))
            self.screen.blit(self.players_hands[2][1], (850, 300))
            if self.players == 4:
                self.screen.blit(self.players_hands[3][0], (440, 50))
                self.screen.blit(self.players_hands[3][1], (460, 50))
        elif self.round == 3:
            self.screen.blit(self.players_hands[0][0], (330, 600))
            self.screen.blit(self.players_hands[0][1], (450, 600))
            self.screen.blit(self.players_hands[0][2], (570, 600))
            self.screen.blit(self.players_hands[1][0], (50, 300))
            self.screen.blit(self.players_hands[1][1], (70, 300))
            self.screen.blit(self.players_hands[1][2], (90, 300))
            self.screen.blit(self.players_hands[2][0], (810, 300))
            self.screen.blit(self.players_hands[2][1], (830, 300))
            self.screen.blit(self.players_hands[2][2], (850, 300))
            if self.players == 4:
                self.screen.blit(self.players_hands[3][0], (430, 50))
                self.screen.blit(self.players_hands[3][1], (450, 50))
                self.screen.blit(self.players_hands[3][2], (470, 50))
        elif self.round == 4:
            self.screen.blit(self.players_hands[0][0], (270, 600))
            self.screen.blit(self.players_hands[0][1], (390, 600))
            self.screen.blit(self.players_hands[0][2], (510, 600))
            self.screen.blit(self.players_hands[0][3], (630, 600))
            self.screen.blit(self.players_hands[1][0], (50, 300))
            self.screen.blit(self.players_hands[1][1], (70, 300))
            self.screen.blit(self.players_hands[1][2], (90, 300))
            self.screen.blit(self.players_hands[1][3], (110, 300))
            self.screen.blit(self.players_hands[2][0], (790, 300))
            self.screen.blit(self.players_hands[2][1], (810, 300))
            self.screen.blit(self.players_hands[2][2], (830, 300))
            self.screen.blit(self.players_hands[2][3], (850, 300))
            if self.players == 4:
                self.screen.blit(self.players_hands[3][0], (420, 50))
                self.screen.blit(self.players_hands[3][1], (440, 50))
                self.screen.blit(self.players_hands[3][2], (460, 50))
                self.screen.blit(self.players_hands[3][3], (480, 50))
        elif self.round == 5:
            self.screen.blit(self.players_hands[0][0], (210, 600))
            self.screen.blit(self.players_hands[0][1], (330, 600))
            self.screen.blit(self.players_hands[0][2], (450, 600))
            self.screen.blit(self.players_hands[0][3], (570, 600))
            self.screen.blit(self.players_hands[0][4], (690, 600))
            self.screen.blit(self.players_hands[1][0], (50, 300))
            self.screen.blit(self.players_hands[1][1], (70, 300))
            self.screen.blit(self.players_hands[1][2], (90, 300))
            self.screen.blit(self.players_hands[1][3], (110, 300))
            self.screen.blit(self.players_hands[1][4], (130, 300))
            self.screen.blit(self.players_hands[2][0], (770, 300))
            self.screen.blit(self.players_hands[2][1], (790, 300))
            self.screen.blit(self.players_hands[2][2], (810, 300))
            self.screen.blit(self.players_hands[2][3], (830, 300))
            self.screen.blit(self.players_hands[2][4], (850, 300))
            if self.players == 4:
                self.screen.blit(self.players_hands[3][0], (410, 50))
                self.screen.blit(self.players_hands[3][1], (430, 50))
                self.screen.blit(self.players_hands[3][2], (450, 50))
                self.screen.blit(self.players_hands[3][3], (470, 50))
                self.screen.blit(self.players_hands[3][4], (490, 50))
        elif self.round == 6:
            self.screen.blit(self.players_hands[0][0], (400, 600))
            self.screen.blit(self.players_hands[0][1], (440, 600))
            self.screen.blit(self.players_hands[0][2], (480, 600))
            self.screen.blit(self.players_hands[0][3], (520, 600))
            self.screen.blit(self.players_hands[0][4], (560, 600))
            self.screen.blit(self.players_hands[0][5], (600, 600))
            self.screen.blit(self.players_hands[1][0], (50, 300))
            self.screen.blit(self.players_hands[1][1], (70, 300))
            self.screen.blit(self.players_hands[1][2], (90, 300))
            self.screen.blit(self.players_hands[1][3], (110, 300))
            self.screen.blit(self.players_hands[1][4], (130, 300))
            self.screen.blit(self.players_hands[1][5], (150, 300))
            self.screen.blit(self.players_hands[2][0], (750, 300))
            self.screen.blit(self.players_hands[2][1], (770, 300))
            self.screen.blit(self.players_hands[2][2], (790, 300))
            self.screen.blit(self.players_hands[2][3], (810, 300))
            self.screen.blit(self.players_hands[2][4], (830, 300))
            self.screen.blit(self.players_hands[2][5], (850, 300))
            if self.players == 4:
                self.screen.blit(self.players_hands[3][0], (400, 50))
                self.screen.blit(self.players_hands[3][1], (420, 50))
                self.screen.blit(self.players_hands[3][2], (440, 50))
                self.screen.blit(self.players_hands[3][3], (460, 50))
                self.screen.blit(self.players_hands[3][4], (480, 50))
                self.screen.blit(self.players_hands[3][4], (500, 50))

    def draw_opponents_attempts(self, opponents_attempts):
        """ Drawing how many wins opponents try to get per round """
        text_font = pygame.font.Font(pygame.font.get_default_font(), 20)
        opp_1_text = f"Attempt: {opponents_attempts[0]}"
        opp_2_text = f"Attempt: {opponents_attempts[1]}"
        opp_3_text = f"Attempt: {opponents_attempts[2]}"
        label_1 = text_font.render(opp_1_text, 0, BLACK)
        label_2 = text_font.render(opp_2_text, 0, BLACK)
        label_3 = text_font.render(opp_3_text, 0, BLACK)
        self.screen.blit(label_1, (50, 450))
        self.screen.blit(label_2, (850, 450))
        self.screen.blit(label_3, (450, 200))

    def update_table_after_first_round(self):
        self.screen.fill(GREEN)
        self.show_trump_card()
        self.screen.blit(game_points_text(self.points), (20,15))
        self.draw_letter_buttons(BUTTONS)
        self.screen.blit(self.players_hands[1][0], (50, 300))
        self.screen.blit(self.players_hands[2][0], (850, 300))
        if self.players == 4:
            self.screen.blit(self.players_hands[3][0], (450, 50))

    def game_loop(self):
        """ Game loop """
        opponents_attempts = []
        pygame.init()
        self.screen.fill(GREEN)
        self.screen.blit(game_top_text(), (420, 315))
        pygame.display.update()

        print("\nGame started")
        while self.game_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    clicked_position = event.pos
                    print("clicked_position:", clicked_position)
                    if players_cards[0].collidepoint(clicked_position):
                        self.screen.fill(GREEN)
                        self.show_trump_card()
                        self.screen.blit(game_points_text(self.points), (20, 15))
                        self.draw_opponents_attempts(opponents_attempts)
                        self.draw_letter_buttons(BUTTONS)
                        self.screen.blit(self.players_hands[0][0], (450, 400))
                        self.screen.blit(self.players_hands[1][0], (50, 300))
                        self.screen.blit(self.players_hands[2][0], (850, 300))
                        if self.players == 4:
                            self.screen.blit(self.players_hands[3][0], (450, 50))
                        pygame.display.update()
                        pygame.time.wait(1000)
                        self.screen.fill(GREEN)
                        self.show_trump_card()
                        self.screen.blit(game_points_text(self.points), (20, 15))
                        self.draw_opponents_attempts(opponents_attempts)
                        self.draw_letter_buttons(BUTTONS)
                        self.screen.blit(self.players_hands[0][0], (450, 400))
                        self.screen.blit(self.players_hands[1][0], (400, 300))
                        self.screen.blit(self.players_hands[2][0], (850, 300))
                        if self.players == 4:
                            self.screen.blit(self.players_hands[3][0], (450, 50))
                        pygame.display.update()
                        pygame.time.wait(1000)
                        self.screen.fill(GREEN)
                        self.show_trump_card()
                        self.screen.blit(game_points_text(self.points), (20, 15))
                        self.draw_opponents_attempts(opponents_attempts)
                        self.draw_letter_buttons(BUTTONS)
                        self.screen.blit(self.players_hands[0][0], (450, 400))
                        self.screen.blit(self.players_hands[1][0], (400, 300))
                        self.screen.blit(self.players_hands[2][0], (850, 300))
                        if self.players == 4:
                            self.screen.blit(self.players_hands[3][0], (450, 250))
                        pygame.display.update()
                        pygame.time.wait(1000)
                        self.screen.fill(GREEN)
                        self.show_trump_card()
                        self.screen.blit(game_points_text(self.points), (20, 15))
                        self.draw_opponents_attempts(opponents_attempts)
                        self.draw_letter_buttons(BUTTONS)
                        self.screen.blit(self.players_hands[0][0], (450, 400))
                        self.screen.blit(self.players_hands[1][0], (400, 300))
                        self.screen.blit(self.players_hands[2][0], (500, 300))
                        if self.players == 4:
                            self.screen.blit(self.players_hands[3][0], (450, 250))
                        pygame.display.update()
                        print("mouse over card:", players_cards[0][1])

                if event.type == pygame.MOUSEBUTTONDOWN:
                    clicked_position = event.pos
                    for button, text in BUTTONS:
                        if button.collidepoint(clicked_position):
                            print("collision with text:", text, button)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:
                        opponents_attempts = self.deal_cards()
                        print("opponents_attempts:", opponents_attempts)
                        self.draw_opponents_attempts(opponents_attempts)
            #pygame.draw.rect(self.screen, BLUE, (890,650,100,40))
            #pygame.draw.rect(self.screen, BLUE, (890,700,100,40))
            pygame.display.update()
