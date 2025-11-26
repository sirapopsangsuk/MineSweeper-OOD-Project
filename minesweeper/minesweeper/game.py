# minesweeper/game.py
from __future__ import annotations
from .board import Board
from .enums import GameState, Difficulty
from .types import Position
from .generator import MineGenerator

PRESETS = {
    Difficulty.EASY:   (9, 9, 10),
    Difficulty.MEDIUM: (16, 16, 40),
    Difficulty.HARD:   (25, 25, 99),
}

class Game:
    def __init__(self, difficulty: Difficulty = Difficulty.EASY, generator: MineGenerator | None = None):
        self.rows, self.cols, self.n_mines = PRESETS[difficulty]
        self.board = Board(self.rows, self.cols)
        self.state = GameState.READY
        self._first_click_done = False
        self.generator = generator or MineGenerator()

    def first_click(self, p: Position) -> None:
        # วางระเบิดหลังคลิกแรก (ห้ามวางทับช่องแรกและเพื่อนบ้านถ้าต้องการ)
        mines = self.generator.place_mines(self.rows, self.cols, self.n_mines, forbidden=[p])
        self.board.set_mines(mines)
        self.state = GameState.RUNNING
        self._first_click_done = True

    def left_click(self, p: Position) -> None:
        if self.state in (GameState.WON, GameState.LOST):
            return
        if not self._first_click_done:
            self.first_click(p)
        ok = self.board.reveal(p)
        if not ok:
            self.state = GameState.LOST
        elif self.board.is_cleared():
            self.state = GameState.WON

    def right_click(self, p: Position) -> None:
        if self.state == GameState.RUNNING or self.state == GameState.READY:
            self.board.toggle_flag(p)
