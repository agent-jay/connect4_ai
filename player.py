import time
import random
import board
from itertools import combinations

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
        self.move_pref_dict={}
        self.gen_move_pref_dict()
        self.move_pref_dict_ab={}
        self.timeout=3
        self.prev_depth=0
        self.depth_limit=43
        self.start_time=None

    def name(self):
        return 'agentjay_mk2'

    def gen_move_pref_dict(self):
        for size in range(1,8):
            for comb in combinations(range(7),size):
                j=0
                for i in comb:
                    j^=2**(6-i)
                self.move_pref_dict[j]= sorted(comb,key=lambda x:self.move_pref[x])

    def make_move(self, move):
        self.b.make_move(move)


    def move_order(self,moves):
        best_mv=self.move_pref_dict_ab.get(self.b.hashable())
        if best_mv:
            return[best_mv]+[mv for mv in self.move_pref_dict[moves] if mv!=best_mv]
        # prefer center moves to end moves. Use when pruning
        return self.move_pref_dict[moves]
        #default
        # return moves


    def get_move(self):
        #Iterative deepening
        self.start_time=time.time()
        self.b.total_moves=0
        best_moves=[]
        depth=1
        while(depth<self.depth_limit):
            best_move=self.get_move_at_depth(depth)
            if best_move==None:
                break
            best_moves.append(best_move)
            depth+=1
        # print("MAX DEPTH:"+str(len(best_moves)))
        self.prev_depth=depth-1
        self.move_pref_dict_ab={}
        return best_moves[-1]
        

    def get_move_at_depth(self,depth):
        values=[]
        for move in self.move_order(self.b.gen_hashmove()):
            self.b.make_move(move)
            value=(self.alpha_beta_minimax(depth-1,-inf,
                inf,maxplayer=False), move)
            # values.append((self.minimax(depth-1,maxplayer=False),move))
            self.b.unmake_last_move()
            if value[0]==None:
                return
            self.move_pref_dict_ab[self.b.hashable()]=move
            values.append(value)
        print(values)
        minimax_val,best_mv=max(values)
        for value in values:
            if value[0]==minimax_val:
                if self.move_pref[value[1]]<self.move_pref[best_mv]:
                    best_mv=value[1]
        return best_mv

    def evaluation(self,maxplayer):
        return 0
        i=len(self.b.move_hist)-1
        evalsum=0
        while(i>=0):
            y,x=self.b.move_hist[i]
            if self.b.state[y][x]==1:
                evalsum+= self.eval_table[y][x]
            else:
                evalsum-= self.eval_table[y][x]
            i-=1
        return evalsum

        y,x=self.b.move_hist[-1]
        if maxplayer: 
            return -self.eval_table[y][x]
        else:
            return +self.eval_table[y][x]

    def alpha_beta_minimax(self,depth, alpha, beta, maxplayer):
        if time.time()-self.start_time>= self.timeout:
            return None
        if self.b.last_move_won():
            if maxplayer:
                return -200
            else :
                return +200
        if depth==0: 
            return self.evaluation(maxplayer) #evaluation of board
        if self.b.is_full():
            return 0
        
        for move in self.move_order(self.b.gen_hashmove()):
            self.b.make_move(move)
            v= self.alpha_beta_minimax(depth-1, alpha,beta, not maxplayer) 
            self.b.unmake_last_move()
            if v==None:
                return None
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

