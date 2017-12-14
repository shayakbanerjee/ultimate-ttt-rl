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

    def winCheck(self, listOfThree):
        return len(set(listOfThree)) == 1 and GridStates.EMPTY not in listOfThree

    def getWinState(self, listOfThree):
        return TTTBoardDecision.WON_O if GridStates.PLAYER_O in listOfThree else TTTBoardDecision.WON_X

    def determineBoardState(self):
        for row in self.board:  # Check rows first
            if self.winCheck(row):  # The row was won
                self.decision = self.getWinState(row)
                return
        for j in range(3):  # Check columns next
            column = [self.board[0][j], self.board[1][j], self.board[2][j]]
            if self.winCheck(column):
                self.decision = self.getWinState(column)
                return
        diagonal1 = [self.board[i][j] for (i,j) in zip([0,1,2],[0,1,2])]
        diagonal2 = [self.board[i][j] for (i, j) in zip([0, 1, 2], [2, 1, 0])]
        if self.winCheck(diagonal1):
            self.decision = self.getWinState(diagonal1)
            return
        if self.winCheck(diagonal2):
            self.decision = self.getWinState(diagonal2)
            return
        if filter(lambda x: GridStates.EMPTY in x, self.board):  # Board is full
            self.decision = TTTBoardDecision.ACTIVE
        else:
            self.decision = TTTBoardDecision.DRAW

    def makeMove(self, who, i, j):   # who is PLAYER_X or PLAYER_O
        if self.board[i][j] != GridStates.EMPTY:
            print 'That location is not empty'
            return
        print '%s moves'%(who)
        self.board[i][j] = who
        #self.printBoard()
        self.determineBoardState()
        if self.decision == TTTBoardDecision.DRAW:
            print 'The game was drawn!'
        elif self.decision != TTTBoardDecision.ACTIVE:
            print 'The game was won by %s'%(GridStates.PLAYER_X if self.decision == TTTBoardDecision.WON_X else GridStates.PLAYER_O)

    def printBoard(self):
        delimiter = "-------------"
        BOARD_FORMAT = "%s\n| {0} | {1} | {2} |\n%s\n| {3} | {4} | {5} |\n%s\n| {6} | {7} | {8} |\n%s"%(delimiter, delimiter, delimiter, delimiter)
        cells = []
        for (i,j) in itertools.product(range(3), range(3)):
            cells.append(self.board[i][j])
        print BOARD_FORMAT.format(*cells)

    def getEmptyBoardPlaces(self):
        boardState = self.getBoardState()
        emptyPlaces = []
        for (i,j) in itertools.product([0,1,2], [0,1,2]):
            if boardState[i][j] == GridStates.EMPTY:
                emptyPlaces.append((i,j))
        return emptyPlaces

    def getBoardState(self):
        return tuple([tuple(row) for row in self.board])

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