"""
CS 4613 - AI Project 1
Authors: Tatyana Graesser (tg1625), Helen Xu (hjx201)

"""

import heapq
from copy import deepcopy

width = 4
height = 3

class Node:
    def __init__(self, state, goal, depth, solnpath, flist):
        self.state = state                              #2-d matrix of puzzle position
        self.hn = sumManhattans(self.state, goal)       #stored to check if this is goal node
        self.depth = depth                              #keeps track of depth in tree
        self.fn = self.hn + self.depth                  #keeps track of total f(n)
        self.solnpath = solnpath                        #keeps track of current solution path
        self.flist = flist + str(self.fn) + " "         #keeps track of list of fvalues of nodes generated in trees

    def __str__(self):
        return "(" + (str)(self.state) + ", f(n) = " + (str)(self.fn) + ", solution path = " + self.solnpath + ", f-list = " + self.flist + ")"

    def __repr__(self):
        return (str)(self)

    def __lt__(self, other): #allows for comparison of two nodes to use in the min heap
        return self.fn < other.fn

def sumManhattans(state1, state2): #get manhattan distance for two states 
    dists = 0
    for y in range(height):
        for x in range(width):
            if state1[y][x] != state2[y][x] and state1[y][x] != 0:
                dists += 1
    return dists

def findzero(state): #find coordinates of the blank tile
    for y in range(height):
        for x in range(width):
            if(state[y][x] == 0):
                return y, x

def expand(nodeo, goal, expanded, expandable): #create 4 children of the node and push them into the expandable list
    if(nodeo.hn == 0): # check if goal has been reached
        return True, nodeo

    zeroy, zerox = findzero(nodeo.state) #find location of zero 

    #Check moving left
    if(zerox > 0):
        lstate = deepcopy(nodeo.state)
        lstate[zeroy][zerox], lstate[zeroy][zerox-1] = lstate[zeroy][zerox-1], lstate[zeroy][zerox]
        #if not already in list with lower f(n) value
        if lstate not in expanded: #create node and push into heap
                lnode = Node(lstate, goal, nodeo.depth + 1, nodeo.solnpath + "L ", nodeo.flist)                
                heapq.heappush(expandable,lnode)
    #Same procedures for the other actions (right, up, and down)
    #check moving right
    if (zerox < width - 1):
        rstate = deepcopy(nodeo.state)
        rstate[zeroy][zerox], rstate[zeroy][zerox+1] = rstate[zeroy][zerox+1], rstate[zeroy][zerox]
        if rstate not in expanded:
                rnode = Node(rstate, goal, nodeo.depth + 1, nodeo.solnpath + "R ", nodeo.flist)
                heapq.heappush(expandable,rnode)
    #check moving up
    if (zeroy > 0):
        ustate = deepcopy(nodeo.state)
        ustate[zeroy][zerox], ustate[zeroy - 1][zerox] = ustate[zeroy - 1][zerox], ustate[zeroy][zerox]
        if ustate not in expanded:
                unode = Node(ustate, goal, nodeo.depth + 1, nodeo.solnpath + "U ", nodeo.flist)
                heapq.heappush(expandable,unode)
    #check moving down
    if (zeroy < height - 1): 
        dstate = deepcopy(nodeo.state) 
        dstate[zeroy][zerox], dstate[zeroy + 1][zerox] = dstate[zeroy + 1][zerox], dstate[zeroy][zerox]
        if dstate not in expanded:
                dnode = Node(dstate, goal, nodeo.depth + 1, nodeo.solnpath + "D ", nodeo.flist)
                heapq.heappush(expandable, dnode)

    return False, None


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
                if row == height: #switch to adding to goal state matrix
                    addingM = goalS
                    row = 0
                else:
                    row += 1 #move to a new row 
                    addingM.append([ ])
        if char != '':
            addingM[row].append(int(char)) #getting last character we may have missed
    #cleaning up any extra rows, probably a better way of making sure we just don't have to do this
    initialS = initialS[:height]
    goalS = goalS[:height]
    print("Reading states from", filepath)
    return initialS, goalS


def printOutput(initialS, goalS, goalNode, numNodes): #print final output to file
        printed = False
        while not printed:
            filepath = input("Enter output file name: ")
            try:
                with open(filepath, "w") as fp:
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
                    fp.write("\n" + str(goalNode.depth) + "\n")     #depth
                    fp.write(str(numNodes) + "\n")                  #N              
                    fp.write(goalNode.solnpath + "\n")              #Solution Path
                    fp.write(goalNode.flist)                        #list of f(n) values
            except:
                print("An error occured, please try again")
            else:
                print("Output printed to", filepath)
                printed = True
        

def solve(initialS, goalS): #actually running A*
    goalReached = False #are we at the goal
    goalNode = None #will hold the goal node if we find one
    
    expandable = [] #min-heap used to keep track of expandable nodes
    expanded = [] #list of nodes that have already been expanded, used for graph-search

    root = Node(initialS, goalS, 0, "", "") #initialize root node
    
    heapq.heappush(expandable,root) #add root to the min-heap
    
    while expandable and not goalReached: #while there are expandable nodes (heap isn't empty) and we haven't gotten a goal:
        currnode = heapq.heappop(expandable) #expand node with least cost (uses min-heap)
        goalReached, goalNode = expand(currnode, goalS, expanded, expandable) #expand the current node. Will return Boolean for if goal was found, as well as the goal node
        expanded.append(currnode.state) #add current node to list of expanded nodes
    
    printOutput(initialS, goalS, goalNode, len(expanded) + len(expandable)) #print output to file

def main(): 
    filepath = ""
    while True:
        filepath = input("Enter filepath for input file. Enter EXIT to end code: ")
        if filepath == "EXIT":
            print("Goodbye :)")
            break
        try:   
            initialS, goalS = createStates(filepath) #read in initial and goal states from starting node
        except:
            print("Incorrect filepath")
        else:
            solve(initialS, goalS) #run fun algorithm
        

if __name__ == "__main__":
    main()

