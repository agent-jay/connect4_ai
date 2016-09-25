class Board:
    def __init__(self):
        self.state= [[0 for y in range(7)] for x in range(6)]
        self.move_hist= []
        self.last_player= 2

    def depth(self):
        return len(self.move_hist)

    def generate_moves(self):
        #checks if top row of a column is empty and returns if so
        return [i for i,val in enumerate(self.state[0]) if val==0]
   
    def make_move(self, move):
        #checks the move'th column from the bottom for the first empty position
        for y in range(5,-1,-1):
            if self.state[y][move]==0:
                self.move_hist.append((y,move))
                self.state[y][move]=-self.last_player+3 #switches between 2 and 1
                self.last_player=-self.last_player+3
                break

    def unmake_last_move(self):
        y,x=self.move_hist.pop()
        self.state[y][x]=0
        self.last_player= -self.last_player+3

    def last_move_won(self):
        if len(self.move_hist)==0:
            return False
        last_y,last_x=self.move_hist[-1]

        #horiz
        x=max(0,last_x-3)

        while(x+3<7 and x<=last_x):
            if len(set(self.state[last_y][x:x+4]))==1:
                # self.diagnostic("horiz")
                return True
            x+=1
        #vert
        if last_y<=2:
            slc=[row[last_x] for row in self.state[last_y:last_y+5]]
            if len(set(slc))==1:
                # self.diagnostic("vert"+str(slc))
                return True
                    
        #left diagonal
        x=last_x-3
        y=last_y-3
        while x<0 or y<0:
            x+=1
            y+=1
        while x+3<7 and y+3<6 and x<=last_x and y<=last_y:
            slc=[self.state[y+i][x+i] for i in range(0,4)]
            # print(self)
            # print([(y+i,x+i) for i in range(0,4)])
            if len(set(slc))==1:
                # self.diagonostic("left diag")
                return True
            x+=1
            y+=1
        
        #right diagonal. 
        x=last_x+3
        y=last_y-3
        while x>6 or y<0:
            x-=1
            y+=1
        # print(y,x)
        while x-3>=0 and y+3<6 and x>=last_x and y<=last_y:
            slc=[self.state[y+i][x-i] for i in range(0,4)]
            # print([(y+i,x-i) for i in range(0,4)])
            if len(set(slc))==1:
                # self.diagnostic("right diag")
                return True
            x-=1
            y+=1
    
    def diagnostic(self,msg=""):
        print(msg)
        print(self)
        print(self.move_hist)

    def test(self):
        self.state=[[0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,1],
                    [0,0,0,0,0,0,1],
                    [0,0,0,0,0,0,1],
                    [0,0,0,0,0,0,1]]
        self.move_hist.append((2,6))
        print(self.last_move_won())
            
    def __str__(self):
        return '\n'+str(self.state).replace('], [', ']\n[')

# b=Board()
# b.test()
