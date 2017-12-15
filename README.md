# The Ultimate Tic Tac Toe Player - with Reinforcement Learning
Reinforcement Learning based Ultimate Tic Tac Toe player

## Background
For more details on the game of Ultimate Tic Tac Toe and why I started this project, refer to my [blog article](https://medium.com/@shayak_89588/playing-ultimate-tic-tac-toe-with-reinforcement-learning-7bea5b9d7252)

This project is meant for others to test their learning algorithms on an existing infrastructure for the Ultimate Tic Tac Toe game. There are reinforcement learning bots, and random bots (who pick moves at random) and they are good for testing against one another

## Board
To instantiate and play a game of ultimate tic tac toe:
```python
    b = UTTTBoard()
    b.makeMove(GridStates.PLAYER_X, (1,1), (1,1))
    b.makeMove(GridStates.PLAYER_O, b.getNextBoardLocation(), (1, 2))
    b.makeMove(GridStates.PLAYER_X, b.getNextBoardLocation(), (1, 1))
```

## Players
There are two implemented bots for playing the game
1. `RandomUTTTPlayer` who makes moves at random
1. `RLUTTTPlayer` who makes moves based on a user-supplied learning algorithm

To play the game with these different bots.
```python
    def playAGame(self, board):
        player1 = RandomUTTTPlayer()
        player2 = RLUTTTPlayer()
        while board.getBoardDecision() == self.BoardDecisionClass.ACTIVE:
            player1.setBoard(board, GridStates.PLAYER_X)
            player2.setBoard(board, GridStates.PLAYER_O)
            pState1 = self.player1.makeNextMove()
            player1.learnFromMove(pState1)
            player2.learnFromMove(pState1)
            pState2 = self.player2.makeNextMove()
            player1.learnFromMove(pState2)
            player2.learnFromMove(pState2)
        return board.getBoardDecision()
```
The `learnFromMove` calls are optional, but necessary if the bots need to learn from every move. The example shows a random player against a reinforcement learning player, but you can choose to play RL vs RL or Random vs Random. Switching the order of player1 and player2 will assign `O` to the RL player and `X` to the Random player.

## Learning Algorithm
The learning algorithm is the key piece to the puzzle for making the RL bot improve its chances of winning over time. There is a generic template provided for the learning algorithm:
```python
class GenericLearning(object):
    def getBoardStateValue(self, player, board, boardState):
        # Return the perceived `value` of a given board state
        raise NotImplementedError

    def learnFromMove(self, player, board, prevBoardState):
        # Learn from the previous board state and the current state of the board
        raise NotImplementedError

    def saveModel(self, filename):
        # Save to file (use pass if no implementation is necessary)
        # Useful for saving intermediate states of the learning model
        raise NotImplementedError

    def loadModel(self, filename):
        # Load an intermediate state of the learning model from file
        # Use only if also saving the intermediate state above
        raise NotImplementedError
```
Any learning model must inherit from this class and implement the above methods. For examples see `TableLearning` for a lookup table based solution, and `NNUltimateLearning` for a neural network based solution.

## Sequence of games
More often than not you will want to just play a sequence of games and observe the learning over time. Code samples for that have been provided and use the `GameSequence` class
```python
    learningPlayer = RLUTTTPlayer()
    randomPlayer = RandomUTTTPlayer()
    results = []
    numberOfSetsOfGames = 40
    for i in range(numberOfSetsOfGames):
        games = GameSequence(100, learningPlayer, randomPlayer, BoardClass=UTTTBoard, BoardDecisionClass=UTTTBoardDecision)
        results.append(games.playGamesAndGetWinPercent())
```

Credit to [this blog post](https://mathwithbaddrawings.com/2013/06/16/ultimate-tic-tac-toe/) for helping me understand the rules of the game with a lot of whiteboard drawings.
