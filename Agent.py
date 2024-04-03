import random

class Agent:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.first_move = True

    def select_action(self, available_actions):
        return random.choice(available_actions)

    def update_strategy(self, state, action, reward, next_state, done):
        self.first_move = False

    def get_reward(self, game, result, action):
        if self.first_move:
            return 0
        elif result == 'won':
            return 1
        elif result == 'lost':
            return -1
        else:
            x, y = action
            if game.has_revealed_neighbors(x, y):
                return 0.5
            else:
                return -0.5
