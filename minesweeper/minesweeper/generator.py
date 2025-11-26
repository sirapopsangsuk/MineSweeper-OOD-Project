# minesweeper/generator.py
import random
from typing import Iterable
from .types import Position

class MineGenerator:
    """วางระเบิดแบบสุ่มธรรมดา"""
    def place_mines(self, rows: int, cols: int, n_mines: int, forbidden: Iterable[Position]) -> set[Position]:
        forbidden_set = set(forbidden)
        all_positions = [Position(r, c) for r in range(rows) for c in range(cols) if Position(r, c) not in forbidden_set]
        mines = set(random.sample(all_positions, n_mines))
        return mines
