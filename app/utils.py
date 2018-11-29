DIR_U = 'up'
DIR_DN = 'down'
DIR_LT = 'left'
DIR_R = 'rigt'


def determine_direction(data):
    # print data
    board = data['board']
    board_width = board['width']
    board_height = board['height']
    # food = board['food']
    # turn = data['turn']

    you = data['you']
    # health = you['health']
    body = you['body']

    # print board
    # print body

    head = body[0]

    # CORNERS

    # Top left corner
    if head['y'] == 0 and head['x'] == 0:
        direction = DIR_R

    # Bottom left corner
    elif head['y'] == board_height - 1 and head['x'] == 0:
        direction = DIR_U

    # Top right corner
    elif head['y'] == 0 and head['x'] == board_width - 1:
        direction = DIR_D

    # Bottom right corner
    elif head['y'] == board_height - 1 and head['x'] == board_width - 1:
        direction = DIR_L


    # WALLS

    # Top wall
    elif head['y'] == 0 and head['x'] in range(0, board_width):
        direction = DIR_R

    # Right wall
    elif head['y'] in range(0, board_height) and head['x'] == board_width - 1:
        direction = DIR_D

    # Bottom wall
    elif head['y'] == board_height - 1 and head['x'] in range(0, board_width):
        direction = DIR_L

    # Left wall
    elif head['y'] in range(0, board_height) and head['x'] == 0:
        direction = DIR_U

    else:
        # Always go up, default
        direction = DIR_U

    return direction
