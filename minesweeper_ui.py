import tkinter as tk
import tkinter.simpledialog as simpledialog
import tkinter.messagebox as messagebox
import random
import itertools
import sys
class GameDialog(tk.Toplevel):  #遊戲的功能介面，包含重新開始遊戲、重新設置遊戲及退出遊戲
    def __init__(self, parent, title, message):
        super().__init__(parent)
        self.title(title)
        self.geometry("200x120")
        tk.Label(self, text=message).pack(pady=10)
        tk.Button(self, text="重新開始", command=self.restart_game).pack()
        tk.Button(self, text="重新設置遊戲", command=self.reset_game).pack()
        tk.Button(self, text="退出", command=self.quit_game).pack()

    def reset_game(self):   #重新設置遊戲
        self.destroy()
        self.master.destroy()
        game_config_dialog = GameConfigDialog(None)
        if game_config_dialog.result is None:
            print("必須輸入遊戲設定！")
        else:
            width, height, mines = game_config_dialog.result
            game = Minesweeper(width, height, mines)
            game.mainloop()

    def restart_game(self): #重新開始遊戲
        self.master.restart()
        self.destroy()
    
    def quit_game(self):    #退出遊戲
        self.destroy()
        self.master.destroy()
        sys.exit()
        
class GameWinDialog(GameDialog):    #遊戲勝利
    def __init__(self, parent):
        super().__init__(parent, '遊戲勝利', "恭喜你，贏得了遊戲！")
class GameOverDialog(GameDialog):   #踩到地雷，遊戲結束
    def __init__(self, parent):
        super().__init__(parent, '遊戲結束', "你踩到地雷了！")
        
class GameConfigDialog(simpledialog.Dialog):    #設定踩地雷的寬度、高度及地雷數量
    def body(self, master):
        self.width_var = tk.StringVar()
        self.height_var = tk.StringVar()
        self.mines_var = tk.StringVar()

        tk.Label(master, text="寬度:").grid(row=0, sticky="w")
        tk.Label(master, text="高度:").grid(row=1, sticky="w")
        tk.Label(master, text="地雷數量:").grid(row=2, sticky="w")

        tk.Entry(master, textvariable=self.width_var).grid(row=0, column=1)
        tk.Entry(master, textvariable=self.height_var).grid(row=1, column=1)
        tk.Entry(master, textvariable=self.mines_var).grid(row=2, column=1)

        return tk.Entry(master, textvariable=self.width_var)

    def validate(self): #檢查使用者輸入的遊戲條件是否符合遊戲規則
        try:
            width = int(self.width_var.get())
            height = int(self.height_var.get())
            mines = int(self.mines_var.get())
            return width > 0 and height > 0 and mines > 0 and mines <= width * height
        except ValueError:
            return False

    def apply(self):
        width = int(self.width_var.get())
        height = int(self.height_var.get())
        mines = int(self.mines_var.get())
        self.result = (width, height, mines)

class Minesweeper(tk.Tk):   #踩地雷主程式
    def __init__(self, width, height, num_mines):
        super().__init__()
        self.title('Minesweeper')
        self.width = width
        self.height = height
        self.num_mines = num_mines
        self.board, self.mines = self.create_board()
        self.buttons = [[tk.Button(self, text=' ', width=3, height=1, command=lambda x=x, y=y: self.reveal(x, y)) for x in range(width)] for y in range(height)]
        self.mine_marks = set()
        for y, row in enumerate(self.buttons):
            for x, button in enumerate(row):
                button.grid(row=y, column=x)
                button.bind('<Button-3>', lambda e, x=x, y=y: self.mark_mine(x, y))

    def create_board(self):
        board = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        mines = set()

        while len(mines) < self.num_mines:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            mines.add((x, y))

        for x, y in mines:
            board[y][x] = 'M'

        return board, mines

    def reveal(self, x, y):
        if self.board[y][x] == 'M':
            self.buttons[y][x].config(text='*', bg='red', fg='white')
            self.game_over()
        else:
            visited = set()
            self.reveal_helper(x, y, visited)
            self.check_win()
    def reveal_mines(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == 'M':
                    self.buttons[y][x].config(text='*', bg='red', fg='white')
    def reveal_helper(self, x, y, visited):
        if (x, y) in visited:
            return

        visited.add((x, y))

        count = 0
        for dx, dy in itertools.product(range(-1, 2), range(-1, 2)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height and self.board[ny][nx] == 'M':
                count += 1

        if count > 0:
            self.board[y][x] = str(count)
            self.buttons[y][x].config(text=count, bg='lightblue', state='disabled')
        else:
            self.board[y][x] = '.'
            self.buttons[y][x].config(text='', bg='lightblue', state='disabled')
            for dx, dy in itertools.product(range(-1, 2), range(-1, 2)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    self.reveal_helper(nx, ny, visited)

    def mark_mine(self, x, y):
        if (x, y) in self.mine_marks:
            self.buttons[y][x].config(text=' ', fg='black')
            self.mine_marks.remove((x, y))
        else:
            self.buttons[y][x].config(text='⚑', fg='red')
            self.mine_marks.add((x, y))

    def check_win(self):
        cells_revealed = 0
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] != ' ' and self.board[y][x] != 'M':
                    cells_revealed += 1

        if cells_revealed == self.width * self.height - self.num_mines:
            GameWinDialog(self)
            self.disable_buttons()

    def disable_buttons(self):
        for y in range(self.height):
            for x in range(self.width):
                self.buttons[y][x].config(state='disabled')

    def restart(self):
        for y, row in enumerate(self.buttons):
            for x, button in enumerate(row):
                button.destroy()

        self.board, self.mines = self.create_board()
        self.buttons = [[tk.Button(self, text=' ', width=3, height=1, command=lambda x=x, y=y: self.reveal(x, y)) for x in range(self.width)] for y in range(self.height)]
        self.mine_marks = set()
        for y, row in enumerate(self.buttons):
            for x, button in enumerate(row):
                button.grid(row=y, column=x)
                button.bind('<Button-3>', lambda e, x=x, y=y: self.mark_mine(x, y))

    def game_over(self):
        GameOverDialog(self)
        self.reveal_mines()
        self.disable_buttons()
        

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()  # 隱藏 root window
    game_config_dialog = GameConfigDialog(None)
    if game_config_dialog.result is None:
        print("必須輸入遊戲設定！")
    else:
        width, height, mines = game_config_dialog.result
        game = Minesweeper(width, height, mines)
        game.mainloop()
