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

The co-ordinate system is shown below, and is the same for the master board, as well as any tile within it:
![ultimate tic tac toe image](https://github.com/shayakbanerjee/ultimate-ttt-rl/raw/master/figures/coordinate_system.png)

## Players
There are two implemented bots for playing the game
1. `RandomUTTTPlayer` who makes moves at random
1. `RLUTTTPlayer` who makes moves based on a user-supplied learning algorithm

To play the game with one or a combination of these bots, use the `SingleGame` class. E.g. with two random players
```python
    from game import SingleGame
    from ultimateplayer import RandomUTTTPlayer
    from ultimateboard import UTTTBoard, UTTTBoardDecision
    
    player1, player2 = RandomUTTTPlayer(), RandomUTTTPlayer()
    game = SingleGame(player1, player2, UTTTBoard, UTTTBoardDecision)
    result = game.playAGame()
```
When using the RL player, it will need to be initialized with a learning algorithm of your choice. I've already provided two sample learning algorithms: `TableLearning` and `NNUltimateLearning`
```python
    from game import SingleGame
    from learning import TableLearning
    from ultimateplayer import RandomUTTTPlayer, RLUTTTPlayer
    from ultimateboard import UTTTBoard, UTTTBoardDecision
    
    player1, player2 = RLUTTTPlayer(TableLearning(UTTTBoardDecision)), RandomUTTTPlayer() 
    game = SingleGame(player1, player2, UTTTBoard, UTTTBoardDecision)
    result = game.playAGame()
```

## Learning Algorithm
The reinforcement learning (RL) player uses a learning algorithm to improve its chances of winning as it plays a number of games and learns about different positions. The learning algorithm is the key piece to the puzzle for making the RL bot improve its chances of winning over time. There is a generic template provided for the learning algorithm:
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
Every *board state* is an 81-character string which represents a raster scan of the entire 9x9 board (row-wise). You can map this to numeric entries as necessary.
Here's an example state: `"    X                               O   XO OO    X                 X        X    "`

## Using your own learning algorithm
Simply implement your learning model e.g. `MyLearningModel` by inheriting from `GenericLearning`. Then instantiate the provided reinforcement learning bot with an instance of this model:
```python
from ultimateboard import UTTTBoardDecision
from learning import GenericLearning
import random
from ultimateplayer import RLUTTTPlayer

class MyLearningModel(GenericLearning):
   def getBoardStateValue(self, player, board, boardState):
       # Your implementation here
       value = random.uniform() # As an example (and a very poor one)
       return value   # Must be a numeric value
   
   def learnFromMove(self, player, board, prevBoardState):
       # Your implementation here - learn some value for the previousBoardState
       pass

learningModel = MyLearningModel(UTTTBoardDecision)
learningPlayer = RLUTTTPlayer(learningModel)
```

## Sequence of games
More often than not you will want to just play a sequence of games and observe the learning over time. Code samples for that have been provided and uses the `GameSequence` class
```python
from ultimateplayer import RLUTTTPlayer, RandomUTTTPlayer
from game import GameSequence
from ultimateboard import UTTTBoard, UTTTBoardDecision

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