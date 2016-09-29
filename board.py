class Board:
    def __init__(self):
        self.state= [[0 for x in range(7)] for y in range(6)]
        self.move_hist= []
        self.last_player= 2
        self.head=[6 for x in range(7)] #position of highest elements

    def depth(self):
        return len(self.move_hist)

    def generate_moves(self):
        #checks if top row of a column(ie. head>0) is empty and returns if so
        return [i for i,val in enumerate(self.head) if val>0]
        # alt method
        # return [i for i,val in enumerate(self.state[0]) if val==0]
   
    def is_full(self):
        if sum(self.head)==0:
            return True
        return False

    def make_move(self, move):
        #Head-store position of topmost piece on each column. Fast vertical checks
        self.head[move]-=1
        self.move_hist.append((self.head[move],move))
        self.state[self.head[move]][move]= -self.last_player+3
        self.last_player=-self.last_player+3
        
    def unmake_last_move(self):
        if len(self.move_hist)==0:
            return
        y,x=self.move_hist.pop()
        self.state[y][x]=0
        self.head[x]+=1
        self.last_player= -self.last_player+3

    def last_move_won(self):
        if len(self.move_hist)==0:
            return False
        last_y,last_x=self.move_hist[-1]

        #horiz
        x=max(0,last_x-3)

        while(x+3<7 and x<=last_x):
            slc=self.state[last_y][x:x+4]
            if len(set(slc))==1 and self.last_player in slc:
                return True
            x+=1
        #vert
        if last_y<=2:
            slc=[row[last_x] for row in self.state[last_y:last_y+4]]
            if len(set(slc))==1 and self.last_player in slc:
                return True
                    
        #left diagonal
        x=last_x-3
        y=last_y-3
        while x<0 or y<0:
            x+=1
            y+=1
        while x+3<7 and y+3<6 and x<=last_x and y<=last_y:
            slc=[self.state[y+i][x+i] for i in range(0,4)]
            if len(set(slc))==1 and self.last_player in slc:
                return True
            x+=1
            y+=1
        
        #right diagonal. 
        x=last_x+3
        y=last_y-3
        while x>6 or y<0:
            x-=1
            y+=1
        while x-3>=0 and y+3<6 and x>=last_x and y<=last_y:
            slc=[self.state[y+i][x-i] for i in range(0,4)]
            if len(set(slc))==1 and self.last_player in slc:
                return True
            x-=1
            y+=1
    
    def diagnostic(self,msg=""):
        print(msg)
        print(self)
        print(self.move_hist)

    def __str__(self):
        return '\n'+str(self.state).replace('], [', ']\n[')

