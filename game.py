from board import TTTBoardDecision, GridStates, TTTBoard
from ultimateboard import UTTTBoard, UTTTBoardDecision
from player import RandomTTTPlayer, RLTTTPlayer
from ultimateplayer import RandomUTTTPlayer, RLUTTTPlayer
from plotting import drawXYPlotByFactor
import os

class GameSequence(object):
    def __init__(self, numberOfGames, player1, player2, BoardClass=TTTBoard, BoardDecisionClass=TTTBoardDecision):
        self.player1 = player1
        self.player2 = player2
        self.numberOfGames = numberOfGames
        self.BoardClass = BoardClass
        self.BoardDecisionClass = BoardDecisionClass

    def playAGame(self, board):
        while board.getBoardDecision() == self.BoardDecisionClass.ACTIVE:
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
            board = self.BoardClass()
            results.append(self.playAGame(board))
        xpct, opct, drawpct = float(results.count(self.BoardDecisionClass.WON_X))/float(self.numberOfGames), \
                              float(results.count(self.BoardDecisionClass.WON_O))/float(self.numberOfGames), \
                              float(results.count(self.BoardDecisionClass.DRAW))/float(self.numberOfGames)
        return (xpct, opct, drawpct)

def playTTTAndPlotResults():
    learningPlayer = RLTTTPlayer()
    randomPlayer = RandomTTTPlayer()
    results = []
    numberOfSetsOfGames = 40
    for i in range(numberOfSetsOfGames):
        games = GameSequence(100, randomPlayer, learningPlayer)
        results.append(games.playGamesAndGetWinPercent())
    plotValues = {'X Win Fraction': zip(range(numberOfSetsOfGames), map(lambda x: x[0], results)),
                  'O Win Fraction': zip(range(numberOfSetsOfGames), map(lambda x: x[1], results)),
                  'Draw Fraction': zip(range(numberOfSetsOfGames), map(lambda x: x[2], results))}
    drawXYPlotByFactor(plotValues, 'Set Number', 'Fraction')

def playUltimateAndPlotResults():
    learningPlayer = RLUTTTPlayer()
    randomPlayer = RandomUTTTPlayer()
    results = []
    numberOfSetsOfGames = 1
    for i in range(numberOfSetsOfGames):
        games = GameSequence(1000, learningPlayer, randomPlayer, BoardClass=UTTTBoard, BoardDecisionClass=UTTTBoardDecision)
        results.append(games.playGamesAndGetWinPercent())
    plotValues = {'X Win Fraction': zip(range(numberOfSetsOfGames), map(lambda x: x[0], results)),
                  'O Win Fraction': zip(range(numberOfSetsOfGames), map(lambda x: x[1], results)),
                  'Draw Fraction': zip(range(numberOfSetsOfGames), map(lambda x: x[2], results))}
    drawXYPlotByFactor(plotValues, 'Set Number', 'Fraction')

if __name__ == '__main__':
    #playTTTAndPlotResults()
    playUltimateAndPlotResults()