import tkinter as tk
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
        tk.Label(self, text="Human VS Human!").pack(pady=10)
        tk.Button(self, text="Back",
                  command=lambda: controller.show_frame(StartPage)).pack()

    

class HumanVComputer(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Label(self, text="Human VS Computer!").grid(pady=10)
        tk.Button(self, text="Back",
                  command=lambda: controller.show_frame(StartPage)).grid(pady=10)

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

    def start_game(self):
        pass

if __name__ == "__main__":
    app = Application()
    app.title("Tic Tac Toe")
    app.mainloop()
