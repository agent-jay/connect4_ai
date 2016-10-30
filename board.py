from random import randint,seed
import numpy as np

INT_64_MAX=int('1'*64,2)
TOP= int(('1000000'*7).zfill(64), 2)
TOP_INT=[6,13,20,27,34,41,48]
PLAYER_SIGN=[1,-1]

class Board:
    def __init__(self):
        self.bitboards= [0,0]
        self.move_hist= []
        self.last_player= 2
        self.head=[x for x in range(0,43,7)] #position of highest elements
        self.total_moves=0
        self.counter=0
        self.rand_seed=53
        self.zobrist=[[],[]]
        self.zobrist_key=0
        self.zobrist_init()
        self.eval_sum=[0,0]
        self.eval_table=[3,4,5,5,4,3,0,4,6,8,8,6,4,0,5,8,11,11,8,5,0,7,10,
                13,13,10,7,0,5,8,11,11,8,5,0,4,6,8,8,6,4,0,3,4,5,5,4,3,0,
                0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    def zobrist_init(self):
        seed(self.rand_seed)
        self.zobrist=[[randint(0,INT_64_MAX) for i in range(64)],
                [randint(0,INT_64_MAX) for i in range(64)]]
    
    def make_move(self, col):
        #Head-store position of topmost piece on each column. Fast vertical checks
        player_index= self.counter & 1
        move= 1<<self.head[col]
        self.bitboards[player_index]^= move
        
        self.zobrist_key^=self.zobrist[player_index][self.head[col]]
        # self.eval_sum[player_index]+= PLAYER_SIGN[player_index]*self.eval_table[self.head[col]]

        self.head[col]+=1
        self.move_hist.append(col)
        self.counter+=1
        self.last_player=-self.last_player+3
        self.total_moves+=1
        
    def unmake_last_move(self):
        if len(self.move_hist)==0:
            return
        col= self.move_hist.pop()
        self.head[col]-=1
        move= 1<<self.head[col]
        self.counter-=1
        player_index= self.counter & 1
        self.bitboards[player_index]^=move
        
        self.zobrist_key^=self.zobrist[player_index][self.head[col]]
        # self.eval_sum[player_index]-= PLAYER_SIGN[player_index]*self.eval_table[self.head[col]]

        self.last_player= -self.last_player+3
    
    def generate_moves(self):
        #checks if top row of a column(ie. head>0) is empty and returns if so
        return [col for col in range(7) if not(TOP & (1<<self.head[col]))]

    def gen_hashmove(self):
        key=0
        for col in range(7):
            if not (TOP & (1<<self.head[col])):
                key+= 2**(6-col)
        return key
                
    def is_full(self):
        if self.head==TOP_INT:
            return True
        return False

    def scan(self,x,y,dx,dy,c):
        #Algorithm by Tor Lattimore
        count=0
        while(x<7 and x>-1 and y>-1 and y<6 and self.state[y][x]==c):
            x+=dx
            y+=dy
            count+=1
        return count

    def last_move_won(self):
        if self.move_hist:
            bitboard=self.bitboards[self.last_player-1]
            directions=[1,7,6,8]
            for direction in directions:
                bb= bitboard & (bitboard >> direction)
                if (bb & (bb >> (2 * direction))):
                    return True
        return False
        
    def diagnostic(self,msg=""):
        print(msg)
        print(self)
        print(self.move_hist)

    def hashable(self):
        return self.zobrist_key

    def __str__(self):
        p1,p2= map(bin,self.bitboards)
        p2.replace('1','2')
        p1=p1.replace('0b','').zfill(64)[::-1]
        p2=p2.replace('0b','').replace('1','2').zfill(64)[::-1]
        a=[[0 for i in range(7)] for j in range(6)]
        pt=0
        y,x=5,0
        while(pt<48):
            if p1[pt]!='0':
                a[y][x]= p1[pt]
            elif p2[pt]!='0':
                a[y][x]=p2[pt]
            else:
                a[y][x]='0'
            pt+=1
            y-=1
            if pt in (6,13,20,27,34,41):
                pt+=1
                x+=1
                y=5
        return '\n'+str(a).replace('], [', ']\n[')


            
            
