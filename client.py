import socketio
import threading
from game_mechanics import *

class ClientHandler():
    def __init__(self):
        self.player_turn_id = 0
        self.USER_NAME = 'brolius'
        self.TOURNAMENT_ID = 12
        self.mode = 'ALPHA_BETA'    # or 'RANDOM'

# White: 2
# Black: 1

client = ClientHandler()

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
    print('Game: ' + str(data['game_id']) + ', Movement: ' + str(data['movementNumber']) + ', Color: ' + str(data['player_turn_id']))
    move = None

    if client.mode == 'ALPHA_BETA':
        move = make_a_move(data['board'], data['player_turn_id'])
    
    if client.mode == 'RANDOM':
        moves = get_possibilities(data['board'], data['player_turn_id'])
        move = select_first_possibility(moves)  

    client.player_turn_id = data['player_turn_id']

    emit_play(
        client.player_turn_id,
        client.TOURNAMENT_ID,
        data['game_id'],
        move
    )

@socket.on('finish')
def finish(data):    
    game_id = data['game_id']
    winner_turn_id = 0
    if data.has_key('winner_turn_id'):
        winner_turn_id = data['winner_turn_id']
    # player_turn_id = data['player_turn_id']
    board = data['board']

    print('Finished game: ' + str(game_id) + ', Winner: ' + str(winner_turn_id))    
    show_board(board)

    emit_player_ready(client.player_turn_id, game_id)

# emit signals
def emit_sign_in():
    user_name = raw_input('Please provide a username: ')    
    mode = raw_input('Select a mode: 1. Minimax with Alpha Beta 2. Random choice ')
    client.mode = 'ALPHA_BETA' if mode == '1' else 'RANDOM'

    socket.emit('signin', {
        'user_name': user_name if user_name != '' else client.USER_NAME,
        'tournament_id': client.TOURNAMENT_ID,
        'user_role': 'player'
    })

    x = threading.Thread(target=disconnect_user_signal)
    x.start()

def emit_play(player_turn_id, tournament_id, game_id, movement):
    socket.emit('play', {
        'player_turn_id': player_turn_id,
        'tournament_id': tournament_id,
        'game_id': game_id,
        'movement': movement
    })

def emit_player_ready(player_turn_id, game_id):
    socket.emit('player_ready', {
        'tournament_id': client.TOURNAMENT_ID,
        'player_turn_id': player_turn_id,
        'game_id': game_id
    })

def disconnect_user_signal():
    signal = raw_input('')
    if (signal == '*'):
        print('User logging out')
        socket.disconnect()

# connect to server
socket.connect('http://localhost:4000')