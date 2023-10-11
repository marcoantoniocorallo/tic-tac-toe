from itertools import cycle
from typing import NamedTuple

class Player(NamedTuple):
    label: str
    color: str


class Move(NamedTuple):
    row: int
    col: int
    label: str = ""


BOARD_SIZE = 3
DEFAULT_PLAYERS = (
    Player(label="X", color="blue"),
    Player(label="O", color="red"),
)


class Game:
    def __init__(self, players=DEFAULT_PLAYERS, board_size=BOARD_SIZE):
        self._players = cycle(players)
        self.board_size = board_size
        self.current_player = next(self._players)
        self.winner_combo = []
        self._current_moves = []
        self._has_winner = False
        self._winning_combos = []
        self._setup_board()

    def _setup_board(self):
        self._current_moves = [
            [Move(row, col) for col in range(self.board_size)]
            for row in range(self.board_size)
        ]
        self._winning_combos = self._get_winning_combos()

    def _get_winning_combos(self):
        """Return all possible winning combinations, i.e. rows, columns and diagonals."""
        rows = [
            [(move.row, move.col) for move in row]
            for row in self._current_moves
        ]
        columns = [list(col) for col in zip(*rows)]
        first_diagonal = [row[i] for i, row in enumerate(rows)]
        second_diagonal = [col[j] for j, col in enumerate(reversed(columns))]
        return rows + columns + [first_diagonal, second_diagonal]

    def is_valid_move(self, move):
        """Return True if move is valid, and False otherwise."""
        row, col = move.row, move.col
        no_winner = not self._has_winner
        move_not_played = self._current_moves[row][col].label == ""

        return no_winner and move_not_played

    def process_move(self, move):
        """Process the current move and check if it's a win."""
        row, col = move.row, move.col
        self._current_moves[row][col] = move

        win_X = [ 
          combo for combo in self._winning_combos 
          if all( self._current_moves[combo[i][0]][combo[i][1]].label == 'X' for i in range(BOARD_SIZE) )
        ]
        win_O = [ 
          combo for combo in self._winning_combos 
          if all( self._current_moves[combo[i][0]][combo[i][1]].label == 'O' for i in range(BOARD_SIZE) )
        ]

        if win_X:
            self._has_winner = True
            self.winner_combo = win_X[0]
        elif win_O:
            self._has_winner = True
            self.winner_combo = win_O[0]

    def has_winner(self):
        """Return True if the game has a winner, and False otherwise."""
        return self._has_winner

    def is_tied(self):
        """Return True if the game is tied, and False otherwise."""
        return not self._has_winner and all( all(move.label != "" for move in row) for row in self._current_moves )

    def toggle_player(self):
        """Return a toggled player."""
        self.current_player = next(self._players)
       
    def reset_game(self):
        """Reset the game state to play again."""
        for row, row_content in enumerate(self._current_moves):
            for col, _ in enumerate(row_content):
                row_content[col] = Move(row, col)
        self._has_winner = False
        self.winner_combo = []