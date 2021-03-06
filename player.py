import time
import random
# import board
from . import board #Change this everytime
from itertools import combinations
from collections import defaultdict

inf=1000
KILLER_MOVE_LEN=2
class Player:
    def __init__(self):
        self.b=board.Board()
        self.coin= 1 #It's the coin this player uses on the board
        self.move_pref= {0:3, 1:2, 2:1, 3:0, 4:1, 5:2, 6:3}
        self.move_pref_dict={}
        self.gen_move_pref_dict()
        self.move_pref_dict_ab={}
        self.killer=defaultdict(list)
        self.history={}
        self.timeout=3
        self.prev_depth=0
        self.depth_limit=43
        self.start_time=None

    def name(self):
        return 'agentjay_mk3'

    def gen_move_pref_dict(self):
        for size in range(1,8):
            for comb in combinations(range(7),size):
                j=0
                for i in comb:
                    j+=2**(6-i)
                self.move_pref_dict[j]= sorted(comb,key=lambda x:self.move_pref[x])
        self.move_pref_dict[0]=[] #When no move is possible

    def make_move(self, move):
        self.b.make_move(move)


    def move_order(self,depth):
        move_cd=self.b.gen_hashmove()
        moves= self.move_pref_dict[move_cd]
        best_mv=self.move_pref_dict_ab.get(self.b.zobrist_key)
        final_moves=[]
        if best_mv in moves:
            final_moves.append(best_mv)
        killer_mv= self.killer.get(depth)
        if killer_mv:
            final_moves+=[mv for mv in killer_mv if mv in moves and
                    mv!=best_mv]
        if final_moves:
            return final_moves+[mv for mv in moves if mv not in final_moves]
        # if killer_mv: 
            # moves=  killer_mv+[mv for mv in moves if mv not in killer_mv]
        # if best_mv in moves: 
            # return [best_mv]+[mv for mv in moves if mv!=best_mv]
        return moves


    def get_move(self):
        #Iterative deepening
        self.start_time=time.time()
        if len(self.b.move_hist)==0:
            self.coin=0
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
        print(self.prev_depth)
        self.move_pref_dict_ab={}
        self.killer.clear()
        return best_moves[-1]
        

    def get_move_at_depth(self,depth):
        values=[]
        alpha=-inf
        # for move in self.b.generate_moves():
        for move in self.move_order(100): #arbit large depth.
            self.b.make_move(move)
            value=(self.alpha_beta_minimax(0,depth-1,alpha,
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

    def evaluation(self):
        # return 0
        return board.PLAYER_SIGN[self.coin]*sum(self.b.eval_sum)
        i=len(self.b.move_hist)-1
        evalsum=0
        while(i>=0):
            x=self.b.move_hist[i]
            if self.b.state[y][x]==self.coin:
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

    def alpha_beta_minimax(self,depth,depthleft, alpha, beta, maxplayer):
        if time.time()-self.start_time>= self.timeout:
            return None
        if self.b.last_move_won():
            if maxplayer:
                return -300
            else :
                return +300
        if depthleft==0: 
            return self.evaluation() #evaluation of board
        if self.b.is_full():
            return 0
        
        # a=self.b.generate_moves()
        # b=sorted(self.move_order(depth))
        # c=self.b.gen_hashmove() 
        # if a !=b:
            # print("ERROR")
            # print(a,b,c)
            # quit(1)

        # for move in self.b.generate_moves():
        best_mv=None
        for move in self.move_order(depth):
            self.b.make_move(move)
            v= self.alpha_beta_minimax(depth+1,depthleft-1, alpha,beta, not maxplayer) 
            self.b.unmake_last_move()
            if v==None:
                return None
            if maxplayer and v>=beta:
                # self.move_pref_dict_ab[self.b.zobrist_key]=move
                tmp=self.killer[depth]
                tmp.insert(0,move)
                if len(tmp)>=KILLER_MOVE_LEN:
                    tmp.pop()
                return beta
            if maxplayer and v>alpha:
                alpha=v
                best_mv=move
            if (not maxplayer) and v<=alpha:
                self.move_pref_dict_ab[self.b.zobrist_key]=move
                return alpha
            if (not maxplayer) and v<beta:
                beta=v
                best_mv=move
        if maxplayer:
            self.move_pref_dict_ab[self.b.zobrist_key]=best_mv
            return alpha
        else:
            self.move_pref_dict_ab[self.b.zobrist_key]=best_mv
            return beta

