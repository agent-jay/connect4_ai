def bound_x(val):
    if val<0:
        return 0
    if val>6:
        return 6
    return val

def bound_y(val):
    if val<0:
        return 0
    if val>5:
        return 5
    return val

class Board:
    def __init__(self):
        self.state= [[0]*7]*6 #state[y][x]
        self.move_hist= []
        self.last_player= 2

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
        self.state[y,x]=0
        self.last_player= -self.last_player+3

    def last_move_won(self):
        if len(self.move_hist)==0:
            return False
        last_y,last_x=self.move_hist[-1]

        #horiz
        x=last_x-3
        if x<0:x=0

        while(x+3<7 and x<=last_x):
            if len(set(self.state[last_y][x:x+4]))==1:
                return True
            x+=1
        #vert
        if last_y<4:
            slc=[row[last_x] for row in self.state[last_y:last_y+3]]
            if len(set(slc))==1:
                return True
                    
        #left diagonal
        x=last_x-3
        y=last_y-3
        while x<0 or y<0:
            x+=1
            y+=1
        while x+3<7 and y+3<6:
            slc=[self.state[y+i][x+i] for i in range(0,4)]
            if len(set(slc))==1:
                return True
            x+=1
            y+=1
        
        #right diagonal
        x=last_x+3
        y=last_y+3
        while x>6 or y>5:
            x+=1
            y+=1
        while x-3>0 and y-3>0:
            slc=[self.state[y-i][x-i] for i in range(0,4)]
            if len(set(slc))==1:
                return True
            x+=1
            y+=1


            
    def __str__(self):
        return str(self.state).replace('], [', ']\n[')

