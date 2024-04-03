import random

class Minesweeper:
    def __init__(self, width, height, num_mines):
        self.width = width
        self.height = height
        self.num_mines = num_mines
        self.board = [[0 for _ in range(width)] for _ in range(height)]
        self.revealed = [[False for _ in range(width)] for _ in range(height)]
        self.game_state = 'playing'
        self.place_mines()
        self.mark_adjacent_mines()

    def place_mines(self):
        placed_mines = 0
        while placed_mines < self.num_mines:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if self.board[y][x] == 0:
                self.board[y][x] = -1
                placed_mines += 1

    def mark_adjacent_mines(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == -1:
                    continue
                mines = self.count_adjacent_mines(x, y)
                self.board[y][x] = mines

    def count_adjacent_mines(self, x, y):
        mines = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if self.board[ny][nx] == -1:
                        mines += 1
        return mines
    
    def reveal_tile(self, x, y):
        if self.game_state != 'playing':
            # print('Game not in "playing" state. Cannot make a move.')
            return

        if not (0 <= x < self.width and 0 <= y < self.height) or self.revealed[y][x]:
            return

        self.revealed[y][x] = True

        if self.board[y][x] == -1:
            self.game_state = 'lost'
            # print("Game lost. Revealing all the tiles.")
            self.reveal_all()
            return

        if self.board[y][x] == 0:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    nx, ny = x + dx, y + dy
                    self.reveal_tile(nx, ny)

        self.check_win()

    def reveal_all(self):
        for y in range(self.height):
            for x in range(self.width):
                self.revealed[y][x] = True

    def check_win(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] != -1 and not self.revealed[y][x]:
                    return
        self.game_state = 'won'

    def print_board(self, reveal_all=False):
        for y in range(self.height):
            for x in range(self.width):
                if reveal_all or self.revealed[y][x]:
                    if self.board[y][x] == -1:
                        print("*", end=" ")
                    else:
                        print(self.board[y][x], end=" ")
                else:
                    print(".", end=" ")
            print()