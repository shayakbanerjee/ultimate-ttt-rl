import itertools

class GridStates():
    EMPTY = ' '
    PLAYER_X = 'X'
    PLAYER_O = 'O'

class TTTBoardDecision():
    ACTIVE = 0
    DRAW = 1
    WON_X = 2
    WON_O = 3

class TTTBoard():
    def __init__(self):
        self.board = self.emptyState()
        self.decision = TTTBoardDecision.ACTIVE

    def emptyState(self):
        return [[GridStates.EMPTY, GridStates.EMPTY, GridStates.EMPTY],
                [GridStates.EMPTY, GridStates.EMPTY, GridStates.EMPTY],
                [GridStates.EMPTY, GridStates.EMPTY, GridStates.EMPTY]]

    def determineBoardState(self):
        def winCheck(listOfThree):
            return len(set(listOfThree)) == 1 and GridStates.EMPTY not in listOfThree

        def getWinState(listOfThree):
            return TTTBoardDecision.WON_O if GridStates.PLAYER_O in listOfThree else TTTBoardDecision.WON_X

        for row in self.board:  # Check rows first
            if winCheck(row):  # The row was won
                self.decision = getWinState(row)
                return
        for j in range(3):  # Check columns next
            column = [self.board[0][j], self.board[1][j], self.board[2][j]]
            if winCheck(column):
                self.decision = getWinState(column)
                return
        diagonal1 = [self.board[i][j] for (i,j) in zip(list(range(3)), list(range(3)))]
        diagonal2 = [self.board[i][j] for (i, j) in zip(list(range(3)), list(range(2,-1,-1)))]
        if winCheck(diagonal1):
            self.decision = getWinState(diagonal1)
            return
        if winCheck(diagonal2):
            self.decision = getWinState(diagonal2)
            return
        if [x for x in self.board if GridStates.EMPTY in x]:  # Board is full
            self.decision = TTTBoardDecision.ACTIVE
        else:
            self.decision = TTTBoardDecision.DRAW

    def makeMove(self, who, i, j, verbose=True):   # who is PLAYER_X or PLAYER_O
        if self.board[i][j] != GridStates.EMPTY:
            print('That location is not empty')
            return
        self.board[i][j] = who
        #self.printBoard()
        self.determineBoardState()
        if self.decision == TTTBoardDecision.DRAW and verbose is True:
            print('This TTT game was drawn!')
        elif self.decision != TTTBoardDecision.ACTIVE and verbose is True:
            print('This TTT game was won by %s'%(GridStates.PLAYER_X if self.decision == TTTBoardDecision.WON_X else GridStates.PLAYER_O))

    def printBoard(self):
        delimiter = "-------------"
        BOARD_FORMAT = "%s\n%s\n%s\n%s\n%s\n%s\n%s"%(delimiter, self.getBoardRowString(0),
                                                     delimiter, self.getBoardRowString(1),
                                                     delimiter, self.getBoardRowString(2), delimiter)
        cells = []
        for (i,j) in itertools.product(list(range(3)), list(range(3))):
            cells.append(self.board[i][j])
        print(BOARD_FORMAT.format(*cells))

    def getBoardRowString(self, row):
        return "| {0} | {1} | {2} |".format(*self.board[row])

    def getGrid(self, i, j):
        return self.board[i][j]

    def getEmptyBoardPlaces(self):
        emptyPlaces = []
        for (i,j) in itertools.product(list(range(3)), list(range(3))):
            if self.board[i][j] == GridStates.EMPTY:
                emptyPlaces.append((i,j))
        return emptyPlaces

    def getBoardState(self):
        return ''.join([''.join(row) for row in self.board])

    def getDoesBoardHaveEmptyCell(self):
        for (i,j) in itertools.product(list(range(3)), list(range(3))):
            if self.board[i][j] == GridStates.EMPTY:
                return True
        return False

    def getBoardDecision(self):
        return self.decision

if __name__ == '__main__':
    b = TTTBoard()
    b.makeMove(GridStates.PLAYER_X, 1, 1)
    b.makeMove(GridStates.PLAYER_O, 0, 0)
    b.makeMove(GridStates.PLAYER_X, 1, 2)
    b.makeMove(GridStates.PLAYER_O, 1, 0)
    b.makeMove(GridStates.PLAYER_X, 2, 0)
    b.makeMove(GridStates.PLAYER_O, 0, 2)
    b.makeMove(GridStates.PLAYER_X, 0, 1)
    b.makeMove(GridStates.PLAYER_O, 2, 1)
    b.makeMove(GridStates.PLAYER_X, 2, 2)