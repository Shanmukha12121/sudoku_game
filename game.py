import copy, pygame, puzzleGen, sudokuSolver, random
import os
import copy
import pygame
import puzzleGen
import sudokuSolver
import random
import sys

def load_image(file_path):
    try:
        image = pygame.image.load(file_path)
    except pygame.error as e:
        print("Error loading image:", e)
        return None
    return image
pygame.init()

size = width, height = 550,700
screen = pygame.display.set_mode(size)

# Creating Title and Icon
icon = pygame.image.load("icon.png")
pygame.display.set_caption("Sudoku Game"+ 74*" " + "by Shanmukh")
pygame.display.set_icon(icon)

# Global parmaters
hoverColor = (79,79,240)
hoverX = 465
hoverY = 120
startGridX = 25
startGridY = 80
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (51,153,255)
RED = (225,125,125)
NAVY = (4,115,202)

pyDigits = [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
            pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]
hoverPos = {"Play": (43,130), "Quit": (43, 276), "Settings": (43,422), "Easy": (50,10), "Medium": (180,10), "Hard": (375,10)}



# Loading all nessecairy images in advance, resizing if needed
grid = pygame.transform.scale(pygame.image.load("Resources/fullgrid.png"), (500,500))
clouds = pygame.transform.scale(pygame.image.load("Resources/clouds.png"), (550,700))
mainMenuButtons = pygame.transform.scale(pygame.image.load("Resources/mainMenuButtons.png"),(470,437.5))
helpMenu = pygame.transform.scale(pygame.image.load("Resources/helpMenu.png"), (550,330))
rightArrow = pygame.transform.scale(pygame.image.load("Resources/rightArrow.png"), (200,200))

buttonsFont = pygame.font.Font('Resources/LEMONMILK-Bold.otf', 40)
digitsFont = pygame.font.Font('Resources/digFont.ttf', 38)
helpFont = pygame.font.Font('Resources/LEMONMILK-Bold.otf', 19)
settingsFont = pygame.font.Font('Resources/LEMONMILK-Bold.otf', 32)
digitsForSettingsFont = pygame.font.Font('Resources/LEMONMILK-Bold.otf', 70)

easy = buttonsFont.render('Easy',True, BLACK, (0,119,202))
medium = buttonsFont.render('Medium', True, BLACK, (0,123,205))
hard = buttonsFont.render('Hard', True, BLACK, (0,128,210))
clue = buttonsFont.render('Clue', True, NAVY, (135,205,239))
solve = buttonsFont.render('Solve', True, NAVY, (165,215,245))
exit = buttonsFont.render('Exit', True, NAVY, (155,215,237))
help = helpFont.render("Press  'S' for solution", True, (4,145,205), (179,220,234))
settingsInst = settingsFont.render("Set the freeze time for the", True, BLACK, (0,123,205))
settingsInst2 = settingsFont.render("solve function (in ms):", True, BLACK, (0,123,205))
settingsInst3 = helpFont.render("Default solving time is 12ms", True, (4,145,205), (179,220,234))
settingsInst4 = helpFont.render("1000 ms = 1 sec", True, (4,145,205), (179,220,234))
settingsWhatButton = helpFont.render("Press 'enter' to select digit, 'space' when you", True, BLACK, (0,123,205))
settingsWhatButton2 = helpFont.render("are done, 'del' to delete last digit", True, BLACK, (0,123,205))
settingsCurrentMs = helpFont.render("Current freeze time:", True, BLACK, (0,123,205))


digitsForSettings = []
for x in ["1","2","3","4","5","6","7","8","9"]:
    digitsForSettings.append(digitsForSettingsFont.render(x, False, BLACK))                                                                

easyRect = pygame.rect.Rect(55,10,80,80)
mediumRect = pygame.rect.Rect(185,10,80,80)
hardRect = pygame.rect.Rect(380,10,80,80)
clueRect = pygame.rect.Rect(55,585,80,80)
solveRect = pygame.rect.Rect(203,585,80,80)
exitRect = pygame.rect.Rect(385,585,80,80)
helpRect = pygame.rect.Rect(55,650,120,120)
settingsInstRect = pygame.rect.Rect(0,0,100,100)
settingsInst2Rect = pygame.rect.Rect(0,40,100,100)
settingsInst3Rect = pygame.rect.Rect(100,630,100,100)
settingsInst4Rect = pygame.rect.Rect(170,655,100,100)
settingsWhatButtonsRect = pygame.rect.Rect(0,80,100,100)
settingsWhatButtonsRect2 = pygame.rect.Rect(0,105,100,100)
settingsCurrentMsRect = pygame.rect.Rect(0,130,100,100)
currentFreezeRect = pygame.rect.Rect(243,130,100,100)

digitsForSettingsRect = [pygame.rect.Rect(161+i*80,200+j*80,70,70) for j in range(3) for i in range(3)]
digitsForSettingsHover = [pygame.rect.Rect(digitsForSettingsRect[i].left - 12, digitsForSettingsRect[i].top + 15, 70, 70) for i in range(9)]

digits = [digitsFont.render(str(x), True, BLACK, WHITE) for x in range(10)]
trueDigits = [digitsFont.render(str(x), True, BLUE, WHITE) for x in range(10)]
falseDigits = [digitsFont.render(str(x), True, RED, WHITE) for x in range(10)]




sudokuNumberLocations = dict()
sudokuHoverLocations = dict()
for row in range(9):
    for col in range(9):
        sudokuNumberLocations[(row,col)] = pygame.rect.Rect(50 + col*55, 88 + row*55, 50, 50)
        sudokuHoverLocations[(row,col)] = pygame.rect.Rect(25 + col*55, 80 + row*55, 60, 60)

sudokuHoverLocations[(9,0)] = pygame.rect.Rect(50,585,120,57)
sudokuHoverLocations[(9,1)] = pygame.rect.Rect(197, 585, 158, 57)
sudokuHoverLocations[(9,2)] = pygame.rect.Rect(380,585,108,57)


def mainMenuScreen():
    screen.blit(clouds,(0,0))
    screen.blit(mainMenuButtons,(40,125))

def playGrid():
    screen.blit(clouds, (0,0))
    screen.blit(grid, (startGridX, startGridY))
    screen.blit(easy, easyRect)
    screen.blit(medium, mediumRect)
    screen.blit(hard, hardRect)
    screen.blit(clue, clueRect)
    screen.blit(solve, solveRect)
    screen.blit(exit,exitRect)
    screen.blit(help,helpRect)

def settingsScreen(currentHover = 10, freeze = 12):
    screen.blit(clouds, (0,0))
    screen.blit(settingsInst, settingsInstRect)
    screen.blit(settingsInst2, settingsInst2Rect)
    screen.blit(settingsWhatButton,settingsWhatButtonsRect)
    screen.blit(settingsWhatButton2,settingsWhatButtonsRect2)
    screen.blit(settingsCurrentMs, settingsCurrentMsRect)
    screen.blit(helpFont.render(str(freeze) + "ms",True, RED, (0,123,205)),currentFreezeRect)
    screen.blit(settingsInst3, settingsInst3Rect)
    screen.blit(settingsInst4, settingsInst4Rect)
    for i in range(9):
        screen.blit(digitsForSettings[i],digitsForSettingsRect[i])
    screen.blit(rightArrow,(160,430))
    if currentHover == 10:
        pygame.draw.rect(screen, hoverColor, pygame.Rect(185, 453 , 160, 160), 4, 200)
    else: pygame.draw.rect(screen, hoverColor, digitsForSettingsHover[currentHover - 1], 4, 10)
    

def changeHoverSettings(currentHover, event):
    if currentHover == 10:
        if event.key == pygame.K_UP:
            currentHover = 8
    elif currentHover in [7,8,9] and event.key == pygame.K_DOWN:
        currentHover = 10
    elif event.key == pygame.K_RIGHT:
        if currentHover % 3 == 0:
            currentHover -= 3
        currentHover += 1
    elif event.key == pygame.K_LEFT:
        if (currentHover - 1) % 3 == 0:
            currentHover += 3
        currentHover -= 1
    elif event.key == pygame.K_UP:
        currentHover = (currentHover - 3) % 9
    elif event.key == pygame.K_DOWN:
        currentHover = (currentHover + 3) % 9
    return currentHover

def drawTempFreeze(freeze):
    s = str(freeze)
    freeze = digitsFont.render(s,True, BLACK, (30,125,230))
    freezeRect = pygame.rect.Rect(255-(7*(len(s)-1)),160,100,100)
    screen.blit(freeze,freezeRect)

def drawHoverMenu(hoverPosition):
    pygame.draw.rect(screen, hoverColor, pygame.Rect(hoverPosition[0], hoverPosition[1] ,hoverX, hoverY), 5, 300)

def drawHoverDifficulties(hoverPosition):
    if hoverPosition == hoverPos["Easy"]: w,h = 125,60

    elif hoverPosition == hoverPos["Medium"]: w,h = 190,60

    elif hoverPosition == hoverPos["Hard"]: w,h = 138,60

    pygame.draw.rect(screen, hoverColor, pygame.Rect(hoverPosition[0], hoverPosition[1] ,w, h), 3, 10)

def handleEnterOnMainMenu(currHover):
                play,running,settings = False,True,False
                if currHover == hoverPos["Play"]: play = True
                elif currHover == hoverPos["Quit"]: running = False
                else: settings = True
                return play,running,settings

def handleUpDownOnMainMenu(currHover, event):
                if event.key == pygame.K_UP:
                    if currHover == hoverPos["Play"]:
                        currHover = hoverPos["Settings"]
                    elif currHover == hoverPos["Quit"]:
                        currHover = hoverPos["Play"]
                    else: currHover = hoverPos["Quit"]
                elif event.key == pygame.K_DOWN:
                    if currHover == hoverPos["Play"]:
                        currHover = hoverPos["Quit"]
                    elif currHover == hoverPos["Quit"]:
                        currHover = hoverPos["Settings"]
                    else: currHover = hoverPos["Play"]
                return currHover

def handlePressWhileOnDifficulties(currHover, event):
    if event.key == pygame.K_RIGHT:
        if currHover == hoverPos["Easy"]:
            currHover = hoverPos["Medium"]
        elif currHover == hoverPos["Medium"]:
            currHover = hoverPos["Hard"]
        else: currHover = hoverPos["Easy"]
    elif event.key == pygame.K_LEFT:
        if currHover == hoverPos["Easy"]:
            currHover = hoverPos["Hard"]
        elif currHover == hoverPos["Medium"]:
            currHover = hoverPos["Easy"]
        else: currHover = hoverPos["Medium"]
    return currHover

def drawHoverDigits(row,col): 
    pygame.draw.rect(screen, hoverColor, sudokuHoverLocations[(row,col)], 5)

def changeSudokuHover(current, key):
    if current[0] == 9:
        if key == pygame.K_LEFT:
            return (current[0], (current[1] - 1) % 3)
        elif key == pygame.K_RIGHT:
            return (current[0], (current[1] + 1) % 3)
        return (current[0],current[1])
    else:
        if key == pygame.K_UP:
            return ((current[0] - 1) % 9, current[1])
        elif key == pygame.K_DOWN:
            return ((current[0] + 1) % 9, current[1])
        elif key == pygame.K_LEFT:
            return (current[0] , (current[1] - 1) % 9)
        elif key == pygame.K_RIGHT:
            return (current[0] ,(current[1] + 1) % 9)


def drawDigit(num , index, currentSudoku, solution):
    digit = digits[num]
    rect = sudokuNumberLocations[(index)]
    if num == 0: return
    correct = (num == solution[index[0]][index[1]])
    if correct:
        digit = trueDigits[num]
        screen.blit(digit,rect)
    else:
        digit = falseDigits[num]
        screen.blit(digit,rect)
    currentSudoku[index[0]][index[1]] = num
    
def deleteDigit(puzzle, currentSudoku, solution, index):
    if (puzzle[index[0]][index[1]] == 0):
        currentSudoku[index[0]][index[1]] = 0
        drawSudoku(puzzle, currentSudoku, solution)


def drawSudoku(puzzle, currentSudoku, solution, isSolving=False):
    playGrid()
    for row in range(9):
        for col in range(9):
            num = currentSudoku[row][col]
            rect = sudokuNumberLocations[(row,col)]
            if num != 0:
                if num == puzzle[row][col]:
                    digit = digits[num]
                elif num == solution[row][col] or isSolving:
                    digit = trueDigits[num]
                else:
                    digit = falseDigits[num]

                screen.blit(digit, rect)

def drawHelp():
    screen.blit(helpMenu, (0,193,300,400))

def drawClue(currentSudoku, solution):
    for row in random.sample(range(9),9):
        for col in random.sample(range(9),9):
            if currentSudoku[row][col] == 0:
                drawDigit (solution[row][col], (row,col), currentSudoku, solution)
                return

def drawSolution(puzzle, currentSudoku, solution, freezeTime = 12):
    for i in range(9):
        for j in range(9):
            if (currentSudoku[i][j] == 0):
                for num in range(1,10):
                    if sudokuSolver.possibleLocation(currentSudoku,i,j,num):
                        currentSudoku[i][j] = num
                        drawSudoku(puzzle, currentSudoku, solution, True)
                        pygame.time.wait(freezeTime)
                        pygame.display.update()
                        if not drawSolution(puzzle, currentSudoku, solution, freezeTime):
                            currentSudoku[i][j] = 0
                            drawSudoku(puzzle, currentSudoku, solution, True)
                            pygame.time.wait(freezeTime)
                            pygame.display.update()
                        else:
                            return currentSudoku
                return None
    return currentSudoku

def showSolution(currentSudoku, solution):
    for i in range(9):
        for j in range(9):
            if currentSudoku[i][j] == 0:
                drawDigit(solution[i][j],(i,j),currentSudoku,solution)
    pygame.display.update()

running = True
mainMenu = True
selectDiff = True
sudoku = False
buttons = False
play, settings = False, False
freeze = 12
while running:
    currHover = hoverPos["Play"]
    while mainMenu:
        mainMenuScreen()
        drawHoverMenu(currHover)
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                running = False
                mainMenu = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    mainMenu = False
                    play, running, settings = handleEnterOnMainMenu(currHover)
                    if settings: currentHoverSet, tempFreeze = 10, 0
                else:
                    currHover = handleUpDownOnMainMenu(currHover, event)
        pygame.display.update()
    
    if play:
        currHover = hoverPos["Easy"]
        while play:
            playGrid()
            drawHoverDifficulties(currHover)    
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    play = False
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        play = False
                        sudoku = True
                    else:
                        currHover = handlePressWhileOnDifficulties(currHover, event)

            pygame.display.update()   
            

    if sudoku:
        if currHover == hoverPos["Easy"]: difficulty = 1
        elif currHover == hoverPos["Medium"]: difficulty = 2
        else: difficulty = 3
        puzzle, solution = puzzleGen.PuzzleGen(difficulty)
        currentSudoku = copy.deepcopy(puzzle)
        drawSudoku(puzzle, currentSudoku, solution)
        pygame.display.update()
        currentHover = (0,0)
        tempHover = (9,1)
        while sudoku:
            drawHoverDigits(currentHover[0],currentHover[1])
            keys = pygame.key.get_pressed()
            if keys[pygame.K_h]:
                drawHelp()
            if keys[pygame.K_s]:
                showSolution(currentSudoku, solution)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sudoku = False
                    running = False
                elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    drawSudoku(puzzle, currentSudoku, solution)
                    if event.type == pygame.KEYDOWN:
                        if event.key in [pygame.K_DOWN, pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT]:
                            currentHover = changeSudokuHover(currentHover,event.key)
                        elif event.key in pyDigits and currentHover[0] != 9 and puzzle[currentHover[0]][currentHover[1]] == 0:
                            # Only if user pressed a digit, and hovered over a non given index
                            drawDigit(int(pygame.key.name(event.key)), currentHover, currentSudoku, solution)
                        elif event.key == pygame.K_DELETE and currentHover[0] != 9:
                            deleteDigit(puzzle, currentSudoku, solution, currentHover)
                        elif event.key == pygame.K_SPACE:
                            temp = currentHover
                            currentHover = tempHover
                            tempHover = temp
                        elif event.key == pygame.K_RETURN:
                            if currentHover == (9,0):
                                drawClue(currentSudoku, solution)
                            elif currentHover == (9,1):
                                drawSolution(puzzle, currentSudoku, solution, freeze)
                            elif currentHover == (9,2):
                                sudoku = False
                                mainMenu = True
                                selectDiff = True   


                        

                
            pygame.display.update()   

    if settings:
        settingsScreen(currentHoverSet, freeze)
        drawTempFreeze(tempFreeze)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if currentHoverSet == 10:
                        settings = False
                        mainMenu = True
                    else: tempFreeze = (tempFreeze * 10) + currentHoverSet
                elif event.key == pygame.K_DELETE:
                    tempFreeze = tempFreeze // 10
                elif event.key == pygame.K_SPACE and tempFreeze != 0:
                    freeze = tempFreeze
                    tempFreeze = 0
                else: currentHoverSet = changeHoverSettings(currentHoverSet,event)


        
    
    pygame.display.update()

pygame.init()

# Set up the screen
screen = pygame.display.set_mode((400, 200))
pygame.display.set_caption("Message Box Example")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Fonts
font = pygame.font.Font(None, 32)

def draw_message_box(message):
    screen.fill(WHITE)
    
    # Draw message box
    pygame.draw.rect(screen, GRAY, (50, 50, 300, 100))
    
    # Draw message text
    text_surface = font.render(message, True, BLACK)
    text_rect = text_surface.get_rect(center=(200, 100))
    screen.blit(text_surface, text_rect)
    
    # Update the display
    pygame.display.flip()

def main():
    message = ""
    draw_message_box(message)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
                
if __name__ == "__main__":
    main()

