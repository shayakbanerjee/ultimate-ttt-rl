from ultimateboard import UTTTBoardDecision, UTTTBoard
from util import Util
from learning import TableLearning
import random
from copy import deepcopy

class UTTTPlayer(object):
    def __init__(self):
        self.board = None
        self.player = None

    def setBoard(self, board, player):
        self.board = board
        self.player = player   # X or O

    def isBoardActive(self):
        return (self.board is not None and self.board.getBoardDecision() == UTTTBoardDecision.ACTIVE)

    def makeNextMove(self):
        raise NotImplementedError

    def learnFromMove(self, prevBoardState):
        raise NotImplementedError

class RandomUTTTPlayer(UTTTPlayer):
    def makeNextMove(self):
        previousState = self.board.getBoardState()
        if self.isBoardActive():
            nextBoardLocation = self.board.getNextBoardLocation()
            if None in nextBoardLocation:
                activeBoardLocations = self.board.getActiveBoardLocations()
                nextBoardLocation = random.choice(activeBoardLocations)
            emptyPlaces = self.board.getEmptyBoardPlaces(nextBoardLocation)
            pickOne = random.choice(emptyPlaces)
            self.board.makeMove(self.player, nextBoardLocation, pickOne)
        return previousState

    def learnFromMove(self, prevBoardState):
        pass  # Random player does not learn from move

class RLUTTTPlayer(UTTTPlayer):
    def __init__(self):
        self.learningAlgo = TableLearning(UTTTBoardDecision)
        super(RLUTTTPlayer, self).__init__()

    def printValues(self):
        self.learningAlgo.printValues()

    def testNextMove(self, state, boardLocation, placeOnBoard):
        boardCopy = Util.nestedTupleToList(deepcopy(state))
        boardCopy[boardLocation[0]][boardLocation[1]][placeOnBoard[0]][placeOnBoard[1]] = self.player
        return Util.nestedListToTuple(boardCopy)

    def makeNextMove(self):
        previousState = self.board.getBoardState()
        if self.isBoardActive():
            nextBoardLocation = self.board.getNextBoardLocation()
            activeBoardLocations = [nextBoardLocation]
            if None in nextBoardLocation:
                activeBoardLocations = self.board.getActiveBoardLocations()
            if random.uniform(0, 1) < 0.8:      # Make a random move with probability 0.2
                moveChoices = {}
                for boardLocation in activeBoardLocations:
                    emptyPlaces = self.board.getEmptyBoardPlaces(boardLocation)
                    for placeOnBoard in emptyPlaces:
                        possibleNextState = self.testNextMove(previousState, boardLocation, placeOnBoard)
                        moveChoices[(tuple(boardLocation), placeOnBoard)] = self.learningAlgo.getBoardStateValue(self.player, self.board, possibleNextState)
                (chosenBoard, pickOne) = max(moveChoices, key=moveChoices.get)
            else:
                chosenBoard = random.choice(activeBoardLocations)
                emptyPlaces = self.board.getEmptyBoardPlaces(chosenBoard)
                pickOne = random.choice(emptyPlaces)
            self.board.makeMove(self.player, chosenBoard, pickOne)
        return previousState

    def learnFromMove(self, prevBoardState):
        self.learningAlgo.learnFromMove(self.player, self.board, prevBoardState)

if __name__  == '__main__':
    board = UTTTBoard()
    player1 = RandomUTTTPlayer()
    player2 = RLUTTTPlayer()