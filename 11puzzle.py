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





def main():
    initialS, goalS = createStates("Sample_Input.txt")
    printOutput(initialS, goalS)

if __name__ == "__main__":
    main()

    