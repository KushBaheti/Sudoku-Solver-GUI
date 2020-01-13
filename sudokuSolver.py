#   Find row, col of an unassigned cell
#   If there is none, return true

#   For digits from 1 to 9
#     a) If there is no conflict for digit at row, col
#         assign digit to row, col and recursively try fill in rest of grid
#     b) If recursion successful, return true
#     c) Else, remove digit and try another

#   If all digits have been tried and nothing worked, return false

# TODO:
# make GUI
# generate sudoku puzzle

def printBoard(board):
    boardSize = len(board)
    for row in range(boardSize):
        for column in range(boardSize):
            print(board[row][column], end=" ")
        print()

def isValid(board, row, column, choice):
    # Check row
    for i in range(len(board)):
        if board[row][i] == choice:
            return False
    
    # Check column
    for i in range(len(board)):
        if board[i][column] == choice:
            return False

    # Check subgrid
    subGridSize = int(len(board) ** (1/2))
    c = column - (column % subGridSize)
    r = row - (row % subGridSize)
    for i in range(subGridSize):
        for j in range(subGridSize):
            if board[i+r][j+c] == choice:
                return False

    return True

def findUnassignedCell(board, boardSize):
    for row in range(boardSize):
        for column in range(boardSize):
            if board[row][column] == 0:
                return [row, column]
    return [-1, -1]

def solveSudoku(board):
    boardSize = len(board)
    choices = []
    for i in range(boardSize):
        choices.append(i+1)

    #  Find row, col of an unassigned cell
    row, column = findUnassignedCell(board, boardSize)
    if row == -1:
        return True

    for choice in choices:
        if (isValid(board, row, column, choice)):
                board[row][column] = choice
                if (solveSudoku(board)):
                    return True
                board[row][column] = 0

    return False

# Main function
if __name__ == "__main__":

    # Create 2D board
    board = [
        [3, 0, 6, 5, 0, 8, 4, 0, 0], 
        [5, 2, 0, 0, 0, 0, 0, 0, 0], 
        [0, 8, 7, 0, 0, 0, 0, 3, 1], 
        [0, 0, 3, 0, 1, 0, 0, 8, 0], 
        [9, 0, 0, 8, 6, 3, 0, 0, 5], 
        [0, 5, 0, 0, 9, 0, 6, 0, 0], 
        [1, 3, 0, 0, 0, 0, 2, 5, 0], 
        [0, 0, 0, 0, 0, 0, 0, 7, 4], 
        [0, 0, 5, 2, 0, 6, 3, 0, 0]
    ]

    # board = [
    #     [5, 3, 0, 0, 7, 0, 0, 0, 0], 
    #     [6, 0, 0, 1, 9, 5, 0, 0, 0], 
    #     [0, 9, 8, 0, 0, 0, 0, 6, 0], 
    #     [8, 0, 0, 0, 6, 0, 0, 0, 3], 
    #     [4, 0, 0, 8, 0, 3, 0, 0, 1],
    #     [7, 0, 0, 0, 2, 0, 0, 0, 6], 
    #     [0, 6, 0, 0, 0, 0, 2, 8, 0],
    #     [0, 0, 0, 4, 1, 9, 0, 0, 5],
    #     [0, 0, 0, 0, 8, 0, 0, 7, 9]
    # ]

    # If succesfully solved, print solved board
    if (solveSudoku(board)):
        printBoard(board)
    else:
        print("No solution exists.")

