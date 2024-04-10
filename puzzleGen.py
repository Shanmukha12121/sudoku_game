import random
import sudokuGen, sudokuSolver
from sudokuSolver import moreThanOneSolution

N = 9

#This method returns a random full puzzle.
#Method is implemented in sudokuGen class 
def randomBoard():
    return sudokuGen.genFullBoard()

#Given a full puzzle and a list of indices,
#Returns a puzzle in which all the indices that are not in the list are zero's
def fillPartialBoard(grid, chosenIndices):
    partial = [[0 for i in range(N)] for j in range(N)]
    for (i,j) in chosenIndices:
        partial[i][j] = grid[i][j]
    return partial

#Main function of this class: given a number 1-3 which repersents the 
#difficulty of the puzzle, it returns a tuple of (puzzle,solution) where
#the difficulty of the puzzle is determined by the input to the function
def PuzzleGen(difficulty):

    allIndices = [(x,y) for x in range(9) for y in range(9)]

    if difficulty != 1:
        if difficulty == 2: neededClues = random.randint(30,35)
        if difficulty == 3: neededClues = random.randint(25,30)
        puzzle, solution = PuzzleGen(1)
        allIndices = random.sample(allIndices,81)
        i, clues = 0, 36
        while i != len(allIndices) and clues != neededClues:
            row, col = allIndices[i][0], allIndices[i][1]
            if puzzle[row][col] != 0:
                puzzle[row][col] = 0
                if sudokuSolver.moreThanOneSolution(puzzle):
                    puzzle[row][col] = solution[row][col]
                else: clues -= 1
            i += 1
        return (puzzle,solution)
    else:
        # This part creates a random puzzle with exactly 36 clues.
        while True:
            grid = randomBoard()
            chosenIndices = random.sample(allIndices, 36)
            puzzleCandidate = fillPartialBoard(grid, chosenIndices)
            if not sudokuSolver.moreThanOneSolution(puzzleCandidate):
                return (puzzleCandidate, grid)
           


def addBestClue(puzzle, solution, alreadyChosen: list[(int,int)]):
    availableGuesses = []
    for i in range(9):
        for j in range(9):
            if (i,j) not in alreadyChosen:
                availableGuesses.append((i,j))
                puzzle[i][j] = solution[i][j]
                if sudokuSolver.moreThanThreeSolutions(puzzle):
                    puzzle[i][j] = 0
                else:
                    alreadyChosen.append((i,j))
                    return
    revealed = random.sample(availableGuesses, 1)
    (x, y) = (revealed[0][0],revealed[0][1])
    alreadyChosen.append((x,y))
    puzzle[x][y] = solution[x][y]
    

def anotherWayPuzzleGen(difficulty):
    hiddenNum = 36
    if difficulty == 2: hiddenNum = 27
    if difficulty == 3: hiddenNum = 20
    allIndices = [(x,y) for x in range(9) for y in range(9)]
    
    while True:
        grid = randomBoard()
        chosenIndices = random.sample(allIndices, hiddenNum)
        puzzleCandidate = fillPartialBoard(grid, chosenIndices)
        if sudokuSolver.moreThanOneSolution(puzzleCandidate):
            if difficulty != 1:
                for i in range (7):
                    addBestClue(puzzleCandidate, grid, chosenIndices)
                    if not sudokuSolver.moreThanOneSolution(puzzleCandidate):
                        return (puzzleCandidate, grid)

        else:
            return (puzzleCandidate, grid)

        
#Prints a puzzle and solution with difficulty matching the input value
def printPuzzleAndSol(difficulty):
    (puz,sol) = PuzzleGen(difficulty)
    #(puz,sol) = anotherWayPuzzleGen()
    print ("Puzzle:")
    Print(puz)

    clues = 0
    for i in range (N):
        for j in range(N):
            if puz[i][j] != 0:
                clues += 1

    print ("Number of clues is: " + str(clues))
    print('\n' + "Solution:")
    Print(sol)

def Print(board):
    for line in board: print(line)
