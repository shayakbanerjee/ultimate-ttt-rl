from board import TTTBoardDecision, TTTBoard
from learning import TableLearning
import random

class TTTPlayer(object):
    def __init__(self):
        self.board = None
        self.player = None

    def setBoard(self, board, player):
        self.board = board
        self.player = player   # X or O

    def isBoardActive(self):
        return (self.board is not None and self.board.getBoardDecision() == TTTBoardDecision.ACTIVE)

    def makeNextMove(self):
        raise NotImplementedError

    def learnFromMove(self, prevBoardState):
        raise NotImplementedError

    def startNewGame(self):
        pass

    def finishGame(self):
        pass

class RandomTTTPlayer(TTTPlayer):
    def makeNextMove(self):
        previousState = self.board.getBoardState()
        if self.isBoardActive():
            emptyPlaces = self.board.getEmptyBoardPlaces()
            pickOne = random.choice(emptyPlaces)
            self.board.makeMove(self.player, pickOne[0], pickOne[1])
        return previousState

    def learnFromMove(self, prevBoardState):
        pass  # Random player does not learn from move

class RLTTTPlayer(TTTPlayer):
    def __init__(self):
        self.learningAlgo = TableLearning()
        super(RLTTTPlayer, self).__init__()

    def printValues(self):
        self.learningAlgo.printValues()

    def testNextMove(self, state, i, j):
        boardCopy = list(state)
        boardCopy[3*i+j] = self.player
        return ''.join(boardCopy)

    def makeNextMove(self):
        previousState = self.board.getBoardState()
        if self.isBoardActive():
            emptyPlaces = self.board.getEmptyBoardPlaces()
            pickOne = random.choice(emptyPlaces)
            if random.uniform(0, 1) < 0.8:      # Make a random move with probability 0.2
                moveChoices = {}
                for (i, j) in emptyPlaces:
                    possibleNextState = self.testNextMove(previousState, i, j)
                    moveChoices[(i, j)] = self.learningAlgo.getBoardStateValue(self.player, self.board, possibleNextState)
                pickOne = max(moveChoices, key=moveChoices.get)
            self.board.makeMove(self.player, pickOne[0], pickOne[1])
        return previousState

    def learnFromMove(self, prevBoardState):
        self.learningAlgo.learnFromMove(self.player, self.board, prevBoardState)

if __name__  == '__main__':
    board = TTTBoard()
    player1 = RLTTTPlayer()
    player2 = RandomTTTPlayer()
