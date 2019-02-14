import json
import os
import random
import bottle
import json

from .api import ping_response, start_response, move_response, end_response
from .utils import determine_direction


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
    color = "#00FF00"
    r = lambda: random.randint(0,255)
    color = '#%02X%02X%02X' % (r(),r(),r())
    return start_response(color)


@bottle.post('/move')
def move():
    data = bottle.request.json
    current_direction = determine_direction(data)
    print("Moving %s" % current_direction)
    return move_response(current_direction)


@bottle.post('/end')
def end():
    data = bottle.request.json
    print(json.dumps(data))
    print("Game %s ended" % data["game"]["id"])
    return end_response()

@bottle.post('/ping')
def ping():
    return ''


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=os.getenv('DEBUG', True)
    )
