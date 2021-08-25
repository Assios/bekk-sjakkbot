import chess
import time
from evaluation.evaluation import *
import random
import pprint
import chess.variant

inf = float('inf')
poscount = 0

DEPTH=2

def search(node, color, depth):
	moves = list(node.legal_moves)

	if not moves:
		print('Game over.')
		return

	move = negamax(node, -inf, inf, color, depth)[1]

	if not move:
		print("NO MOVES")
		return random.choice(moves)
	else:
		return move

def negamax(node, a, b, color, depth=DEPTH):
	global poscount

	if (depth == 0) or (node.is_variant_end()):
		return (evaluate(node) * color, None)

	moves = list(node.legal_moves)

	best_move = None
	best_value = -inf

	for move in moves:
		poscount+=1

		node.push(move)
		result = negamax(node, -b, -a, -color, depth-1)
		value = -result[0]
		node.pop()
		if value > best_value:
			best_value = value
			best_move = move

		a = max(a, value)

		if a >= b:
			break

	return (best_value, best_move)


if __name__ == "__main__":
	board = chess.Board()
	moves = []

	c = 0
	while not board.is_game_over():
		print(board)

		if c%2==0:
			move = input("move: \n\n")
			move = chess.Move.from_uci(move)
			if not move in board.legal_moves:
				continue
		else:
			start_time = time.time()

			(value, move) = negamax(board, -inf, inf, -1, DEPTH)
			print(move)

			elapsed = time.time() - start_time
			print("--- %s moves ---" % (len(list(board.legal_moves))))
			print("--- number of nodes: %s --" % poscount)
			print("--- %s seconds ---" % (elapsed))
			print("--- nodes per second: %s ---" % str(poscount / elapsed))

		print(move)
		moves.append(str(move))
		board.push(move)
		c+=1
