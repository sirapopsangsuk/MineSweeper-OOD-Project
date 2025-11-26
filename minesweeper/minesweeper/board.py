# minesweeper/board.py
from __future__ import annotations
from typing import Iterable
from .cell import Cell
from .types import Position

_NEIGHBORS = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]

class Board:
    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.grid: list[list[Cell]] = [[Cell() for _ in range(cols)] for _ in range(rows)]
        self.mines: set[Position] = set()
        self.revealed_count = 0
        self._total_cells = rows * cols

    def in_bounds(self, p: Position) -> bool:
        return 0 <= p.row < self.rows and 0 <= p.col < self.cols

    def neighbors(self, p: Position) -> list[Position]:
        ans = []
        for dr, dc in _NEIGHBORS:
            q = Position(p.row + dr, p.col + dc)
            if self.in_bounds(q):
                ans.append(q)
        return ans

    def set_mines(self, mine_positions: Iterable[Position]) -> None:
        self.mines = set(mine_positions)
        for pos in self.mines:
            self.grid[pos.row][pos.col].has_mine = True
        # คำนวณจำนวนระเบิดรอบ ๆ
        for r in range(self.rows):
            for c in range(self.cols):
                p = Position(r, c)
                if not self.grid[r][c].has_mine:
                    self.grid[r][c].adj_mines = sum(1 for n in self.neighbors(p) if self.grid[n.row][n.col].has_mine)

    def reveal(self, p: Position) -> bool:
        """เผยช่อง ถ้าเจอระเบิดคืน False (แพ้) ถ้าไม่ระเบิดคืน True"""
        cell = self.grid[p.row][p.col]
        if cell.is_revealed or cell.is_flagged:
            return True
        if cell.has_mine:
            cell.state = cell.state.REVEALED
            return False
        # safe
        self._reveal_area(p)
        return True

    def _reveal_area(self, start: Position) -> None:
        from collections import deque
        q = deque([start])
        visited = set()  # สร้าง Set สำหรับเก็บตำแหน่งที่เคยเพิ่มเข้า Queue
        while q:
            p = q.popleft()
            cell = self.grid[p.row][p.col]
            if cell.is_revealed or cell.is_flagged:
                continue

            cell.state = cell.state.REVEALED
            self.revealed_count += 1

            if cell.adj_mines == 0 and not cell.has_mine:
                for n in self.neighbors(p):
                    if not self.grid[n.row][n.col].is_revealed and not self.grid[n.row][n.col].has_mine:
                        if (n.row, n.col) not in visited:  # ตรวจสอบว่าเคยเพิ่มตำแหน่งนี้เข้า Queue แล้วหรือยัง
                            q.append(n)
                            visited.add((n.row, n.col))  # เพิ่มตำแหน่งที่เพิ่งเพิ่มเข้า Queue ลงใน visited


    def toggle_flag(self, p: Position) -> None:
        cell = self.grid[p.row][p.col]
        if cell.is_revealed:
            return
        cell.state = cell.state.HIDDEN if cell.is_flagged else cell.state.FLAGGED

    def is_cleared(self) -> bool:
        """ชนะเมื่อเปิดช่องที่ไม่ใช่ระเบิดครบ"""
        return self.revealed_count == (self._total_cells - len(self.mines)) 
