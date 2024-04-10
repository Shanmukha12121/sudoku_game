import copy, random

N = 9

# Given a grid, and an 'index' in the grid
# ret == True iff num can be put in the index, while keeping grid a legal sudoku puzzle
def possibleLocation(grid,row,col,num):
    for i in range (9):
        if ((i != col and grid[row][i] == num) or (i != row and grid[i][col] == num)):
            return False
    
    r = 3 * (row // 3)
    c = 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if ((r+i,c+j) != (row,col) and grid[r+i][c+j] == num):
                return False
    return True


# This function (including the global parm COUNT) is used in order to
# determine the number of possible solutions to a given puzzle
# It is used by the "uniqueSolution" function which is written below
COUNT = 0
def solutionNumber(grid):
    global COUNT
    for i in range(N):
        for j in range(N):
            if (grid[i][j] == 0):
                for num in range(1,10):
                    if possibleLocation(grid,i,j,num):
                        grid[i][j] = num
                        solutionNumber(grid)
                        grid[i][j] = 0
                return
    COUNT += 1

def moreThanOneSolution(grid):
    solNum = [0]
    def rec(grid, solNum):
        for i in range(N):
            for j in range(N):
                if (grid[i][j] == 0):
                    for num in range(1,10):
                        if possibleLocation(grid,i,j,num):
                            grid[i][j] = num
                            rec(grid, solNum)
                            grid[i][j] = 0
                    return
        solNum[0] += 1
        if solNum[0] > 1:
            raise Exception()
    try:
        puzzle = copy.deepcopy(grid)
        rec(puzzle, solNum)
        return False
    except:
        return True

def moreThanThreeSolutions(grid):
    solNum = [0]
    def rec(grid, solNum):
        for i in range(N):
            for j in range(N):
                if (grid[i][j] == 0):
                    for num in range(1,10):
                        if possibleLocation(grid,i,j,num):
                            grid[i][j] = num
                            rec(grid, solNum)
                            grid[i][j] = 0
                    return
        solNum[0] += 1
        if solNum[0] > 3:
            raise Exception()
    try:
        puzzle = copy.deepcopy(grid)
        rec(puzzle, solNum)
        return False
    except:
        return True


# returns a number which represents the number of solutions to the puzzle
# ret == 0 iff no solutions
# ret == 1 iff one solution
# ret == x , x > 1 iff there are x solutions to the puzzle
def uniqueSolution(puzzle):
    global COUNT
    solutionNumber(puzzle)
    temp = COUNT
    COUNT = 0
    return temp


# Prints all possible solutions to a puzzle
def allSolutions(grid):
    for i in range(N):
        for j in range(N):
            if (grid[i][j] == 0):
                for num in range(1,10):
                    if possibleLocation(grid,i,j,num):
                        grid[i][j] = num
                        allSolutions(grid)
                        grid[i][j] = 0
                return
    print("Solution: ")
    for line in grid: print(line)


# Returns the solution to a puzzle (or 1 of the solutions, if there are more then 1 solutions)
def solve(puzzle):
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] == 0:
                for num in range(1,10):
                    if possibleLocation(puzzle, i, j, num):
                        puzzle[i][j] = num
                        if not solve(puzzle):
                            puzzle[i][j] = 0
                        else:
                            return puzzle
                return None
    print("Solved!")
    return puzzle
