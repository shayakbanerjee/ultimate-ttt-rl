from board import GridStates, TTTBoardDecision

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
        pprint(self.values)
        print 'Total number of states: %s' % (len(self.values))