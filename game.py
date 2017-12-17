from board import TTTBoardDecision, GridStates, TTTBoard

class GameSequence(object):
    def __init__(self, numberOfGames, player1, player2, BoardClass=TTTBoard, BoardDecisionClass=TTTBoardDecision):
        self.player1 = player1
        self.player2 = player2
        self.numberOfGames = numberOfGames
        self.BoardClass = BoardClass
        self.BoardDecisionClass = BoardDecisionClass

    def playAGame(self, board):
        self.player1.startNewGame()
        self.player2.startNewGame()
        while board.getBoardDecision() == self.BoardDecisionClass.ACTIVE:
            self.player1.setBoard(board, GridStates.PLAYER_X)
            self.player2.setBoard(board, GridStates.PLAYER_O)
            pState1 = self.player1.makeNextMove()
            self.player1.learnFromMove(pState1)
            self.player2.learnFromMove(pState1)
            pState2 = self.player2.makeNextMove()
            self.player1.learnFromMove(pState2)
            self.player2.learnFromMove(pState2)
        self.player1.finishGame()
        self.player2.finishGame()
        return board.getBoardDecision()

    def playGamesAndGetWinPercent(self):
        results = []
        for i in range(self.numberOfGames):
            board = self.BoardClass()
            results.append(self.playAGame(board))
        xpct, opct, drawpct = float(results.count(self.BoardDecisionClass.WON_X))/float(self.numberOfGames), \
                              float(results.count(self.BoardDecisionClass.WON_O))/float(self.numberOfGames), \
                              float(results.count(self.BoardDecisionClass.DRAW))/float(self.numberOfGames)
        return (xpct, opct, drawpct)
