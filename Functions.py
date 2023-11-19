import time
from Player import HumanPlayer, RandomComputerPlayer, ComputerPlayer

class TicTacToe:
    def __init__(self):
        # Initialising the board
        self.boardList = ['.', '.', '.', '.', '.', '.', '.', '.', '.']
        self.currentWinner = None

    # This function was used to print the game in text-based
    def printBoard(self):
        for row in range(3):
            for col in range(3):
                index = 3*row + col
                print('| ' + self.boardList[index], end=' ')
            print('|')
        print()

    # Uses the board to determine the current turn number
    def getCurrentTurnNumber(self):
        # Count the number of '.', number of turns would be 10-(this num)
        emptySpaces = 0
        for i in range(9):
            if self.boardList[i] == '.':
                emptySpaces = emptySpaces + 1
        return 10 - emptySpaces

    # Uses the board to find the current player
    # X is player 1
    # O is player 2
    def getCurrentPlayer(self):
        turnNumber = self.getCurrentTurnNumber()
        if turnNumber % 2 == 0:
            return 'X'
        else:
            return 'O'
    
    def availableMoves(self):
        # try doing with regular expression!
        moves = []
        for (i, spot) in enumerate(self.boardList):
            if spot == '.':
                moves.append(i)
        return moves

    def emptySpaces(self):
        return self.boardList.count('.')

    # Attempts to play a turn 
    def makeTurn(self, index, player):
        # If invalid turn, board should remain the same
        if index < 0 or index > 8 or self.boardList[index] != '.':
            return False
        else:
            self.boardList[index] = player
            return True

    # Check for game draw
    def checkDraw(self):
        # Check if there are no more terns left
        if self.getCurrentTurnNumber() == 10:
            return True
        return False
        
    # Check for game win
    def checkWin(self, player):
        winningCombinations = [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [2,4,6]]
        for win in winningCombinations:
            if self.boardList[win[0]] == self.boardList[win[1]] == self.boardList[win[2]] == player:
                return True
        return False

    def play(self, x_player, o_player, print_game):
        if print_game:
            self.printBoard()

        currentPlayer = self.getCurrentPlayer()
        winner = None
        # We want to iterate while the board still has empty squares
        # We will break out of the loop when there is a winner
        while self.emptySpaces() > 0:
            if currentPlayer == 'X':
                index = x_player.getMove(self)
            else:
                index = o_player.getMove(self)
            
            # Try to make the move and check if it is valid
            isValid = self.makeTurn(index, currentPlayer)
            if not isValid:
                print('Invalid move. Try again.')
                continue

            # Print the board if the game is being played
            if print_game:
                self.printBoard()

            # Check for win before changing the player
            if self.checkWin(currentPlayer):
                winner = currentPlayer
                break
            
            # Change the player
            currentPlayer = self.getCurrentPlayer()

            # Add a delay so computer doesn't generate moves too quickly
            time.sleep(0.8)

        self.printBoard()
        if winner == None:
            print('Draw')
        else:
            print(F"{winner} wins the game")    

    def resetBoard(self):
        self.boardList = ['.', '.', '.', '.', '.', '.', '.', '.', '.']
        self.currentWinner = None