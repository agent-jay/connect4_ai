import board
import random
import logging
from copy import deepcopy

log_level=logging.INFO

def perft(board, depth):
    board_bk=deepcopy(board)
    # Set up logging
    logging.basicConfig(filename='perft.log',filemode='w',level=log_level)
    logging.debug('STARTING SEARCH')

    fringe=[] #fringe elements (move,depth before move is made)
    depthn_nodes=0
    nodes_visited=0
    init_boarddepth=board.depth()
    # explored={} 
    
    fringe.extend([(move,0) for move in board.generate_moves()])
    while(len(fringe)>0):
        logging.debug('___________')
        logging.debug(board)
        logging.debug("MOVE hist:"+str(board.move_hist))
        logging.debug("FRINGE:"+str(fringe))
        logging.debug("DEPTH "+str(depth)+" Leaf Nodes:"+ str(depthn_nodes))
        logging.debug("Nodes visited:"+str(nodes_visited))
        if nodes_visited%10000==0:
            print(nodes_visited, depthn_nodes)

        move,move_depth=fringe.pop()
        while board.depth()-init_boarddepth>move_depth:
            board.unmake_last_move()

        board.make_move(move)
        current_depth=board.depth()-init_boarddepth

        if current_depth==depth:
            depthn_nodes+=1
            nodes_visited+=1
            continue
        elif board.last_move_won()==True:
            logging.debug("This move wins!!!")
            depthn_nodes+=1
            nodes_visited+=1
            continue
        else:
            #Expanding nodes
            nodes_visited+=1
            fringe.extend([(move,current_depth) for move in board.generate_moves()])

    print("Number of leaf nodes at ",depth," :",depthn_nodes)
    board=board_bk
    return depthn_nodes
              

def find_win(board, depth):
  pass



