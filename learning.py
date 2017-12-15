from board import GridStates, TTTBoardDecision
import json
from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.utils import plot_model
import numpy as np

class GenericLearning(object):
    def getBoardStateValue(self, player, board, boardState):
        raise NotImplementedError

    def learnFromMove(self, player, board, prevBoardState):
        raise NotImplementedError

    def saveModel(self, filename):
        raise NotImplementedError

    def loadModel(self, filename):
        raise NotImplementedError

class TableLearning(GenericLearning):
    def __init__(self, DecisionClass=TTTBoardDecision):
        self.values = {}
        self.DecisionClass = DecisionClass

    def getBoardStateValue(self, player, board, boardState):
        decision = board.getBoardDecision()
        if decision == self.DecisionClass.WON_X:
            self.values[boardState] = 1.0 if player == GridStates.PLAYER_X else 0.0
        if decision == self.DecisionClass.WON_O:
            self.values[boardState] = 1.0 if player == GridStates.PLAYER_O else 0.0
        if boardState not in self.values:
            self.values[boardState] = 0.5
        return self.values[boardState]

    def learnFromMove(self, player, board, prevBoardState):
        curBoardState = board.getBoardState()
        curBoardStateValue = self.getBoardStateValue(player, board, curBoardState)
        if prevBoardState not in self.values:
            self.getBoardStateValue(player, board, prevBoardState)
        self.values[prevBoardState] = self.values[prevBoardState] + 0.2*(curBoardStateValue - self.values[prevBoardState])

    def printValues(self):
        from pprint import pprint
        #pprint(filter(lambda x: x!=0.5, self.values.values()))
        pprint(self.values)
        print 'Total number of states: %s' % (len(self.values))
        print 'Total number of knowledgeable states: %s' % (len(filter(lambda x: x!=0.5, self.values.values())))

    def saveLearning(self, filename):
        json.dump(self.values, open(filename,'w'))

    def loadLearning(self, filename):
        self.values = json.load(open(filename, 'r'))


class NNUltimateLearning(GenericLearning):
    STATE_TO_NUMBER_MAP = {GridStates.EMPTY: 0, GridStates.PLAYER_O: -1, GridStates.PLAYER_X: 1}

    def __init__(self, DecisionClass=TTTBoardDecision):
        self.DecisionClass = DecisionClass
        self.initializeModel()

    def initializeModel(self):
        self.model = Sequential()
        self.model.add(Dense(81, input_dim=81, activation='relu'))
        self.model.add(Dense(81, activation='relu'))
        self.model.add(Dense(1, activation='sigmoid'))
        self.model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
        plot_model(self.model, to_file='model.png')

    def convertBoardStateToInput(self, boardState):
        return np.asarray([map(lambda x: self.STATE_TO_NUMBER_MAP.get(x), boardState)])

    def trainModel(self, boardState, y):
        self.model.fit(self.convertBoardStateToInput(boardState), np.asarray([y]), verbose=0)

    def getPrediction(self, boardState):
        return self.model.predict(self.convertBoardStateToInput(boardState))[0]

    def getBoardStateValue(self, player, board, boardState):  #TODO: Can batch the inputs to do several predictions at once
        decision = board.getBoardDecision()
        predY = self.getPrediction(boardState)[0]
        if decision == self.DecisionClass.WON_X:
            predY = 1.0 if player == GridStates.PLAYER_X else 0.0
            self.trainModel(boardState, predY)
        if decision == self.DecisionClass.WON_O:
            predY = 1.0 if player == GridStates.PLAYER_O else 0.0
            self.trainModel(boardState, predY)
        return predY

    def learnFromMove(self, player, board, prevBoardState):
        curBoardState = board.getBoardState()
        curBoardStateValue = self.getBoardStateValue(player, board, curBoardState)
        prevBoardStateValue = self.getPrediction(prevBoardState)
        trainY = prevBoardStateValue + 0.2 * (curBoardStateValue - prevBoardStateValue)
        self.trainModel(prevBoardState, trainY)

    def printValues(self):
        pass

    def saveLearning(self, filename):
        self.model.save(filename)

    def loadLearning(self, filename):
        self.model = load_model(filename)
