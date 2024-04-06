import numpy as np
import random
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

class DeepQNAgent:
    def __init__(self, game, num_episodes, state_size, action_size, gamma=0.95, epsilon=1.0, epsilon_min=0.01, 
                 epsilon_reduction=0.995, learning_rate=0.01):
        self.game = game
        self.num_episodes = num_episodes
        self.state_size = state_size
        self.action_size = action_size
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_reduction = epsilon_reduction
        self.learning_rate = learning_rate
        
        self.model = self._build_model()

    def _build_model(self):
        model = Sequential()
        model.add(Dense(512, input_dim=self.state_size, activation='relu'))
        model.add(Dense(256, activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(learning_rate=self.learning_rate))
        return model

    def choose_action(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])

    def update_model(self, state, action, reward, next_state, done):
        target = reward
        if not done:
            target += self.gamma * np.amax(self.model.predict(next_state)[0])
        target_f = self.model.predict(state)
        target_f[0][action] = target
        self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_reduction

    def get_reward(self, game, result, action, is_direct_action):
        if not is_direct_action:
            return 0
        if game.first_move:
            game.first_move = False
            return 0
        elif result == 'lost':
            return -1
        elif result == 'won':
            return 1
        else:
            x, y = game.id_to_action(action)
            if game.has_revealed_neighbors(x, y):
                return 0.5
            else:
                return -0.5
