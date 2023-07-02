import math
import random

class Player:
    def __init__(self, letter):
        self.letter = letter

    def getMove(self, game):
        pass

class RandomComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def getMove(self, game):
        # Get all the available moves
        availableMoves = game.availableMoves()
        return random.choice(availableMoves)

# Computer player that uses minimax algorithm
class ComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def getMove(self, game):
        # Get all the available moves
        availableMoves = game.availableMoves()
        if len(availableMoves) == 0:
            return None
        elif len(availableMoves) == 9:
            return random.choice(availableMoves)
        else:
            # We want to get the best move using the minimax algorithm
            bestMove = self.minimax(game, self.letter)['position']
        return bestMove

    def minimax(self, state, player):
        max_player = self.letter    #AI Player
        other_player = 'O' if player == 'X' else 'X'

        # First, we want to check if the previous move is a winning move
        if state.checkWin(other_player):
            # If it is, we want to return a score of -1
            return {'position': None, 'score': 1 * (state.emptySpaces() + 1) if other_player == max_player else -1 * (state.emptySpaces() + 1)}
        elif state.checkDraw():
            return {'position': None, 'score': 0}
        
        # Initialize best
        if player == max_player:
            best = {'position': None, 'score': -math.inf}
        else:
            best = {'position': None, 'score': math.inf}
        
        moves = state.availableMoves()
        for move in moves:
            # Try the move, then recurse using minimax to simulate the game
            # The base case is when the game is over either by a win or a draw
            state.makeTurn(move, player)
            sim_score = self.minimax(state, other_player)

            # Undo the move
            state.boardList[move] = '.'
            state.currentWinner = None
            sim_score['position'] = move

            # Update the best move
            if player == max_player:
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score
        return best


class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def getMove(self, game):
        while True:
            move = input(self.letter + '\'s turn. Input move (row col): ').split()
            # Check if input is valid
            if len(move) != 2:
                print('Invalid input. Try again.')
                continue
            elif not move[0].isdigit() or not move[1].isdigit():
                print('Invalid input. Try again.')
                continue
            else:
                move = int(move[0]) - 1, int(move[1]) - 1  # convert string input to int and 0-index
                index = move[0]*3 + move[1]

                # Check if move is valid
                if index < 0 or index > 8 or game.boardList[index] != '.':
                    print('Invalid move. Try again.')
                else:
                    return index