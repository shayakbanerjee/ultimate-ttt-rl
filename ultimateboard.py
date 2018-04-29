from board import TTTBoard, TTTBoardDecision, GridStates
import itertools

class UTTTBoardDecision():
    ACTIVE = 10
    DRAW = 11
    WON_X = 12
    WON_O = 13

class UTTTBoard(object):
    def __init__(self):
        self.board = self.emptyState()
        self.decision = UTTTBoardDecision.ACTIVE
        self.nextBoardLocation = [None, None]

    def emptyState(self):
        return [[TTTBoard(), TTTBoard(), TTTBoard()],
                [TTTBoard(), TTTBoard(), TTTBoard()],
                [TTTBoard(), TTTBoard(), TTTBoard()]]

    def determineBoardState(self):
        def winCheck(listOfThree):
            threeResults = list(map(lambda x: x.getBoardDecision(), listOfThree))
            return len(set(threeResults)) == 1 and threeResults[0] in [TTTBoardDecision.WON_O, TTTBoardDecision.WON_X]

        def getWinState(listOfThree):
            threeResults = map(lambda x: x.getBoardDecision(), listOfThree)
            return UTTTBoardDecision.WON_O if TTTBoardDecision.WON_O in threeResults else UTTTBoardDecision.WON_X

        for row in self.board:  # Check rows first
            if winCheck(row):  # The row was won
                self.decision = getWinState(row)
                return
        for j in range(3):  # Check columns next
            column = [self.board[0][j], self.board[1][j], self.board[2][j]]
            if winCheck(column):
                self.decision = getWinState(column)
                return
        diagonal1 = [self.board[i][j] for (i,j) in zip(range(3), range(3))]
        diagonal2 = [self.board[i][j] for (i, j) in zip(range(3), range(2,-1,-1))]
        if winCheck(diagonal1):
            self.decision = getWinState(diagonal1)
            return
        if winCheck(diagonal2):
            self.decision = getWinState(diagonal2)
            return
        self.decision = UTTTBoardDecision.DRAW
        for (i,j) in itertools.product(range(3), range(3)):
            if self.board[i][j].getBoardDecision() == TTTBoardDecision.ACTIVE:
                self.decision = UTTTBoardDecision.ACTIVE
                return

    def getEmptyBoardPlaces(self, whichBoard):
        nextBoard = self.board[whichBoard[0]][whichBoard[1]]
        return nextBoard.getEmptyBoardPlaces()

    def getActiveBoardLocations(self):
        activeBoards = []
        for (i, j) in itertools.product(range(3), range(3)):
            if self.board[i][j].getBoardDecision() == TTTBoardDecision.ACTIVE or self.board[i][j].getDoesBoardHaveEmptyCell():
                activeBoards.append((i, j))
        return activeBoards

    def getNextBoardLocation(self):
        return self.nextBoardLocation

    def makeMove(self, who, whichBoard, whichLocation):
        tttboard = self.board[whichBoard[0]][whichBoard[1]]
        i, j = whichLocation[0], whichLocation[1]
        if tttboard.getGrid(i, j) != GridStates.EMPTY:
            print('That location is not empty')
            return
        tttboard.makeMove(who, i, j, verbose=False)
        #self.printBoard()
        self.determineBoardState()
        if self.decision == UTTTBoardDecision.DRAW:
            print('This Ultimate-TTT game was drawn!')
            self.nextBoardLocation = [None, None]
        elif self.decision != UTTTBoardDecision.ACTIVE:
            print('This Ultimate-TTT game was won by %s'%(GridStates.PLAYER_X if self.decision == UTTTBoardDecision.WON_X else GridStates.PLAYER_O))
            self.nextBoardLocation = [None, None]
        else:
            nextTttboard = self.board[i][j]
            self.nextBoardLocation = [i, j] if nextTttboard.getBoardDecision() == TTTBoardDecision.ACTIVE else [None, None]

    def printBoard(self):
        delimiter = '-------------'*3+'\n'
        for boardRow in range(3):
            rowString = delimiter
            rowString += self.getBoardRowString(boardRow, 0) + '\n' + delimiter
            rowString += self.getBoardRowString(boardRow, 1) + '\n' + delimiter
            rowString += self.getBoardRowString(boardRow, 2) + '\n' + delimiter[:-1]
            print(rowString)

    def getBoardRowString(self, boardRow, row):
        rowString = ''
        for boardColumn in range(3):
            board = self.board[boardRow][boardColumn]
            rowString += board.getBoardRowString(row)
        return rowString

    def getBoardState(self):
        boardStrings = []
        for (i,j) in itertools.product(range(3), range(3)):
            board = self.board[i][j]
            [boardStrings.append(''.join(board.board[i])) for i in range(3)]
        return ''.join(boardStrings)

    def getBoardDecision(self):
        return self.decision

if __name__ == '__main__':
    b = UTTTBoard()
    b.makeMove(GridStates.PLAYER_X, (1,1), (1,1))
    b.makeMove(GridStates.PLAYER_O, b.getNextBoardLocation(), (1, 2))
    b.makeMove(GridStates.PLAYER_X, b.getNextBoardLocation(), (1, 1))
    b.makeMove(GridStates.PLAYER_O, b.getNextBoardLocation(), (0, 0))
    b.makeMove(GridStates.PLAYER_X, b.getNextBoardLocation(), (1, 1))
    b.makeMove(GridStates.PLAYER_O, b.getNextBoardLocation(), (2, 2))
    b.makeMove(GridStates.PLAYER_X, b.getNextBoardLocation(), (1, 1))
    b.makeMove(GridStates.PLAYER_O, b.getNextBoardLocation(), (2, 1))
    b.makeMove(GridStates.PLAYER_X, b.getNextBoardLocation(), (1, 1))
    b.printBoard()
    print(b.getBoardState())
