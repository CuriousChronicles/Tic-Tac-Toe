import tkinter as tk
import time
from tkinter import messagebox
from Functions import TicTacToe
from Player import HumanPlayer, RandomComputerPlayer, ComputerPlayer

class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        # self.geometry("500x500")
        self.resizable(False, False)
        
        self.container = tk.Frame(self)
        self.container.grid(sticky="nsew")

        # I've made some kind of change here
        self.frames = {}

        for F in (StartPage, HumanVHuman, HumanVComputer, ComputerVComputer):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        tk.Label(self, text="Welcome to Tic Tac Toe!").pack(pady=10)
        tk.Label(self, text="Please select a game mode:").pack(pady=10)

        gm1_button = tk.Button(self, text="Human VS Human", 
                               command=lambda: controller.show_frame(HumanVHuman))
        gm1_button.pack(pady=10)

        gm2_button = tk.Button(self, text="Human VS Computer", 
                               command=lambda: controller.show_frame(HumanVComputer))
        gm2_button.pack(pady=10)

        gm3_button = tk.Button(self, text="Computer VS Computer", 
                               command=lambda: controller.show_frame(ComputerVComputer))
        gm3_button.pack(pady=10)

        exit_button = tk.Button(self, text="Exit", command=controller.quit)
        exit_button.pack(pady=10)

class HumanVHuman(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.label = tk.Label(self, text="Human VS Human!")
        self.label.grid(row=0, column=0, columnspan=3, pady=10)

        # Create the board
        self.board_buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                button = tk.Button(self, text=" ", width = 20, height = 3, command=lambda i=i, j=j: self.make_move(i, j))
                button.grid(row=i, column=j)
                row.append(button)
            self.board_buttons.append(row)

        # Create a reset button
        tk.Button(self, text="Reset", command=self.reset).grid(row=3, column=0, columnspan=3)

        # Create a back button
        tk.Button(self, text="Back",
                  command=lambda: controller.show_frame(StartPage)).grid(row=4, column=0, columnspan=3)

        self.controller = controller
        self.game = TicTacToe()
        self.player1 = HumanPlayer('X')
        self.player2 = HumanPlayer('O')
        self.current_player = self.player1

    # Make a move
    def make_move(self, i, j):
        index = i * 3 + j
        if self.game.boardList[index] == '.':
            self.game.makeTurn(index, self.current_player.letter)
            self.board_buttons[i][j].config(text=self.current_player.letter)

            if self.game.checkWin(self.current_player.letter):
                tk.messagebox.showinfo("Game Over", f"{self.current_player.letter} wins!")
                self.controller.show_frame(StartPage)
                return
            elif self.game.checkDraw():
                tk.messagebox.showinfo("Game Over", "Draw!")
                self.controller.show_frame(StartPage)
                return

            # switch player
            self.current_player = self.player1 if self.current_player == self.player2 else self.player2

    def reset(self):
        self.game.resetBoard()

        for i in range(3):
            for j in range(3):
                self.board_buttons[i][j].config(text=" ")

        self.current_player = self.player1

class HumanVComputer(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.label = tk.Label(self, text="Human VS Human!")
        self.label.grid(row=0, column=0, columnspan=3, pady=10)

        # Create a toggle button which allows the user to choose who goes first
        self.toggle = tk.IntVar()
        self.toggle.set(1)
        tk.Checkbutton(self, text="Human First", variable=self.toggle).grid(row=0, column=3, columnspan=3)

        # Create the board
        self.board_buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                button = tk.Button(self, text=" ", width = 20, height = 3, command=lambda i=i, j=j: self.make_move(i, j))
                button.grid(row=i, column=j)
                row.append(button)
            self.board_buttons.append(row)

        # Create a reset button
        tk.Button(self, text="Reset", command=self.reset).grid(row=3, column=0, columnspan=3)

        # Create a back button
        tk.Button(self, text="Back",
                  command=lambda: controller.show_frame(StartPage)).grid(row=4, column=0, columnspan=3)

        self.controller = controller
        self.game = TicTacToe()
        self.player1 = HumanPlayer('X')
        self.player2 = ComputerPlayer('O')
        self.current_player = self.player1

    # Make a move
    def make_move(self, i, j):
        index = i * 3 + j
        if self.game.boardList[index] == '.':
            self.game.makeTurn(index, self.current_player.letter)
            self.board_buttons[i][j].config(text=self.current_player.letter)

            if self.game.checkWin(self.current_player.letter):
                tk.messagebox.showinfo("Game Over", f"{self.current_player.letter} wins!")
                self.controller.show_frame(StartPage)
                return
            elif self.game.checkDraw():
                tk.messagebox.showinfo("Game Over", "Draw!")
                self.controller.show_frame(StartPage)
                return

            # switch player
            self.current_player = self.player1 if self.current_player == self.player2 else self.player2

            # Computer's turn
            # Add a delay when computer makes a move
            if isinstance(self.current_player, ComputerPlayer):
                self.after(100, self.make_computer_move)

    def make_computer_move(self):
        index = self.current_player.getMove(self.game)
        self.game.makeTurn(index, self.current_player.letter)
        self.board_buttons[index // 3][index % 3].config(text=self.current_player.letter)
        time.sleep(1.0)

        if self.game.checkWin(self.current_player.letter):
            tk.messagebox.showinfo("Game Over", f"{self.current_player.letter} wins!")
            self.controller.show_frame(StartPage)
            return
        elif self.game.checkDraw():
            tk.messagebox.showinfo("Game Over", "Draw!")
            self.controller.show_frame(StartPage)
            return

        # switch player
        self.current_player = self.player1 if self.current_player == self.player2 else self.player2

    def reset(self):
        self.game.resetBoard()

        for i in range(3):
            for j in range(3):
                self.board_buttons[i][j].config(text=" ")

        self.current_player = self.player1

class ComputerVComputer(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.label = tk.Label(self, text="Computer VS Computer!")
        self.label.grid(row=0, column=0, columnspan=3, pady=10)

        # Create the board
        self.board_buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                button = tk.Button(self, text=" ", width = 20, height = 3)
                button.grid(row=i, column=j)
                row.append(button)
            self.board_buttons.append(row)

        # Create a start button
        start_button = tk.Button(self, text="Start", command=self.start_game)
        start_button.grid(row=3, column=0, columnspan=3)

        # Create a back button
        back_button = tk.Button(self, text="Back", command=lambda: controller.show_frame(StartPage))
        back_button.grid(row=4, column=0, columnspan=3)

        self.controller = controller
        self.game = TicTacToe()
        self.player1 = ComputerPlayer('X')
        self.player2 = ComputerPlayer('O')

        self.current_player = self.player1

    def start_game(self):
        self.play_next_move()

    def play_next_move(self):
        # get move from the current player
        index = self.current_player.getMove(self.game)
        self.game.makeTurn(index, self.current_player.letter)

        # update the board
        i, j = divmod(index, 3)
        self.board_buttons[i][j].config(text=self.current_player.letter)

        if self.game.checkWin(self.current_player.letter):
            tk.messagebox.showinfo("Game Over", f"{self.current_player.letter} wins!")
            self.controller.show_frame(StartPage)
            return
        elif self.game.checkDraw():
            tk.messagebox.showinfo("Game Over", "Draw!")
            self.controller.show_frame(StartPage)
            return

        # switch player
        self.current_player = self.player1 if self.current_player == self.player2 else self.player2

        # schedule the next move
        self.after(500, self.play_next_move)

if __name__ == "__main__":
    app = Application()
    app.title("Tic Tac Toe")
    app.mainloop()
