import tkinter as tk
from tkinter import font

# Global variables
current_player = "X"
board = [""] * 9
buttons = []
game_over = False
score = {"X": 0, "O": 0, "Draws": 0}

WIN_COMBOS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6)
]

root = tk.Tk()
root.title("Tic Tac Toe")
root.configure(bg="#2b2b2b")
root.resizable(False, False)

cell_font = font.Font(family="Helvetica", size=32, weight="bold")
label_font = font.Font(family="Helvetica", size=14, weight="bold")
status_font = font.Font(family="Helvetica", size=16, weight="bold")

DEFAULT_BTN_BG = "#3c3f41"
WIN_BG = "#4caf50"

status_var = tk.StringVar(value="Player X's turn")
status_label = tk.Label(root, textvariable=status_var, font=status_font,
                         bg="#2b2b2b", fg="#f5f5f5", pady=10)
status_label.grid(row=0, column=0, columnspan=3)

board_frame = tk.Frame(root, bg="#2b2b2b")
board_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

score_frame = tk.Frame(root, bg="#2b2b2b")
score_frame.grid(row=2, column=0, columnspan=3, pady=(10, 5))

score_var = tk.StringVar()
score_label = tk.Label(score_frame, textvariable=score_var, font=label_font,
                        bg="#2b2b2b", fg="#f5f5f5")
score_label.pack()

control_frame = tk.Frame(root, bg="#2b2b2b")
control_frame.grid(row=3, column=0, columnspan=3, pady=(5, 15))

def on_click(index):
    global current_player, game_over

    if game_over:
        return
    if board[index] != "":
        return

    board[index] = current_player
    buttons[index].config(text=current_player, fg="#61dafb" if current_player == "X" else "#ff8a65")

    winning_combo = check_winner()
    if winning_combo:
        game_over = True
        highlight_winner(winning_combo)
        status_var.set(f"Player {current_player} wins!")
        score[current_player] += 1
        update_scoreboard()
    elif "" not in board:
        game_over = True
        status_var.set("It's a draw!")
        score["Draws"] += 1
        update_scoreboard()
    else:
        current_player = "O" if current_player == "X" else "X"
        status_var.set(f"Player {current_player}'s turn")


def check_winner():
    for combo in WIN_COMBOS:
        a, b, c = combo
        if board[a] != "" and board[a] == board[b] == board[c]:
            return combo
    return None


def highlight_winner(combo):
    for i in combo:
        buttons[i].config(bg=WIN_BG)


def restart_game():
    global board, current_player, game_over
    board = [""] * 9
    current_player = "X"
    game_over = False
    status_var.set("Player X's turn")
    for btn in buttons:
        btn.config(text="", bg=DEFAULT_BTN_BG)


def reset_score():
    global score
    score = {"X": 0, "O": 0, "Draws": 0}
    update_scoreboard()
    restart_game()


def update_scoreboard():
    score_var.set(f"X: {score['X']}    O: {score['O']}    Draws: {score['Draws']}")

for i in range(9):
    btn = tk.Button(
        board_frame, text="", font=cell_font, width=4, height=1,
        bg=DEFAULT_BTN_BG, fg="#f5f5f5", activebackground="#555555",
        relief="flat", command=lambda idx=i: on_click(idx)
    )
    btn.grid(row=i // 3, column=i % 3, padx=5, pady=5)
    buttons.append(btn)

update_scoreboard()

restart_btn = tk.Button(control_frame, text="Restart Game", font=label_font,
                         bg="#3c3f41", fg="#f5f5f5", activebackground="#555555",
                         relief="flat", padx=10, pady=5, command=restart_game)
restart_btn.grid(row=0, column=0, padx=8)

reset_btn = tk.Button(control_frame, text="Reset Score", font=label_font,
                       bg="#3c3f41", fg="#f5f5f5", activebackground="#555555",
                       relief="flat", padx=10, pady=5, command=reset_score)
reset_btn.grid(row=0, column=1, padx=8)

if __name__ == "__main__":
    root.mainloop()