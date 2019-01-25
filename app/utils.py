import math
import itertools
import numpy as np


DIR_U = 'up'
DIR_D = 'down'
DIR_L = 'left'
DIR_R = 'right'

MIN_HEALTH = 50


def determine_direction(data):
    # print data
    board = data['board']
    board_width = data['board']['width']
    board_height = data['board']['height']
    food = data['board']['food']
    turn = data['turn']

    health = data['you']['health']
    whole_body = data['you']['body']

    head = whole_body[0]
    body = whole_body[1:]

    direction = 'up'

    # CORNERS

    if head['x'] == 0 and head['y'] == 0:
        direction = DIR_R

    # Bottom left corner
    elif head['x'] == 0 and head['y'] == board_height - 1:
        direction = DIR_U

    # Top right corner
    elif head['x'] == board_width - 1 and head['y'] == 0:
        direction = DIR_D

    # Bottom right corner
    elif head['x'] == board_width - 1 and head['y'] == board_height - 1:
        direction = DIR_L

    # WALLS

    # Top wall
    elif head['x'] in range(0, board_width) and head['y'] == 0 :
        direction = DIR_R

    # Right wall
    elif head['x'] == board_width - 1 and head['y'] in range(0, board_height) :
        direction = DIR_D

    # Bottom wall
    elif head['x'] in range(0, board_width) and head['y'] == board_height - 1 :
        direction = DIR_L

    # Left wall
    elif head['x'] == 0 and head['y'] in range(0, board_height) :
        direction = DIR_U

    # FOOD DETECTION

    if health < MIN_HEALTH:
        closest_food = find_closest_food_coord(whole_body, food)

        # same row as food
        if head['x'] == closest_food['x']:
            # same column as food
            if head['y'] < closest_food['y']:
                direction = DIR_D
            else:
                direction = DIR_U

        # same column as food
        elif head['y'] == closest_food['y']:
            # same row as food
            if head['x'] < closest_food['x']:
                direction = DIR_R
            else:
                direction = DIR_L

    return direction


def find_closest_food_coord(body, food):
    points = [tup for tup in itertools.product([body[0]], food)]
    return points[np.argmin([distance_between_points(Pa, Pb) for (Pa, Pb) in points])][1]


def distance_between_points(p1, p2):
    return math.hypot(p2['x'] - p1['x'], p2['y'] - p1['y'])
