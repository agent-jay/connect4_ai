import board
import random
import logging
import time

depth=0
def perft(board, depth):
    if depth==0:
        return 1
    if board.last_move_won():
        return 1
    count=0
    for move in board.generate_moves():
        board.make_move(move)
        count+= perft(board, depth-1)
        board.unmake_last_move()
    return count

def find_win(board, depth):
  pass



