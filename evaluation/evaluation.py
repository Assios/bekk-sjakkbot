import chess
import random
from pprint import pprint
from .piece_square_tables import pst

cols = "ABCDEFGH"
rows = "12345678"

def create_fields():
	return [(col + row) for col in cols for row in rows]

fields = create_fields()

def field_to_coords(field):
    x, y = field[0], field[1]

    col = "ABCDEFGH".find(x)
    row = 8 - int(y)

    return(row,col) 


def evaluate(node):
    return random.random()
