from board import GridStates, TTTBoardDecision
import json

class TableLearning(object):
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