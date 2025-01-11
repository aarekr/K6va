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
opponents_attempts = []  # how many wins opponents plan to get during a round
played_cards = []
playing_order = []       # player, opp1, (opp3), opp2

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

    def draw_buttons(self, BUTTONS):
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
        self.screen.blit(game_round_text(self.round), (20, 15))
        self.screen.blit(game_points_text(self.points), (20, 50))
        self.draw_buttons(BUTTONS)
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

        opponent_3_hand_value = 0
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
        x_coord = player_card_x_coordinates(self.round)
        x_coord_opp_1 = get_opp_1_x_coord(self.round)
        x_coord_opp_2 = get_opp_2_x_coord(self.round)
        if self.round == 1:
            for i in range(self.round):
                self.screen.blit(self.players_hands[0][i], (x_coord[i], 600))
            card = pygame.Rect(450, 600, 100, 130)
            players_cards.append(card)
            for i in range(self.round):
                self.screen.blit(self.players_hands[1][i], (x_coord_opp_1[i], 300))
            for i in range(self.round):
                self.screen.blit(self.players_hands[2][i], (x_coord_opp_2[i], 300))
            if self.players == 4:
                for i in range(self.round):
                    self.screen.blit(self.players_hands[3][i], (x_coord[i], 50))
        elif self.round == 2:
            for i in range(self.round):
                self.screen.blit(self.players_hands[0][i], (x_coord[i], 600))
            card = pygame.Rect(390, 600, 100, 130)
            players_cards.append(card)
            card = pygame.Rect(510, 600, 100, 130)
            players_cards.append(card)
            for i in range(self.round):
                self.screen.blit(self.players_hands[1][i], (x_coord_opp_1[i], 300))
            for i in range(self.round):
                self.screen.blit(self.players_hands[2][i], (x_coord_opp_2[i], 300))
            if self.players == 4:
                for i in range(self.round):
                    self.screen.blit(self.players_hands[3][i], (x_coord[i], 50))
        elif self.round == 3:
            for i in range(self.round):
                self.screen.blit(self.players_hands[0][i], (x_coord[i], 600))
            for i in range(self.round):
                self.screen.blit(self.players_hands[1][i], (x_coord_opp_1[i], 300))
            for i in range(self.round):
                self.screen.blit(self.players_hands[2][i], (x_coord_opp_2[i], 300))
            if self.players == 4:
                for i in range(self.round):
                    self.screen.blit(self.players_hands[3][i], (x_coord[i], 50))
        elif self.round == 4:
            for i in range(self.round):
                self.screen.blit(self.players_hands[0][i], (x_coord[i], 600))
            for i in range(self.round):
                self.screen.blit(self.players_hands[1][i], (x_coord_opp_1[i], 300))
            for i in range(self.round):
                self.screen.blit(self.players_hands[2][i], (x_coord_opp_2[i], 300))
            if self.players == 4:
                for i in range(self.round):
                    self.screen.blit(self.players_hands[3][i], (x_coord[i], 50))
        elif self.round == 5:
            for i in range(self.round):
                self.screen.blit(self.players_hands[0][i], (x_coord[i], 600))
            for i in range(self.round):
                self.screen.blit(self.players_hands[1][i], (x_coord_opp_1[i], 300))
            for i in range(self.round):
                self.screen.blit(self.players_hands[2][i], (x_coord_opp_2[i], 300))
            if self.players == 4:
                for i in range(self.round):
                    self.screen.blit(self.players_hands[3][i], (x_coord[i], 50))
        elif self.round == 6:
            for i in range(self.round):
                self.screen.blit(self.players_hands[0][i], (x_coord[i], 600))
            for i in range(self.round):
                self.screen.blit(self.players_hands[1][i], (x_coord_opp_1[i], 300))
            for i in range(self.round):
                self.screen.blit(self.players_hands[2][i], (x_coord_opp_2[i], 300))
            if self.players == 4:
                for i in range(self.round):
                    self.screen.blit(self.players_hands[3][i], (x_coord[i], 50))
        elif self.round == 7:
            for i in range(self.round):
                self.screen.blit(self.players_hands[0][i], (x_coord[i], 600))
            for i in range(self.round):
                self.screen.blit(self.players_hands[1][i], (x_coord_opp_1[i], 300))
            for i in range(self.round):
                self.screen.blit(self.players_hands[2][i], (x_coord_opp_2[i], 300))
            if self.players == 4:
                for i in range(self.round):
                    self.screen.blit(self.players_hands[3][i], (x_coord[i], 50))
        elif self.round == 8:
            for i in range(self.round):
                self.screen.blit(self.players_hands[0][i], (x_coord[i], 600))
            for i in range(self.round):
                self.screen.blit(self.players_hands[1][i], (x_coord_opp_1[i], 300))
            for i in range(self.round):
                self.screen.blit(self.players_hands[2][i], (x_coord_opp_2[i], 300))
            if self.players == 4:
                for i in range(self.round):
                    self.screen.blit(self.players_hands[3][i], (x_coord[i], 50))
        elif self.round == 9:
            for i in range(self.round):
                self.screen.blit(self.players_hands[0][i], (x_coord[i], 600))
            for i in range(self.round):
                self.screen.blit(self.players_hands[1][i], (x_coord_opp_1[i], 300))
            for i in range(self.round):
                self.screen.blit(self.players_hands[2][i], (x_coord_opp_2[i], 300))
            if self.players == 4:
                for i in range(self.round):
                    self.screen.blit(self.players_hands[3][i], (x_coord[i], 50))
        elif self.round == 10:
            for i in range(self.round):
                self.screen.blit(self.players_hands[0][i], (x_coord[i], 600))
            for i in range(self.round):
                self.screen.blit(self.players_hands[1][i], (x_coord_opp_1[i], 300))
            for i in range(self.round):
                self.screen.blit(self.players_hands[2][i], (x_coord_opp_2[i], 300))
            if self.players == 4:
                for i in range(self.round):
                    self.screen.blit(self.players_hands[3][i], (x_coord[i], 50))
        elif self.round == 11:
            for i in range(self.round):
                self.screen.blit(self.players_hands[0][i], (x_coord[i], 600))
            for i in range(self.round):
                self.screen.blit(self.players_hands[1][i], (x_coord_opp_1[i], 300))
            for i in range(self.round):
                self.screen.blit(self.players_hands[2][i], (x_coord_opp_2[i], 300))
            if self.players == 4:
                for i in range(self.round):
                    self.screen.blit(self.players_hands[3][i], (x_coord[i], 50))
        elif self.round == 12:
            for i in range(self.round):
                self.screen.blit(self.players_hands[0][i], (x_coord[i], 600))
            for i in range(self.round):
                self.screen.blit(self.players_hands[1][i], (x_coord_opp_1[i], 300))
            for i in range(self.round):
                self.screen.blit(self.players_hands[2][i], (x_coord_opp_2[i], 300))
            if self.players == 4:
                for i in range(self.round):
                    self.screen.blit(self.players_hands[3][i], (x_coord[i], 50))

    def draw_player_attempt(self):
        # player's attempt
        base_font = pygame.font.Font(None, 32)
        user_text = ''
        input_rect = pygame.Rect(200, 700, 50, 32)
        color_active = pygame.Color('lightskyblue3')
        color_passive = pygame.Color('chartreuse4') 
        color = color_passive
        attempt_entered = False
        read_input = True
        active = False
        while (read_input is True):
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN: 
                    if input_rect.collidepoint(event.pos): 
                        active = True
                    else:
                        active = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        print("RETURN")
                        attempt_entered = True
                        read_input = False
                        break
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        user_text += event.unicode
                        print("else")
            if active:
                color = color_active
            else:
                color = color_passive
            if attempt_entered == True:
                break
            pygame.draw.rect(self.screen, color, input_rect)
            text_surface = base_font.render(user_text, True, (255, 255, 255))
            self.screen.blit(text_surface, (input_rect.x+5, input_rect.y+5))
            input_rect.w = max(100, text_surface.get_width()+10)
            pygame.display.flip()
        print("exited while")

    def draw_attempts(self, opponents_attempts):
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
        self.screen.blit(game_round_text(self.round), (20, 15))
        self.screen.blit(game_points_text(self.points), (20, 50))
        self.draw_buttons(BUTTONS)
        self.screen.blit(self.players_hands[1][0], (50, 300))
        self.screen.blit(self.players_hands[2][0], (850, 300))
        if self.players == 4:
            self.screen.blit(self.players_hands[3][0], (450, 50))

    def move_cards_to_center(self, opponents_attempts):
        """ Moving chosen cards to the table center """
        self.screen.blit(self.players_hands[0][0], (450, 400))
        self.screen.blit(self.players_hands[1][0], (50, 300))
        self.screen.blit(self.players_hands[2][0], (850, 300))
        if self.players == 4:
            self.screen.blit(self.players_hands[3][0], (450, 50))
        pygame.display.update()
        pygame.time.wait(1000)
        self.screen.fill(GREEN)
        self.show_trump_card()
        self.screen.blit(game_round_text(self.round), (20, 15))
        self.screen.blit(game_points_text(self.points), (20, 50))
        self.draw_attempts(opponents_attempts)
        self.draw_buttons(BUTTONS)
        self.screen.blit(self.players_hands[0][0], (450, 400))
        self.screen.blit(self.players_hands[1][0], (400, 300))
        self.screen.blit(self.players_hands[2][0], (850, 300))
        if self.players == 4:
            self.screen.blit(self.players_hands[3][0], (450, 50))
        pygame.display.update()
        pygame.time.wait(1000)
        self.screen.fill(GREEN)
        self.show_trump_card()
        self.screen.blit(game_round_text(self.round), (20, 15))
        self.screen.blit(game_points_text(self.points), (20, 50))
        self.draw_attempts(opponents_attempts)
        self.draw_buttons(BUTTONS)
        self.screen.blit(self.players_hands[0][0], (450, 400))
        self.screen.blit(self.players_hands[1][0], (400, 300))
        self.screen.blit(self.players_hands[2][0], (850, 300))
        if self.players == 4:
            self.screen.blit(self.players_hands[3][0], (450, 250))
        pygame.display.update()
        pygame.time.wait(1000)
        self.screen.fill(GREEN)
        self.show_trump_card()
        self.screen.blit(game_round_text(self.round), (20, 15))
        self.screen.blit(game_points_text(self.points), (20, 50))
        self.draw_attempts(opponents_attempts)
        self.draw_buttons(BUTTONS)
        self.screen.blit(self.players_hands[0][0], (450, 400))
        self.screen.blit(self.players_hands[1][0], (400, 300))
        self.screen.blit(self.players_hands[2][0], (500, 300))
        if self.players == 4:
            self.screen.blit(self.players_hands[3][0], (450, 250))
        pygame.display.update()
        print("mouse over card:", players_cards[0][1])

    def check_who_won(self):
        print("checking who won:", self.players_hands)

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
                """if players_cards != []:
                    mouse_position = pygame.mouse.get_pos()
                    if players_cards[0].collidepoint(mouse_position):
                        print("mouse position:", mouse_position)"""
                if event.type == pygame.MOUSEBUTTONDOWN:
                    clicked_position = event.pos
                    print("clicked_position:", clicked_position)
                    if players_cards[0].collidepoint(clicked_position):
                        print("mouse over card")
                        self.screen.fill(GREEN)
                        self.show_trump_card()
                        self.screen.blit(game_round_text(self.round), (20, 15))
                        self.screen.blit(game_points_text(self.points), (20, 50))
                        self.draw_attempts(opponents_attempts)
                        self.draw_buttons(BUTTONS)
                        self.move_cards_to_center(opponents_attempts)
                        self.check_who_won()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    clicked_position = event.pos
                    for button, text in BUTTONS:
                        if button.collidepoint(clicked_position):
                            print("collision with text:", text, button)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:
                        opponents_attempts = self.deal_cards()
                        self.draw_player_attempt()
                        print("opponents_attempts:", opponents_attempts)
                        self.draw_attempts(opponents_attempts)
            #pygame.draw.rect(self.screen, BLUE, (890,650,100,40))
            #pygame.draw.rect(self.screen, BLUE, (890,700,100,40))
            pygame.display.update()
