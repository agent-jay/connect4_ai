import board
import random
import logging
import time

def perft(board, depth):
    if depth==0:
        return 1
    if board.last_move_won():
        return 1
    if board.is_full():
        return 1
    count=0
    for move in board.generate_moves():
        board.make_move(move)
        count+= perft(board, depth-1)
        board.unmake_last_move()
    return count


    
def find_win(board, depth):
    values=[]
    for move in board.generate_moves():
        board.make_move(move)
        values.append((minimax(board,depth-1,maxplayer=False),move))
        board.unmake_last_move()
    minimax_value=max(values)
    if minimax_value[0]>0:
        # print("WIN BY PLAYING %s"% minimax_value[1])
        return "WIN BY PLAYING %s"% minimax_value[1]
    elif minimax_value[0]<0:
        # print("ALL MOVES LOSE")
        return "ALL MOVES LOSE"
    else:
        # print("NO FORCED WIN IN %s MOVES"%depth)
        return "NO FORCED WIN IN %s MOVES"%depth

def minimax(board,depth, maxplayer):
    if board.last_move_won():
        if maxplayer==True:
            return -100
        else :
            return +100
    
    if depth==0 or board.is_full():
        return 0 

    values=[]
    for move in board.generate_moves():
        board.make_move(move)
        values.append(minimax(board,depth-1, not maxplayer))
        board.unmake_last_move()
    #If maximizing player
    if maxplayer==True:
        return max(values)
    #if minimizing player
    else:
        return min(values)
