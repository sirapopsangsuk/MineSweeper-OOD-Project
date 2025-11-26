# tests/test_board.py
import pytest
from minesweeper.board import Board
from minesweeper.types import Position

def test_neighbors_center():
    b = Board(3,3)
    ns = b.neighbors(Position(1,1))
    assert len(ns) == 8

def test_reveal_safe_area():
    b = Board(3,3)
    b.set_mines({Position(0,0)})
    ok = b.reveal(Position(2,2))
    assert ok is True
    assert b.grid[2][2].is_revealed
