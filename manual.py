import time
import random
import board

inf=1000

class Player:
    def __init__(self):
        self.b=board.Board()

    def name(self):
        return 'Manual'

    def make_move(self, move):
        self.b.make_move(move)

    def get_move(self):
        mv= int(input("Input num from 0-6:"))
        if mv in range(7):
            return mv
    

