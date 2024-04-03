import random

class Agent:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def select_action(self, available_actions):
        return random.choice(available_actions)

    def update_strategy(self, state, action, reward, next_state, done):
        pass

    def get_reward(self, result):
        if result == 'won':
            return 100
        elif result == 'lost':
            return -100
        elif result == 'continue':
            return 1
        else:
            return -10