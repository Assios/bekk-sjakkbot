import requests
import json
import multiprocessing
from multiprocessing import Pool
import engine
import logging_pool
import chess
from keys import TOKEN, BOT_ID
from engine import *
import random
import chess.variant
import random

BASE_URL = 'https://lichess.org/'

headers = {'Authorization': 'Bearer %s' % TOKEN}

def time_to_depth(time):
	"""
	time er gjenstående tid i millisekunder
	depth (returverdien) er antall halvtrekk boten skal regne fremover
	
	"""

	return 2

def accept_challenge(game_id):
	#curl -H "Authorization: Bearer rSRtCAEFhYAYd66z" https://lichess.org/api/challenge/gdksij27/accept -X POST
	print('ACCEPTING_CHALLENGE')
	response = requests.post('https://lichess.org/api/challenge/%s/accept' % (game_id), headers=headers)
	print('RESPONSE')
	print(response)
	return response.json()

def make_move(game_id, move):
	response = requests.post('https://lichess.org/api/bot/game/%s/move/%s' % (game_id, move), headers=headers)
	return response.json()

def game_updates(game_id):
	response = requests.get('https://lichess.org/api/bot/game/stream/%s' % (game_id), headers=headers, stream=True)
	return response

def bot_upgrade():
	response = requests.post(BASE_URL + 'bot/account/upgrade', headers=headers)
	return response.json()

def stream_events(event_queue):
	response = requests.get(BASE_URL + 'api/stream/event', headers=headers, stream=True)

	for event in response.iter_lines():
		if event:
			event_queue.put_nowait(json.loads(event.decode('utf-8')))
		else:
			event_queue.put_nowait({'type': 'ping'})

def play_game(game_id, event_queue):
	start_color = 1
	my_time = 'btime'
	game_stream = game_updates(game_id).iter_lines()

	print('GAME_STREAM')
	print(game_stream)

	game = json.loads(next(game_stream).decode('utf-8'))

	board = chess.Board()

	if game['white']['id'] == BOT_ID.lower():
		start_color = -1
		my_time = 'wtime'

		bot_move = search(board, color=-start_color, depth=3)

		print("BOT")
		print(bot_move)

		make_move(game_id, bot_move)

	for event in game_stream:
		upd = json.loads(event.decode('utf-8')) if event else None
		_type = upd['type'] if upd else 'ping'
		if (_type == 'gameState'):
			last_move = upd['moves'].split(' ')[-1]
			last_move = chess.Move.from_uci(last_move)
			board.push(last_move)

			moves = upd['moves'].split(' ')

			bot_move = search(board, color=-start_color, depth=time_to_depth(upd[my_time]))

			print(bot_move)

			make_move(game_id, bot_move)

if __name__ == '__main__':
	manager = multiprocessing.Manager()
	challenge_queue = []
	event_queue = manager.Queue()

	control_stream = multiprocessing.Process(target=stream_events, args=[event_queue])
	control_stream.start()

	with logging_pool.LoggingPool(10) as pool:
		while True:
			event = event_queue.get()

			print("EVENT")
			print(event)

			if (event['type'] == 'challenge') and (event['challenge']['variant']['key'] == 'standard'):
				_id = event['challenge']['id'].strip()

				accept_challenge(_id)
			elif event['type'] == 'gameStart':
				game_id = event['game']['id']
				pool.apply_async(play_game, [game_id, event_queue])

	control_stream.terminate()
	control_stream.join()

