import time
import random
import board

inf=1000

class Player:
    def __init__(self):
        self.b=board.Board()
        self.eval_table=[[3,4,5,7,5,4,3],
                         [4,6,8,10,8,6,4],
                         [5,8,11,13,11,8,5],
                         [5,8,11,13,11,8,5],
                         [4,6,8,10,8,6,4],
                         [3,4,5,7,5,4,3]]
        self.move_pref= {0:3, 1:2, 2:1, 3:0, 4:1, 5:2, 6:3}

    def name(self):
        return 'agentjay_mk1'

    def make_move(self, move):
        self.b.make_move(move)


    def move_order(self,moves):
        # prefer center moves to end moves. Use when pruning
        return sorted(moves,key=lambda x:self.move_pref[x])
        #default
        # return moves


    def get_move(self):
        depth=8
        values=[]
        start= time.time()
        for move in self.b.generate_moves():
            self.b.make_move(move)
            values.append((self.alpha_beta_minimax(depth-1,-inf,
                inf,maxplayer=False), move))
            # values.append((self.minimax(depth-1,maxplayer=False),move))
            self.b.unmake_last_move()
        minimax_val,best_mv=max(values)
        for value in values:
            if value[0]==minimax_val:
                if (value[1]-3)**2<(best_mv-3)**2:
                    best_mv=value[1]
        return best_mv

    def evaluation(self,maxplayer):
        y,x=self.b.move_hist[-1]
        if maxplayer: 
            return -self.eval_table[y][x]
        else:
            return +self.eval_table[y][x]

    def minimax(self,depth, maxplayer):
        if self.b.last_move_won():
            if maxplayer:
                return -100
            else :
                return +100
        
        if depth==0 or self.b.is_full():
            return self.evaluation(maxplayer)           
            #Default evaluation is 0
            # return 0 

        values=[]
        for move in self.b.generate_moves():
            self.b.make_move(move)
            values.append(self.minimax(depth-1, not maxplayer))
            self.b.unmake_last_move()
        #If maximizing player
        if maxplayer:
            return max(values)
        #if minimizing player
        else:
            return min(values)


    def alpha_beta_minimax(self,depth, alpha, beta, maxplayer):
        if self.b.last_move_won():
            if maxplayer:
                return -100
            else :
                return +100
        if self.b.is_full():
            return 0
        if depth==0: 
            return self.evaluation(maxplayer) #evaluation of board
        
        for move in self.move_order(self.b.generate_moves()):
            self.b.make_move(move)
            v= self.alpha_beta_minimax(depth-1, alpha,beta, not maxplayer) 
            self.b.unmake_last_move()
            if maxplayer and v>=beta:
                return beta
            if maxplayer and v>alpha:
                alpha=v
            if (not maxplayer) and v<=alpha:
                return alpha
            if (not maxplayer) and v<beta:
                beta=v
        if maxplayer:
            return alpha
        else:
            return beta

