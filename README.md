Machine Learning midterm project - AutoChess
---

## Description
This is project try to make an autonomous chess engine.


Dataset
-----

[Download](https://www.ficsgames.org/download.html) dataset of year 2019 (~1Gb).


TODOs
-----
- Fix game play
- Generate training dataset
- Implement simple neural network model or ml model
- Implement minimax, alpha-beta, ...
- Implement valuator


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
