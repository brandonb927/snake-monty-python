import json
import os
import random
import bottle
import json

from api import ping_response, start_response, move_response, end_response

@bottle.route('/')
def index():
    return '''
    Battlesnake documentation can be found at
       <a href="https://docs.battlesnake.io">https://docs.battlesnake.io</a>.
    '''

@bottle.route('/static/<path:path>')
def static(path):
    """
    Given a path, return the static file located relative
    to the static folder.

    This can be used to return the snake head URL in an API response.
    """
    return bottle.static_file(path, root='static/')

@bottle.post('/ping')
def ping():
    """
    A keep-alive endpoint used to prevent cloud application platforms,
    such as Heroku, from sleeping the application instance.
    """
    return ping_response()

@bottle.post('/start')
def start():
    data = bottle.request.json

    """
    TODO: If you intend to have a stateful snake AI,
            initialize your snake state here using the
            request's data if necessary.
    """
    print(json.dumps(data))

    color = "#00FF00"

    return start_response(color)


@bottle.post('/move')
def move():
    data = bottle.request.json

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
        current_direction = 'right'

    # Bottom left corner
    elif head['y'] == board_height - 1 and head['x'] == 0:
        current_direction = 'up'

    # Top right corner
    elif head['y'] == 0 and head['x'] == board_width - 1:
        current_direction = 'down'

    # Bottom right corner
    elif head['y'] == board_height - 1 and head['x'] == board_width - 1:
        current_direction = 'left'


    # WALLS

    # Top wall
    elif head['y'] == 0 and head['x'] in range(0, board_width):
        current_direction = 'right'

    # Right wall
    elif head['y'] in range(0, board_height) and head['x'] == board_width - 1:
        current_direction = 'down'

    # Bottom wall
    elif head['y'] == board_height - 1 and head['x'] in range(0, board_width):
        current_direction = 'left'

    # Left wall
    elif head['y'] in range(0, board_height) and head['x'] == 0:
        current_direction = 'up'

    else:
        # Always go up, default
        current_direction = 'up'

    print "Moving %s" % current_direction
    return move_response(current_direction)


@bottle.post('/end')
def end():
    data = bottle.request.json

    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """
    print(json.dumps(data))

    return end_response()

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=os.getenv('DEBUG', True)
    )
