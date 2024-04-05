from Agent import DeepQNAgent
from Game import Minesweeper
import numpy as np

def train(agent, game, episodes=1000):
    for episode in range(episodes):
        game.reset()
        state = np.array(game.get_state()).flatten().reshape(1, agent.state_size)
        done = False
        total_reward = 0

        while not done:
            action = agent.choose_action(state)
            _, result = game.reveal_tile(*game.id_to_action(action))
            next_state = np.array(game.get_state()).flatten().reshape(1, agent.state_size)
            reward = agent.get_reward(game, result, action)
            total_reward += reward
            agent.update_model(state, action, reward, next_state, done)
            state = next_state
            done = game.is_finished()

        print(f"Episode {episode + 1}: Game {result}, Total Score: {total_reward}")

if __name__ == "__main__":
    width, height, num_mines = 10, 10, 30
    episodes = 100
    game = Minesweeper(width, height, num_mines)
    agent = SimplifiedDeepQNAgent(game=game, num_episodes=episodes, state_size=width*height, action_size=width*height, learning_rate=0.01)
    train(agent, game, episodes)
