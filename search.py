import board
import random
import logging
import time

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

state_val_lookup={} #should be refreshed every move

def negamax(board,depth):
    if board.last_move_won():
        if board.last_player==1:
            return -100
        else :
            return +100
    
    if depth==0:
        return 0 #Why 0 as an evaluation

    values=[]
    for move in board.generate_moves():
        board.make_move(move)
        #str_board= str(board)
        # if str_board in state_val_lookup:
            # values.append(state_val_lookup[str_board])
        # else:       
        val=-negamax(board,depth-1)
        values.append(val)
        #state_val_lookup[str_board]=val
        board.unmake_last_move()
    return max(values)

    
def find_win(board, depth):
    if board.last_move_won():
        if board.last_player==1:
            return "PLAYER 1 ALREADY WON"
        else:
            return "PLAYER 2 ALREADY WON"
    values=[]
    for move in board.generate_moves():
        board.make_move(move)
        values.append((-negamax(board,depth-1), move))
        board.unmake_last_move()
    minimax_value=max(values)
    if minimax_value[0]>0:
        print("WIN BY PLAYING %s"% minimax_value[1])
        return "WIN BY PLAYING %s"% minimax_value[1]
    elif minimax_value[0]<0:
        print("ALL MOVES LOSE")
        return "ALL MOVES LOSE"
    else:
        print("NO FORCED WIN IN %s MOVES"%depth)
        return "NO FORCED WIN IN %s MOVES"%depth

b=board.Board()
start=time.clock()
#print(perft(b,8))
#find_win(b,8)
print(time.clock()-start)
