Machine Learning midterm project - SimpleChess
---

This is a ML project :))


Dataset
-----

[Download](https://www.ficsgames.org/download.html) dataset of year 2019 (~1Gb).


TODOs
-----
- [x] Fix game play
- [ ] Generate training dataset
  - [ ] Explore state encoding strategies
  - [ ] Gen state sets
  - [ ] Gen next move sets
- [ ] Implement simple neural network model or ml model
  - [ ] Model to evaluate a state (% win)
  - [ ] Model to predict next piece to move
- [ ] Implement search algorithms
  - [x] [Minimax](https://en.wikipedia.org/wiki/Minimax#Minimax\_algorithm\_with\_alternate\_moves)
  - [ ] [Alpha-Beta pruning](https://en.wikipedia.org/wiki/Alpha-beta\_pruning)
- [ ] Implement valuator
  - [x] Random
  - [ ] [Simple](https://www.chessprogramming.org/Simplified\_Evaluation\_Function)

Usage
-----

```
  pip install -r requirements.txt
  python3 main.py
```


Idea
-----
- Encode a board by vector of 8x8x12, label -1, 0, 1
  - Encode using piece position
- First train a model to evaluate a chess board (win, lose, draw)
- In general: minimax work on all next possible move --> too many possibility
- Then train a model to predict which piece to move
- Minimax only work on that predicted piece --> reduce search space
