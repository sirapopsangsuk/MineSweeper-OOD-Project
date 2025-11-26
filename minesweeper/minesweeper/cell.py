# minesweeper/cell.py
from dataclasses import dataclass
from .enums import CellState

@dataclass
class Cell:
    has_mine: bool = False
    adj_mines: int = 0
    state: CellState = CellState.HIDDEN

    @property
    def is_revealed(self) -> bool:
        return self.state == CellState.REVEALED

    @property
    def is_flagged(self) -> bool:
        return self.state == CellState.FLAGGED
