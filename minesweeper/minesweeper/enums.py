# minesweeper/enums.py
from enum import Enum, auto

class GameState(Enum):
    READY = auto()
    RUNNING = auto()
    WON = auto()
    LOST = auto()

class CellState(Enum):
    HIDDEN = auto()
    REVEALED = auto()
    FLAGGED = auto()

class Difficulty(Enum):
    EASY = auto()     # 9x9, 10 mines
    MEDIUM = auto()   # 16x16, 40 mines
    HARD = auto()     # 30x16, 99 mines
