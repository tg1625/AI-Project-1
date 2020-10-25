#each node of search tree stores action cost, sum of manhattan distances, and total h(n) value, and pointers to child nodes, is_expanded value?

#keep hashmap of evaluated states? 
width = 4	
height = 3


class Node:
	def __init__(self, state, fn, depth):
		#initialize node
		self.state = state
		self.fn = fn
		self.depth = depth
		
	def expand(self):
		#create child node for left, right, down, up
		


def createStates(filepath):
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

def printOutput(initialS, goalS):
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
    initialS, goalS = createStates("Sample_Input.txt")
    printOutput(initialS, goalS)

if __name__ == "__main__":
    main()

	#sum up manhattan distances

#have another data structure to store path-cost pairs?


#read in states from file
#initialize graph of states (array of states? or dictionary map storing the h(n) and )
#create tree-type data structure thing?
#have list of unexpanded nodes (as a priority queue?)
#attempt all options: create nodes for each thing
#camculate h(n) of that state

#expand_node: expands nodes and adds new states to the graph if they aren't there?
