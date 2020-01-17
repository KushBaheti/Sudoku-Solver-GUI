import pygame
import time
pygame.font.init()

#   use valid to make sure user entry can go into board
#   if valid, then solve current board to ensure there is a solution from current stage
#   if true allow, else error

# Grid holds Boxes in row-column structure
class Grid:
    board = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

    def __init__(self, rows, cols, width, height, win):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.win = win
        self.boxes = [[Box(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.selected = None
        self.model = None
        self.updateModel()

    # model is the board sent to solver to check validity (excludes pencil marks)
    def updateModel(self):
        self.model = [[self.boxes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    # set permanent (non-pencil mark) value if valid and solvable
    def place(self, choice):
        row, col = self.selected
        if self.boxes[row][col].value == 0:
            self.boxes[row][col].set(choice)
            self.updateModel()

            if isValid(self.model, row, col, choice) and self.solve():
                return True
            else:
                self.boxes[row][col].set(0)
                self.boxes[row][col].setTemp(0)
                self.updateModel()
                return False
        else:
            return True

    # set temp (pencil mark) value
    def sketch(self, tempChoice):
        row, col = self.selected
        self.boxes[row][col].setTemp(tempChoice)

    # draw sudoku board and values in boxes
    def draw(self):
        gap = self.width / 9
        for i in range(self.rows + 1):
            if i % 3 == 0 and  i != 0:
                thickness = 4
            else:
                thickness = 1
            pygame.draw.line(self.win, (0, 0, 0), (0, i*gap), (self.width, i*gap), thickness)
            pygame.draw.line(self.win, (0, 0, 0), (i*gap, 0), (i*gap, self.height), thickness)

        for i in range(self.rows):
            for j in range(self.cols):
                self.boxes[i][j].draw(self.win)

    # select box pressed
    def select(self, row, col):
        # reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.boxes[i][j].selected = False

        self.boxes[row][col].selected = True
        self.selected = (row, col)

    # select box navigated to using arrow keys
    def arrowKeySelect(self, deltaRow, deltaCol):
        row, col = self.selected or [0, 0]
        if row + deltaRow < 9 and row + deltaRow >= 0 and col + deltaCol < 9 and col + deltaCol >= 0:
            self.select(row + deltaRow, col + deltaCol)
        
    # remove pencil mark on selected box
    def clear(self):
        row, col = self.selected
        if self.boxes[row][col].value == 0:
            self.boxes[row][col].setTemp(0)

    # return position (indices) of box clicked
    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y), int(x)) # opposite because we are sending back the INDEX of box
        else:
            return None

    # check if any empty box left on board
    def isFinished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.boxes[i][j].value == 0:
                    return False
        return True

    # solve sudoku board from current state
    def solve(self):
        find = findUnassignedCell(self.model)
        if not find:
            return True
        else:
            row, column = find

        for i in range(1, 10):
            if isValid(self.model, row, column, i):
                self.model[row][column] = i
                if self.solve():
                    return True
                self.model[row][column] = 0
        return False

    # solve sudoku board along with visual representation of backtracking algorithm
    def solveGUI(self):
        self.updateModel()
        find = findUnassignedCell(self.model)
        if not find:
            return True
        else:
            row, column = find

        for i in range(1, 10):
            if isValid(self.model, row, column, i):
                self.model[row][column] = i
                self.boxes[row][column].set(i)
                self.boxes[row][column].drawChange(self.win, True)
                self.updateModel()
                pygame.display.update()
                pygame.time.delay(100)

                if self.solveGUI():
                    return True
                
                self.model[row][column] = 0
                self.boxes[row][column].set(0)
                self.boxes[row][column].drawChange(self.win, False)
                self.updateModel()
                pygame.display.update()
                pygame.time.delay(100)

# A Box object represents one of the 81 boxes to be filled in the sudoku board
class Box:
    rows = 9
    cols = 9
    
    def __init__(self, value, row, col, width, height):
        self.value = value
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.temp = 0
        self.selected = False

    # draw values in box and highlight currently selected box
    def draw(self, win):
        font = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = font.render(str(self.temp), 1, (128,128,128))
            win.blit(text, (x+5, y+5))
        elif self.value != 0:
            text = font.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))
        
        if self.selected:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)

    # used by solveGUI to implement visual representation of backtracking algorithm
    def drawChange(self, win, correctEntry = True):
        font = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        pygame.draw.rect(win, (255, 255, 255), (x, y, gap, gap), 0)

        text = font.render(str(self.value), 1, (0, 0, 0))
        win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

        if correctEntry:
            pygame.draw.rect(win, (0, 255, 0), (x, y, gap, gap), 3)
        else:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)

    # set permanent (non-pencil mark) value of box
    def set(self, value):
        self.value = value

    # set temporary (pencil mark) value of box
    def setTemp(self, temp):
        self.temp = temp

# find next empty box
def findUnassignedCell(board):
    for row in range(9):
        for column in range(9):
            if board[row][column] == 0:
                return [row, column]
    return None

# check if placement is valid
def isValid(board, row, column, choice):
    # Check row
    for i in range(9):
        if board[row][i] == choice and column != i:
            return False
    
    # Check column
    for i in range(9):
        if board[i][column] == choice and row != i:
            return False

    # Check subgrid
    c = column - (column % 3)
    r = row - (row % 3)
    
    for i in range(3):
        for j in range(3):
            if board[i+r][j+c] == choice and [i+r, j+c] != [row, column]:
                return False
    return True

# draw contents of window excluding sudoku board itself
def redrawWindow(win, board, elapsedTime, strikes):
    win.fill((255, 255, 255))
    font = pygame.font.SysFont("comicsans", 40)
    text = font.render("Time:" + formatTime(elapsedTime), 1, (0, 0, 0))
    win.blit(text, (540 - 190, 560))
    text = font.render("X " * strikes, 1, (255, 0, 0))
    win.blit(text, (20, 560))
    board.draw()
    if strikes == 3:
        pygame.draw.rect(win, (0, 0, 0), (95, 560, 250, 25), 1)
        font = pygame.font.SysFont("comicsans", 30)
        text = font.render("Oh no, you striked out :/", 1, (255, 0, 0))
        win.blit(text, (100, 563))

# formats and returns the timer
def formatTime(secs):
    sec = secs % 60
    min = secs // 60
    hour = min // 60
    return str(hour).zfill(2) + ":" + str(min).zfill(2) + ":" + str(sec).zfill(2)

# if game is lost (by making 3 mistakes), board is solved using solveGUI
def lostGame(win, board):
    pygame.time.delay(3000)
    board.solveGUI()

def main():
    win = pygame.display.set_mode((540, 600))
    pygame.display.set_caption("Sudoku")
    board = Grid(9, 9, 540, 540, win)
    key = None
    run = True
    start = time.time()
    strikes = 0

    while run:

        elapsedTime = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9

                if event.key == pygame.K_LEFT:
                    board.arrowKeySelect(0, -1)
                    key = None
                if event.key == pygame.K_RIGHT:
                    board.arrowKeySelect(0, 1)
                    key = None
                if event.key == pygame.K_UP:
                    board.arrowKeySelect(-1, 0)
                    key = None
                if event.key == pygame.K_DOWN:
                    board.arrowKeySelect(1, 0)
                    key = None
                
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None
                
                if event.key == pygame.K_SPACE:
                    board.solveGUI()
                
                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.boxes[i][j].temp != 0:
                        if board.place(board.boxes[i][j].temp):
                            print("Success")
                        else:
                            print("Wrong")
                            strikes += 1
                        key = None

                        if board.isFinished():
                            print("Game over")
                            
            if event.type == pygame.MOUSEBUTTONDOWN:
               pos = pygame.mouse.get_pos()
               clicked = board.click(pos)
               if clicked:
                   board.select(clicked[0], clicked[1])
                   key = None

        if board.selected and key != None:
            board.sketch(key)

        redrawWindow(win, board, elapsedTime, strikes)
        pygame.display.update()
        if strikes == 3:
            lostGame(win, board)

main()
pygame.quit()

