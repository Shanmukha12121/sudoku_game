import tkinter as tk
from tkinter import messagebox
import random

def generate_sudoku():
    # Initialize empty 9x9 grid
    grid = [[0 for _ in range(9)] for _ in range(9)]
    
    # Fill the diagonal boxes
    for i in range(0, 9, 3):
        nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        random.shuffle(nums)
        for j in range(3):
            for k in range(3):
                grid[i+j][i+k] = nums.pop()
    
    # Backtrack to fill remaining cells
    solve(grid)
    
    # Randomly remove numbers to create puzzle
    remove_count = 45  # Adjust difficulty by changing this count
    while remove_count > 0:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if grid[row][col] != 0:
            grid[row][col] = 0
            remove_count -= 1
            
    return grid

def solve(grid):
    find = find_empty(grid)
    if not find:
        return True
    else:
        row, col = find

    for num in range(1, 10):
        if is_valid(grid, num, (row, col)):
            grid[row][col] = num

            if solve(grid):
                return True

            grid[row][col] = 0

    return False

def is_valid(grid, num, pos):
    # Check row
    for i in range(len(grid[0])):
        if grid[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(grid)):
        if grid[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if grid[i][j] == num and (i,j) != pos:
                return False

    return True

def find_empty(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 0:
                return (i, j)
    return None

def on_click(row, col):
    def inner(event=None):
        if not entries[row][col].get().isdigit():
            messagebox.showerror("Invalid Input", "Please enter a number between 1 and 9.")
            return
        num = int(entries[row][col].get())
        if num < 1 or num > 9:
            messagebox.showerror("Invalid Input", "Please enter a number between 1 and 9.")
            return
        if is_valid_move(sudoku, row, col, num):
            entries[row][col].config(state='disabled', disabledforeground='black')
            entries[row][col].config(bg='#F0E68C')  # Light Khaki
            sudoku[row][col] = num
            if find_empty(sudoku) is None:
                messagebox.showinfo("Congratulations!", "You solved the Sudoku puzzle!")
        else:
            messagebox.showerror("Invalid Move", "This number cannot be placed here.")
    return inner

def is_valid_move(grid, row, col, num):
    # Check row
    if num in grid[row]:
        return False
    
    # Check column
    for i in range(9):
        if grid[i][col] == num:
            return False
    
    # Check box
    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if grid[i][j] == num:
                return False
    
    return True

def create_sudoku_gui():
    global entries
    global sudoku
    sudoku = generate_sudoku()
    
    root = tk.Tk()
    root.title("Sudoku")
    
    entries = [[None for _ in range(9)] for _ in range(9)]
    
    # Define custom colors and fonts
    background_color = "#F5F5F5"  # White Smoke
    entry_color = "#F0FFFF"       # Azure
    shade_color = "#D3D3D3"        # Light Grey
    font_style = ("Helvetica", 12)
    
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] == 0:
                entries[i][j] = tk.Entry(root, width=4, justify='center', font=font_style, bg=entry_color, highlightbackground=shade_color)
                entries[i][j].grid(row=i, column=j, padx=1, pady=1)
                entries[i][j].bind("<FocusIn>", lambda event, r=i, c=j: entries[r][c].delete(0, 'end'))
                entries[i][j].bind("<Return>", on_click(i, j))
            else:
                entries[i][j] = tk.Label(root, text=str(sudoku[i][j]), width=4, height=2, relief='sunken', font=font_style, bg=entry_color, highlightbackground=shade_color)
                entries[i][j].grid(row=i, column=j, padx=1, pady=1)
                
            # Add shade for every 3x3 grid
            if (i // 3 + j // 3) % 2 == 0:
                entries[i][j].config(bg=shade_color)
    
    root.mainloop()

# Example usage:
if __name__ == "__main__":
    create_sudoku_gui()
