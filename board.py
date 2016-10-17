class Board:
    def __init__(self):
        self.state= [[0 for x in range(7)] for y in range(6)]
        self.move_hist= []
        self.last_player= 2
        self.head=[6 for x in range(7)] #position of highest elements
        self.total_moves=0

    def depth(self):
        return len(self.move_hist)

    def generate_moves(self):
        #checks if top row of a column(ie. head>0) is empty and returns if so
        return tuple(i for i,val in enumerate(self.head) if val>0)
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
        self.total_moves+=1
        
    def unmake_last_move(self):
        if len(self.move_hist)==0:
            return
        y,x=self.move_hist.pop()
        self.state[y][x]=0
        self.head[x]+=1
        self.last_player= -self.last_player+3

    def scan(self,x,y,dx,dy,c):
        #Algorithm by Tor Lattimore
        count=0
        while(x<7 and x>-1 and y>-1 and y<6 and self.state[y][x]==c):
            x+=dx
            y+=dy
            count+=1
        return count

    def last_move_won(self):
        if len(self.move_hist)==0:
            return False
        last_y,last_x=self.move_hist[-1]

        #horiz
        if self.scan(last_x-1,last_y,-1,0,self.last_player) + self.scan(last_x+1,last_y,1,0,self.last_player)>=3:
            return True
        #vertical
        if self.scan(last_x,last_y-1,0,-1,self.last_player) + self.scan(last_x,last_y+1,0,1,self.last_player)>=3:
            return True
        #diagonal
        if self.scan(last_x-1,last_y-1,-1,-1,self.last_player) + self.scan(last_x+1,last_y+1,1,1,self.last_player)>=3:
            return True
        if self.scan(last_x-1,last_y+1,-1,1,self.last_player) + self.scan(last_x+1,last_y-1,1,-1,self.last_player)>=3:
            return True
        return False


    def diagnostic(self,msg=""):
        print(msg)
        print(self)
        print(self.move_hist)

    def __str__(self):
        return '\n'+str(self.state).replace('], [', ']\n[')

