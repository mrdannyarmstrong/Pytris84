import tkinter as tk
import random

# Game settings
ROWS = 20
COLS = 10
EMPTY = " ."   # Empty space represented by a dot
BLOCK = "[]"   # Filled block representation
SPEED = 500    # Falling speed in milliseconds

# Tetromino shapes
SHAPES = {
    'I': [(-1, 0), (0, 0), (1, 0), (2, 0)],
    'O': [(0, 0), (1, 0), (0, 1), (1, 1)],
    'T': [(-1, 0), (0, 0), (1, 0), (0, 1)],
    'S': [(0, 0), (1, 0), (-1, 1), (0, 1)],
    'Z': [(-1, 0), (0, 0), (0, 1), (1, 1)],
    'J': [(-1, 0), (0, 0), (1, 0), (1, 1)],
    'L': [(-1, 0), (0, 0), (1, 0), (-1, 1)]
}

class Piece:
    def __init__(self, shape):
        self.shape = shape
        self.blocks = SHAPES[shape][:]
        self.x = COLS // 2
        self.y = 0

    def get_positions(self):
        return [(self.x + dx, self.y + dy) for dx, dy in self.blocks]

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def rotate(self):
        if self.shape == 'O':
            return  # O doesn’t rotate
        self.blocks = [(-dy, dx) for dx, dy in self.blocks]

def create_board():
    return [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]

def collision(piece, board):
    for x, y in piece.get_positions():
        if x < 0 or x >= COLS or y >= ROWS or (y >= 0 and board[y][x] == BLOCK):
            return True
    return False

def place_piece(piece, board):
    for x, y in piece.get_positions():
        if 0 <= y < ROWS:
            board[y][x] = BLOCK

def clear_lines(board):
    global score, lines_cleared, level, SPEED
    new_board = [row for row in board if any(cell == EMPTY for cell in row)]
    lines_cleared_in_this_move = ROWS - len(new_board)

    if lines_cleared_in_this_move > 0:
        score += lines_cleared_in_this_move * 100
        lines_cleared += lines_cleared_in_this_move
        level = lines_cleared // 10 + 1
        SPEED = max(100, 500 - (level - 1) * 50)

    for _ in range(lines_cleared_in_this_move):
        new_board.insert(0, [EMPTY for _ in range(COLS)])
    return new_board

def draw_board(board, current_piece):
    temp_board = [row[:] for row in board]
    for x, y in current_piece.get_positions():
        if 0 <= y < ROWS and 0 <= x < COLS:
            temp_board[y][x] = BLOCK

    # Adding borders with consistent spacing
    display = "\n".join(f"<! {''.join(row)} !>" for row in temp_board)
    board_label.config(text=display)

    score_label.config(text=f"Score: {score}")
    level_label.config(text=f"Level: {level}")
    lines_label.config(text=f"Lines: {lines_cleared}")

def game_loop():
    global current_piece, board, running
    if not running:
        return

    current_piece.move(0, 1)
    if collision(current_piece, board):
        current_piece.move(0, -1)
        place_piece(current_piece, board)
        board[:] = clear_lines(board)
        current_piece = Piece(random.choice(list(SHAPES.keys())))
        if collision(current_piece, board):
            board_label.config(text="GAME OVER\nPress R to Restart")
            running = False
            return

    draw_board(board, current_piece)
    root.after(SPEED, game_loop)

def key_press(event):
    global current_piece, board, running
    if not running:
        if event.keysym.lower() == 'r':
            restart_game()
        return

    if event.keysym == 'Left':
        current_piece.move(-1, 0)
        if collision(current_piece, board):
            current_piece.move(1, 0)
    elif event.keysym == 'Right':
        current_piece.move(1, 0)
        if collision(current_piece, board):
            current_piece.move(-1, 0)
    elif event.keysym == 'Down':
        current_piece.move(0, 1)
        if collision(current_piece, board):
            current_piece.move(0, -1)
    elif event.keysym == 'Up':
        old_blocks = current_piece.blocks[:]
        current_piece.rotate()
        if collision(current_piece, board):
            current_piece.blocks = old_blocks

    draw_board(board, current_piece)

def restart_game():
    global board, current_piece, running, score, level, lines_cleared, SPEED
    board = create_board()
    current_piece = Piece(random.choice(list(SHAPES.keys())))
    running = True
    score = 0
    level = 1
    lines_cleared = 0
    SPEED = 500
    draw_board(board, current_piece)
    game_loop()

# ---- Tkinter UI ----
root = tk.Tk()
root.title("Pytris 84")
root.geometry("580x320")  # Increased width to accommodate controls
root.resizable(False, False)

# Layout Frames
main_frame = tk.Frame(root)
main_frame.pack(expand=True, fill="both")

left_frame = tk.Frame(main_frame)
left_frame.pack(side="left", padx=5, pady=5)

center_frame = tk.Frame(main_frame)
center_frame.pack(expand=True, fill="both", side="left")

# Info Labels
score_label = tk.Label(left_frame, text="Score: 0", font=("Courier", 10), anchor="w")
level_label = tk.Label(left_frame, text="Level: 1", font=("Courier", 10), anchor="w")
lines_label = tk.Label(left_frame, text="Lines: 0", font=("Courier", 10), anchor="w")

score_label.pack(anchor="w")
level_label.pack(anchor="w")
lines_label.pack(anchor="w")

# Tetris Board (Board Label)
board_label = tk.Label(center_frame, font=("Courier", 10), justify="left", anchor="n")
board_label.grid(row=0, column=0, padx=10, pady=5)  # Game Board in the left part of the frame

control_instructions = """
Left Arrow: Move Left \n 
Right Arrow: Move Right \n
Up Arrow: Rotate the piece \n
Down Arrow: Speed up the piece \n
R: Restart the game"""
control_label = tk.Label(center_frame, text=control_instructions, font=("Courier", 10), justify="left")
control_label.grid(row=0, column=1, padx=10, pady=20)  # Instructions next to the game board

root.bind("<Key>", key_press)

# ---- Game Initialization ----
board = create_board()
current_piece = Piece(random.choice(list(SHAPES.keys())))
running = True

score = 0
level = 1
lines_cleared = 0

draw_board(board, current_piece)
game_loop()

root.mainloop()
