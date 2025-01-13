""" Helper functions and variables for the UI class """

import pygame

RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

PLAYER_AND_OPP_3_X_COORDINATES_LIST = [[450], [440, 460], [430, 450, 470], [420, 440, 460, 480],
    [410, 430, 450, 470, 490], [400, 420, 440, 460, 480, 500], [390, 410, 430, 450, 470, 490, 510],
    [380, 400, 420, 440, 460, 480, 500, 520], [370, 390, 410, 430, 450, 470, 490, 510, 530],
    [360, 380, 400, 420, 440, 460, 480, 500, 520, 540],
    [350, 370, 390, 410, 430, 450, 470, 490, 510, 530, 550],
    [340, 360, 380, 400, 420, 440, 460, 480, 500, 520, 540, 560]]

OPP_1_X_COORDINATES_LIST = [[50], [50, 70], [50, 70, 90], [50, 70, 90, 110], [50, 70, 90, 110, 130],
    [50, 70, 90, 110, 130, 150], [50, 70, 90, 110, 130, 150, 170],
    [50, 70, 90, 110, 130, 150, 170, 190], [50, 70, 90, 110, 130, 150, 170, 190, 210],
    [50, 70, 90, 110, 130, 150, 170, 190, 210, 230],
    [50, 70, 90, 110, 130, 150, 170, 190, 210, 230, 250],
    [50, 70, 90, 110, 130, 150, 170, 190, 210, 230, 250, 270]]

OPP_2_X_COORDINATES_LIST = [[850], [830, 850], [810, 830, 850], [790, 810, 830, 850],
    [770, 790, 810, 830, 850], [750, 770, 790, 810, 830, 850], [730, 750, 770, 790, 810, 830, 850],
    [710, 730, 750, 770, 790, 810, 830, 850], [690, 710, 730, 750, 770, 790, 810, 830, 850],
    [670, 690, 710, 730, 750, 770, 790, 810, 830, 850],
    [650, 670, 690, 710, 730, 750, 770, 790, 810, 830, 850],
    [630, 650, 670, 690, 710, 730, 750, 770, 790, 810, 830, 850]]

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

def game_points_text(points):
    """ Displaying how many total points the player has """
    text_font = pygame.font.Font(pygame.font.get_default_font(), 25)
    game_points = f"Points: {points}"
    label = text_font.render(game_points, 0, BLACK)
    return label

def game_round_text(round):
    """ Displaying what round is played """
    text_font = pygame.font.Font(pygame.font.get_default_font(), 30)
    round = f"Round: {round}"
    label = text_font.render(round, 0, BLACK)
    return label

def box_text(letter):
    """ Drawing texts in buttons """
    button_font = pygame.font.Font(pygame.font.get_default_font(), 20)
    label = button_font.render(letter, True, BLACK)
    return label

def player_card_x_coordinates(round):
    return PLAYER_AND_OPP_3_X_COORDINATES_LIST[round - 1]

def get_opp_1_x_coord(round):
    return OPP_1_X_COORDINATES_LIST[round - 1]

def get_opp_2_x_coord(round):
    return OPP_2_X_COORDINATES_LIST[round - 1]

TEXT_BOXES = []
for row in range(2):
    for column in range(1):
        X = 850
        y = 60 * row + 630
        box = pygame.Rect(X, y, 120, 40)
        TEXT_BOXES.append(box)

BUTTONS = []
BUTTON_TEXTS = ["FIRST", "SECOND"]
for index, box in enumerate(TEXT_BOXES):
    text = BUTTON_TEXTS[index]
    button = ([box, text])
    BUTTONS.append(button)

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
print("CARD_LIST length: ", len(CARD_LIST))
