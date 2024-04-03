import random

class Minesweeper:
    def __init__(self, width, height, num_mines):
        self.width = width
        self.height = height
        self.num_mines = num_mines
        self.board = [[0 for _ in range(width)] for _ in range(height)]
        self.revealed = [[False for _ in range(width)] for _ in range(height)]
        self.game_state = 'playing'
        self.reset()

    def reset(self):
        self.board = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.revealed = [[False for _ in range(self.width)] for _ in range(self.height)]
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
                self.board[y][x] = self.count_adjacent_mines(x, y)

    def count_adjacent_mines(self, x, y):
        mines = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height and self.board[ny][nx] == -1:
                    mines += 1
        return mines

    def reveal_tile(self, x, y):
        if self.game_state != 'playing' or not (0 <= x < self.width and 0 <= y < self.height) or self.revealed[y][x]:
            return None, 'invalid'
        
        self.revealed[y][x] = True

        if self.board[y][x] == -1:
            self.game_state = 'lost'
            self.reveal_all()
            return self.get_state(), 'lost'

        if self.board[y][x] == 0:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    self.reveal_tile(x + dx, y + dy)

        self.check_win()
        return self.get_state(), 'won' if self.game_state == 'won' else 'continue'

    def reveal_all(self):
        for y in range(self.height):
            for x in range(self.width):
                self.revealed[y][x] = True

    def check_win(self):
        if all(self.revealed[y][x] or self.board[y][x] == -1 for x in range(self.width) for y in range(self.height)):
            self.game_state = 'won'

    def get_state(self):
        state = [[-1 if not self.revealed[y][x] else (self.board[y][x] if self.board[y][x] != -1 else -2) 
                for x in range(self.width)] for y in range(self.height)]
        return state

    def print_board(self, reveal_all=False):
        for y in range(self.height):
            for x in range(self.width):
                if reveal_all or self.revealed[y][x]:
                    print('*' if self.board[y][x] == -1 else self.board[y][x], end=' ')
                else:
                    print('.', end=' ')
            print()

    def get_available_actions(self):
        return [(x, y) for x in range(self.width) for y in range(self.height) if not self.revealed[y][x]]

    def action_to_id(self, x, y):
        return y * self.width + x

    def id_to_action(self, action_id):
        return action_id % self.width, action_id // self.width

    def is_finished(self):
        return self.game_state != 'playing'
