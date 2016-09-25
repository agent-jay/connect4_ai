import board
import random
import logging

def diag_dump(board,fringe,current_depth):
    print("\n____DIAGNOSTIC____")
    board.diagnostic()
    print(fringe)
    print(current_depth)
    

def perft(board, depth):
    # Set up logging
    logging.basicConfig(filename='search.log',filemode='w',level=logging.ERROR)
    logging.debug('STARTING SEARCH')

    fringe=[] #fringe elements (move,depth before move is made)
    depthn_nodes=0
    nodes_visited=0
    # explored={} 
    
    fringe.extend([(move,0) for move in board.generate_moves()])
    while(len(fringe)>0):
        logging.debug('___________')
        logging.debug(board)
        logging.debug("MOVE hist:"+str(board.move_hist))
        logging.debug("FRINGE:"+str(fringe))
        logging.debug("DEPTH "+str(depth)+" Leaf Nodes:"+ str(depthn_nodes))
        logging.debug("Nodes visited:"+str(nodes_visited))
        if nodes_visited%1000==0:
            print(nodes_visited, depthn_nodes)

        move,move_depth=fringe.pop()
        while board.depth()>move_depth:
            board.unmake_last_move()

        board.make_move(move)
        current_depth=board.depth()

        if current_depth==depth:
            # print("HERE1")
            depthn_nodes+=1
            nodes_visited+=1
            continue
        elif board.last_move_won()==True:
            diag_dump(board,fringe,current_depth)
            quit(1)
            nodes_visited+=1
            continue
        else:
            #Expanding nodes
            nodes_visited+=1
            fringe.extend([(move,current_depth) for move in board.generate_moves()])

    print("Number of leaf nodes at ",depth," :",depthn_nodes)
    return depthn_nodes
              
#b=board.Board()
#perft(b, 5) 
        
    

def find_win(board, depth):
  pass



