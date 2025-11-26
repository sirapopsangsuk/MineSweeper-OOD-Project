import os
from minesweeper.game import Game
from minesweeper.enums import Difficulty
from minesweeper.types import Position
import string

AZ = list(string.ascii_lowercase)

def clear_terminal():
    """ล้างหน้าจอเทอร์มินัล"""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_instructions():
    """แสดงคำแนะนำวิธีการเล่น"""
    print("----------------------------------------------------------------")
    print("|      l = left click to reveal cell , r = right click to flag |")
    print("|      Enter <l/r> <row> <column> example --> r 0 1            |")
    print("|      Enter 'restart' to restart game                         |")
    print("----------------------------------------------------------------")

def render(game: Game) -> None:
    clear_terminal()  # ล้างหน้าจอทุกครั้งที่ render
    display_instructions()  # แสดงคำแนะนำวิธีการเล่น

    b = game.board
    
    # แสดง header (คอลัมน์) ใช้ตัวเลขสำหรับคอลัมน์
    header = "  "
    for c in range(b.cols):
        if c == 10:
            # ใช้ ord() และ chr() เพื่อแปลงตัวเลขเป็นตัวอักษร A-Z
            header += f" {chr(c - 10 + ord('A'))} "
        elif c > 10:
            header += f"{chr(c - 10 + ord('B') - 1)} "
        else:
            header += f"{c:2d}"  # ใช้ตัวเลขสำหรับคอลัมน์

    print(header)
    # แสดงตาราง
    for r in range(b.rows):
        row_disp = []
        for c in range(b.cols):
            cell = b.grid[r][c]
            if cell.state.name == "HIDDEN":
                row_disp.append("■")
            elif cell.state.name == "FLAGGED":
                row_disp.append("⚑")
            else:
                row_disp.append("*" if cell.has_mine else (f"{cell.adj_mines}" if cell.adj_mines > 0 else " "))
        
        # แสดงแถว โดยใช้ตัวเลขสำหรับแถว ถ้า >= 10 ใช้ A-Z
        if r >= 10:
            print(f" {chr(r - 10 + ord('A')):2}" + " ".join(row_disp))  # แสดงแถว A-Z
        else:
            print(f"{r:2d} " + " ".join(row_disp))  # แสดงแถว 0-9

def get_difficulty_choice() -> Difficulty:
    """ให้ผู้ใช้เลือกระดับความยาก"""
    while True:
        print("เลือกระดับความยาก:")
        print("1. Easy")
        print("2. Medium")
        print("3. Hard")
        choice = input("กรุณากรอกหมายเลขที่เลือก (1/2/3): ")
        
        if choice == '1':
            return Difficulty.EASY
        elif choice == '2':
            return Difficulty.MEDIUM
        elif choice == '3':
            return Difficulty.HARD
        else:
            print("เลือกไม่ถูกต้อง กรุณากรอกใหม่.")

def restart_game(game: Game) -> bool:
    """ถามผู้เล่นว่าอยากเล่นใหม่หรือไม่"""
    while True:
        choice = input("ต้องการเริ่มเกมใหม่หรือไม่? (y/n/restart): ").lower()
        if choice == 'y' or choice == 'restart':
            # รีเซ็ตเกมใหม่และให้ผู้เล่นเลือกระดับความยากใหม่
            difficulty = get_difficulty_choice()  # รับระดับความยากใหม่
            game.__init__(difficulty)  # รีเซ็ตเกมใหม่
            return True
        elif choice == 'n':
            print("ขอบคุณที่เล่น Minesweeper!")
            return False
        else:
            print("กรุณากรอก 'y', 'n', หรือ 'restart'.")

def convert_row(row_input: str):
    """แปลง row จาก 0-25 เป็น 0-25"""
    if row_input.isdigit():  # ถ้าผู้ใช้กรอกเป็นตัวเลข
        row_input = int(row_input)
        return row_input
    elif row_input in AZ:
        return (ord(row_input.lower()) - 97) + 10 
        
    raise ValueError("แถวต้องเป็น 0-25")

def convert_col(col_input: str):
    """แปลง col จาก 0-9 เป็น 0-9"""
    if col_input.isdigit():  # ถ้าผู้ใช้กรอกเป็นตัวเลข
        col_input = int(col_input)
        return col_input
    elif col_input in AZ:
        return (ord(col_input.lower()) - 97) + 10 
    
    raise ValueError("คอลัมน์ต้องเป็น 0-9")

def main():
    difficulty = get_difficulty_choice()  # รับระดับความยากจากผู้ใช้
    game = Game(difficulty)

    while True:
        while game.state.name not in ("WON", "LOST"):
            render(game)
            cmd = input("[l/r/restart] row col > ").strip().split()
            if len(cmd) == 1 and cmd[0] == "restart":
                # รีสตาร์ทเกมระหว่างเล่นและให้เลือกระดับความยากใหม่
                difficulty = get_difficulty_choice()  # เลือกระดับความยากใหม่
                game.__init__(difficulty)  # รีเซ็ตเกมใหม่
                continue
            
            if len(cmd) != 3:
                print("คำสั่งไม่ถูกต้อง! กรุณากรอกใหม่.")
                continue
                
            kind, row_input, col_input = cmd[0], cmd[1], cmd[2]
            
            try:
                row = convert_row(row_input)  # แปลง row เป็นตัวเลข
                col = convert_col(col_input)  # แปลง col เป็นตัวเลข
                if kind == "l":
                    game.left_click(Position(row, col))
                    print(row , col)
                elif kind == "r":
                    game.right_click(Position(row, col))
                    
            except ValueError:
                print("ข้อผิดพลาด: กรุณากรอกแถวและคอลัมน์เป็นตัวเลข (0-9).")
                continue
        
        render(game)
        print("You Win!" if game.state.name == "WON" else "Boom! You Lose.")
        
        # ถามผู้เล่นว่าอยากเริ่มเกมใหม่หรือไม่
        if not restart_game(game):
            break

if __name__ == "__main__":
    main()
