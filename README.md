# The Ultimate Tic Tac Toe Player Bot - with Reinforcement Learning
Reinforcement Learning based [Ultimate Tic Tac Toe](https://en.wikipedia.org/wiki/Ultimate_tic-tac-toe) player

![ultimate tic tac toe image](https://github.com/shayakbanerjee/ultimate-ttt-rl/raw/master/figures/sequence-of-moves.png)

## Background
For more details on the game of Ultimate Tic Tac Toe and why I started this project, refer to my [blog article](https://medium.com/@shayak_89588/playing-ultimate-tic-tac-toe-with-reinforcement-learning-7bea5b9d7252)

This project is meant for others to test their learning algorithms on an existing infrastructure for the Ultimate Tic Tac Toe game. This project has two implemented reinforcement learning bots, and a random bot (that pick moves at random) and they are good for testing against one another for benchmarking performance.

Credit to [this blog post](https://mathwithbaddrawings.com/2013/06/16/ultimate-tic-tac-toe/) for helping me understand the rules of the game with a lot of whiteboard drawings.

## Board
To instantiate and play a game of ultimate tic tac toe:
```python
    b = UTTTBoard()
    b.makeMove(GridStates.PLAYER_X, (1,1), (1,1))
    b.makeMove(GridStates.PLAYER_O, b.getNextBoardLocation(), (1, 2))
    b.makeMove(GridStates.PLAYER_X, b.getNextBoardLocation(), (1, 1))
```
To view the state of the board at any given time (you'll get a console output):
```python
    b.printBoard()
```
The co-ordinate system is shown below:

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
The `learnFromMove` calls are necessary for the bots to learn from every move. The example shows a random player against a reinforcement learning player, but you can choose to play RL vs RL or Random vs Random. Switching the order of player1 and player2 will assign `O` to the RL player and `X` to the Random player.

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
        
    def resetForNewGame(self):
        # Optional to implement. Reinitialize some form of state for each new game played
        pass
        
    def gameOver(self):
        # Option to implement. When a game is completed, run some sort of learning e.g. train a neural network
        pass
```
Any learning model must inherit from this class and implement the above methods. For examples see `TableLearning` for a lookup table based solution, and `NNUltimateLearning` for a neural network based solution.

## Using your own learning algorithm
Simply implement your learning model e.g. `MyLearningModel` by inheriting from `GenericLearning`. Then instantiate the provided reinforcement learning bot with an instance of this model:
```python
   from ultimateboard import UTTTBoardDecision
   
   class MyLearningModel(GenericLearning):
       def getBoardStateValue(self, player, board, boardState):
           # Your implementation here
           return value
       
       def learnFromMove(self, player, board, prevBoardState):
           # Your implementation here       
   
   learningModel = MyLearningModel(UTTTBoardDecision)
   learningPlayer = RLUTTTPlayer(learningModel)
```

## Sequence of games
More often than not you will want to just play a sequence of games and observe the learning over time. Code samples for that have been provided and uses the `GameSequence` class
```python
    learningPlayer = RLUTTTPlayer()
    randomPlayer = RandomUTTTPlayer()
    results = []
    numberOfSetsOfGames = 40
    for i in range(numberOfSetsOfGames):
        games = GameSequence(100, learningPlayer, randomPlayer, BoardClass=UTTTBoard, BoardDecisionClass=UTTTBoardDecision)
        results.append(games.playGamesAndGetWinPercent())
```

## Prerequisites
You will need to have [numpy](http://www.numpy.org) installed to work with this code. If using the neural network based learner in the examples provided, you will also need to have [keras](https://keras.io) installed. This will require one of [Tensorflow](https://github.com/tensorflow/tensorflow), [Theano](https://github.com/Theano/Theano) or [CNTK](https://github.com/Microsoft/cntk).