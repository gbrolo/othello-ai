import socketio
from game_mechanics import *

# White: 2
# Black: 1

USER_NAME = 'brolius'
TOURNAMENT_ID = 12

# define socket
socket = socketio.Client()

# define handlers
@socket.on('connect')
def on_connect():
    emit_sign_in()
    print('Connection succesfull')    

@socket.on('disconnect')
def on_disconnect():
    print('Disconnected')
    socket.disconnect()

@socket.on('ok_signin')
def on_ok_signin():
    print('Login succesfull') 

@socket.on('ready')
def on_ready(data):
    print('Ready signal received')
    print('data received: ', data)

    moves = get_possibilities(data['board'], data['player_turn_id'])
    move = select_first_possibility(moves)    

    emit_play(
        data['player_turn_id'],
        TOURNAMENT_ID,
        data['game_id'],
        move
    )

@socket.on('finish')
def finish(data):
    print('finish data: ', data)
    game_id = data['game_id']
    winner_turn_id = 0
    if data.has_key('winner_turn_id'):
        winner_turn_id = data['winner_turn_id']
    player_turn_id = data['player_turn_id']
    board = data['board']

    print('Finished game: ', game_id)
    print('Winner, player: ', winner_turn_id)
    show_board(board)

    emit_player_ready(player_turn_id, game_id)

# emit signals
def emit_sign_in():
    user_name = raw_input('Please provide a username: ')    
    socket.emit('signin', {
        'user_name': user_name if user_name != '' else USER_NAME,
        'tournament_id': TOURNAMENT_ID,
        'user_role': 'player'
    })

def emit_play(player_turn_id, tournament_id, game_id, movement):
    socket.emit('play', {
        'player_turn_id': player_turn_id,
        'tournament_id': tournament_id,
        'game_id': game_id,
        'movement': movement
    })

def emit_player_ready(player_turn_id, game_id):
    socket.emit('player_ready', {
        'tournament_id': TOURNAMENT_ID,
        'player_turn_id': player_turn_id,
        'game_id': game_id
    })

# connect to server
socket.connect('http://localhost:4000')