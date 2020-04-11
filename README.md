Machine Learning midterm project - AutoChess
---

##Description
This is project try to make an autonomous chess engine.


##Dataset
[Download](https://www.ficsgames.org/download.html) dataset of year 2019 (~1Gb).


##Structure
  - state: store game states (include white and black)
  - main: play game
  - model: neural network
  - train: train and test model

## api:
  - move(oldState, newState, promotion=None)
    - human moves
    - check legal move
    - computer move
  - newgame()
