import heapq
from copy import deepcopy

width = 4
height = 3



class Node:
        def __init__(self, state, goal, depth, solnpath, flist):
                self.state = state                              #2-d matrix of puzzle position
        
                self.hn = sumManhattans(self.state, goal)       #stored to check if this is goal node
                self.depth = depth #keeps track of depth in tree

                self.fn = self.hn + self.depth #keeps track of total f(n)

                self.solnpath = solnpath #keeps track of current solution path
                self.flist = flist + str(self.fn) + " " #keeps track of list of fvalues of nodes generated in trees

        def __str__(self):
                return "(" + (str)(self.state) + ", f(n) = " + (str)(self.fn) + ", solution path = " + self.solnpath + ", f-list = " + self.flist + ")"

        def __repr__(self):
                return (str)(self)

        def __lt__(self, other):
                return self.fn < other.fn


def createStates(filepath): #create 2D matrices for initial state and goal state from file
    initialS = [[]] #initial state matrix
    goalS = [[]] #goal state matrix
    with open(filepath, 'r') as fp:
        char = '' #keeping track of number
        row = 0 #keeping track of matrix row
        addingM = initialS #first adding to initial state matrix 
        for c in fp.read():
            if c.isnumeric():
                char += c
            elif c == ' ':
                addingM[row].append(int(char))
                char = ''
            elif c == '\n':
                if (char != ''): #add any found numbers 
                    addingM[row].append(int(char))
                    char = ''
                if row == 3: #switch to adding to goal state matrix
                    addingM = goalS
                    row = 0
                else:
                    row += 1 #move to a new row 
                    addingM.append([ ])
        if char != '':
            addingM[row].append(int(char)) #getting last character we may have missed
    #cleaning up any extra rows, probably a better way of making sure we just don't have to do this
    initialS = initialS[:3]
    goalS = goalS[:3]
    # print(initialS)
    # print(goalS)
    return initialS, goalS

def expand(nodeo, goal, expanded, expandable): #create 4 children of the node and push them into the expandable list
        if(nodeo.hn == 0): # check if goal has been reached
                return expandable, True, nodeo
        
        
        zeroy, zerox = findzero(nodeo.state) #find location of zero

        rstate = deepcopy(nodeo.state)
        lstate = deepcopy(nodeo.state)
        ustate = deepcopy(nodeo.state)
        dstate = deepcopy(nodeo.state) 

        print(zeroy, zerox)

        if(zerox > 0):
                print("left") #make left state
                lstate[zeroy][zerox], lstate[zeroy][zerox-1] = lstate[zeroy][zerox-1], lstate[zeroy][zerox]


                #if not already in list with lower f(n) value
                if lstate not in expanded:
                        print(lstate)
                        lnode = Node(lstate, goal, nodeo.depth + 1, nodeo.solnpath + "L ", nodeo.flist)                #create node and push into stack
                        heapq.heappush(expandable,lnode)

        #do the same for the other three
        if (zerox < width - 1):
                print("right") #make right
                rstate[zeroy][zerox], rstate[zeroy][zerox+1] = rstate[zeroy][zerox+1], rstate[zeroy][zerox]
                if rstate not in expanded:
                        print(rstate)
                        rnode = Node(rstate, goal, nodeo.depth + 1, nodeo.solnpath + "R ", nodeo.flist)
                        heapq.heappush(expandable,rnode)
        if (zeroy > 0):
                print("up") #make up
                ustate[zeroy][zerox], ustate[zeroy - 1][zerox] = ustate[zeroy - 1][zerox], ustate[zeroy][zerox]
                if ustate not in expanded:
                        print(ustate)
                        unode = Node(ustate, goal, nodeo.depth + 1, nodeo.solnpath + "U ", nodeo.flist)
                        heapq.heappush(expandable,unode)
        if (zeroy < height - 1): #down
                print("down")
                dstate[zeroy][zerox], dstate[zeroy + 1][zerox] = dstate[zeroy + 1][zerox], dstate[zeroy][zerox]
                if dstate not in expanded:
                        print(dstate)
                        dnode = Node(dstate, goal, nodeo.depth + 1, nodeo.solnpath + "D ", nodeo.flist)
                        heapq.heappush(expandable, dnode)

        return expandable, False, None


def findzero(state): #find location of zero
        for y in range(height):
                for x in range(width):
                        if(state[y][x] == 0):
                                return y, x

def printOutput(initialS, goalS): #print final output
    with open("Test_Output.txt", "w") as fp:
        #printing out initial state
        for row in initialS:
            for char in row:
                fp.write(str(char) + " ")
            fp.write("\n")
        fp.write("\n")
        #printing out goal state
        for row in goalS:
            for char in row:
                fp.write(str(char) +  " ")
            fp.write("\n")
        fp.write("\n")

def sumManhattans(state1, state2):
    dists = 0
    for y in range(height):
        for x in range(width):
            if state1[y][x] != state2[y][x] and state1[y][x] != 0:
                dists += 1
    return dists

def main():
        goalReached = False
        goalNode = None

        
        initialS, goalS = createStates("Sample_Input.txt") #read in initial and goal states from starting node
    
        expandable = []
        expanded = [] #initialize graphs of expandable nodes and already-expanded nodes

        firstnode = Node(initialS, goalS, 0, "", "") #initialize node
        
        heapq.heappush(expandable,firstnode)#uses a min heap to get nodes with min f(n) value


        while expandable and not goalReached: #while there are expandable nodes list isn't empty:
                currnode = heapq.heappop(expandable) #expand node with least cost (uses min-heap)
                print("expanding " + str(currnode.state))
                expandable, goalReached, goalNode = expand(currnode, goalS, expanded, expandable) #push each child generated into expandable nodes list, along with its h(n) value and its current solution path and its cumulative f(n)s
                expanded.append(currnode.state)

                print(expandable)
        #nodes are only created when we choose that state to be expanded

        print(len(expanded))
        print(expanded)
        print("goal node: " + str(goalNode))
        printOutput(initialS, goalS)

if __name__ == "__main__":
        main()

