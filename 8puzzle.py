#holds the state of traversal and generates next possible moves
class State:
    #constructor
    def __init__(self,data,depth,fval):
        self.data = data
        self.depth = depth
        self.fval = fval

        #generate possible moves from current state
    def possible_moves(self):
        #search grid to find 0 e.g. movable
        x,y = self.search(self.data,'0')
        #all possible moves for the 0
        values = [[x,y-1],[x,y+1],[x-1,y],[x+1,y]]
        moves = []
        for i in values:
            #making sure move is valid and possible
            move = self.move(self.data,x,y,i[0],i[1])
            #if possible
            if move is not None:
                #new state after moved added to tree
                move_state = State(move,self.depth+1,0)
                #add the state to the array
                moves.append(move_state)

        #return array of new states that are possible moves
        return moves

    #making sure move is valid and if it is out of range and doesnt work it will return None
    def move(self,puz,x1,y1,x2,y2):
        #if in range
        if x2 >= 0 and x2 < len(self.data) and y2 >= 0 and y2 < len(self.data):
            #hard copy of current puzzle
            temp_puz = []
            temp_puz = self.hardCopy(puz)
            #change will hold value that will be swaped with 0
            change = temp_puz[x2][y2]
            #swapping values
            temp_puz[x2][y2] = temp_puz[x1][y1]
            temp_puz[x1][y1] = change
            #return new puzzle after the move
            return temp_puz
        else:
            return None

    #auxillary function used to hard copy the array
    def hardCopy(self,root):
        copy = []
        for i in root:
            t = []
            for j in i:
                t.append(j)
            copy.append(t)
        return copy

    #search for a character in the array and return coords, only used for 0
    def search(self,puz,zero):
        for x in range(0,len(self.data)):
            for y in range(0,len(self.data)):
                if puz[x][y] == zero:
                    return x,y


#is a class used for the inputs and operation of the a* algorithm
class Puzzle:
    #constructor
    def __init__(self):
        self.n = 3
        self.open = []
        self.closed = []

    #read in user input as a grid and return the array
    def read(self):
        puz = []
        for i in range(0,self.n):
            temp = input().split(" ")
            puz.append(temp)
        return puz

    #f value for Number of tiles out of position
    def f(self,start,goal):
        return self.h(start.data,goal)+start.depth

    #h value for Number of tiles out of position
    def h(self,start,goal):
        hval = 0
        for i in range(0,self.n):
            for j in range(0,self.n):
                if start[i][j] != goal[i][j] and start[i][j] != '0':
                    hval += 1
        return hval

    #f value for Sum of the manhattan distances
    def fMan(self,start,goal):
        return self.hMan(start.data,goal)+start.depth

    #h value for Sum of the manhattan distance
    def hMan(self,start,goal):
        hval = 0
        for i in range(0,self.n):
            for j in range(0,self.n):
                if start[i][j] != goal[i][j] and start[i][j] != '0':
                    indxG = [(ix,iy) for ix, row in enumerate(goal) for iy, y in enumerate(row) if y == start[i][j]]
                    hval+=(abs(i-indxG[0][0])+abs(j-indxG[0][1]))
        return hval

    def main(self,test=False):
        #input for choice of heuristic
        print("\nEnter heuristic difference or manhattan, [D/M]\n")
        heu = str(input(": ")).lower()

        #demo option
        if(test == True):
            start = initial_state
            goal = goal_state

        else:
            print("Enter the initial state: \n")
            start = self.read()

            print("Enter the goal state: \n")
            goal = self.read()

        start = State(start,0,0)
        #initial f values dependant on choice of heuristic
        if(heu == "d"):
            start.fval = self.f(start,goal)
        else:
            start.fval = self.fMan(start,goal)
        self.open.append(start)
        #A*
        while True:
            current = self.open[0]
            #finish when h is 0
            if(heu == "d"):
                if(self.h(current.data,goal) == 0):
                    print("\n It took ",current.depth," moves")
                    break
            else:
                if(self.hMan(current.data,goal) == 0):
                    print("\n It took ",current.depth," moves")
                    break
            #generate and go through possible moves
            for i in current.possible_moves():
                if(heu == "d"):
                    i.fval = self.f(i,goal)
                else:
                    i.fval = self.fMan(i,goal)
                #add all to open queue
                self.open.append(i)
            #close current as searching next moves and remove from open
            self.closed.append(current)
            del self.open[0]
            #sort into order of lowest f value to search first
            self.open.sort(key = lambda x:x.fval,reverse=False)


if __name__=="__main__":

    #DEMO
    initial_state = [['0' ,'2', '4'] ,['5', '7', '6'], ['8', '3', '1']]
    goal_state = [['0' ,'4', '6'] ,['2', '7', '1'], ['5', '8', '3']]
    demo = Puzzle()
    demo.main(True)
    #display
    print("\n with an Initial state of: \n", initial_state)
    print("\n and the Goal state being: \n", goal_state)
    #user ready input
    puzzle = Puzzle()
    puzzle.main()
