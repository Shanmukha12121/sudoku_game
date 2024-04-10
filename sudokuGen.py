import random

N = 3

def pattern(r,c):
    return (N*(r%N)+r//N+c)%(N*N)

# randomize rows, columns and numbers (of valid base pattern)
def shuffle(s):
    return random.sample(s,len(s)) 

# Creating a random order of rows and cols shuffle
rangeBase = range(N)

def genRowsAndCols():
    rows = []
    for i in shuffle(rangeBase):
        for j in shuffle(rangeBase):
            rows.append(N*i + j)
    cols = []
    for i in shuffle(rangeBase):
        for j in shuffle(rangeBase):
            cols.append(N*i + j)

    nums  = shuffle(range(1,N*N+1))
    return (rows,cols,nums)



def checkLegal(grid):
    for i in range(9):
        for j in range(9):
            if not legal(grid,i,j): return False
    return True

def legal(grid,row,col):
    for i in range (9):
        if ((i != col and grid[row][i] == grid[row][col]) or (i != row and grid[i][col] == grid[row][col])):
            return False
    
    r = 3 * (row // 3)
    c = 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if ((r+i,c+j) != (row,col) and grid[r+i][c+j] == grid[row][col]):
                return False
    return True

def genFullBoard():    
    board = []
    rows,cols,nums = genRowsAndCols()
    for row in rows:
        currRow = []
        for col in cols:
            currRow.append(nums[pattern(row,col)])
        board.append(currRow)
    return board


#for line in genFullBoard(): print(line)
