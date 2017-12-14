from board import TTTBoardDecision, GridStates, TTTBoard
from player import RandomTTTPlayer, RLTTTPlayer
from plotting import drawXYPlotByFactor

class GameSequence(object):
    def __init__(self, numberOfGames, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.numberOfGames = numberOfGames

    def playAGame(self, board):
        while board.getBoardDecision() == TTTBoardDecision.ACTIVE:
            self.player1.setBoard(board, GridStates.PLAYER_X)
            self.player2.setBoard(board, GridStates.PLAYER_O)
            pState1 = self.player1.makeNextMove()
            self.player1.learnFromMove(pState1)
            self.player2.learnFromMove(pState1)
            pState2 = self.player2.makeNextMove()
            self.player1.learnFromMove(pState2)
            self.player2.learnFromMove(pState2)
        return board.getBoardDecision()

    def playGamesAndGetWinPercent(self):
        results = []
        for i in range(self.numberOfGames):
            board = TTTBoard()
            results.append(self.playAGame(board))
        xpct, opct, drawpct = float(results.count(TTTBoardDecision.WON_X))/float(self.numberOfGames), \
                              float(results.count(TTTBoardDecision.WON_O))/float(self.numberOfGames), \
                              float(results.count(TTTBoardDecision.DRAW))/float(self.numberOfGames)
        return (xpct, opct, drawpct)

if __name__ == '__main__':
    learningPlayer = RLTTTPlayer()
    randomPlayer = RandomTTTPlayer()
    results = []
    numberOfSetsOfGames = 40
    for i in range(numberOfSetsOfGames):
        games = GameSequence(100, learningPlayer, randomPlayer)
        results.append(games.playGamesAndGetWinPercent())
    plotValues = {'X Win Fraction': zip(range(numberOfSetsOfGames), map(lambda x: x[0], results)),
                  'O Win Fraction': zip(range(numberOfSetsOfGames), map(lambda x: x[1], results)),
                  'Draw Fraction': zip(range(numberOfSetsOfGames), map(lambda x: x[2], results))}
    drawXYPlotByFactor(plotValues, 'Set Number', 'Fraction')
