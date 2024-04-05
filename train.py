from Agent import DeepQNAgent
from Game import Minesweeper
import numpy as np
import matplotlib.pyplot as plt
import os

def train(agent, game, episodes=10):
    rewards = []
    outcomes = []

    logs_dir = 'data/logs'
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    rewards_file_path = os.path.join(logs_dir, 'total_rewards.txt')
    outcomes_file_path = os.path.join(logs_dir, 'outcomes.txt')

    with open(rewards_file_path, 'w') as rewards_file, open(outcomes_file_path, 'w') as outcomes_file:
        for episode in range(episodes):
            game.reset()
            state = np.array(game.get_state()).flatten().reshape(1, agent.state_size)
            done = False
            total_reward = 0

            while not done:
                action = agent.choose_action(state)
                _, result = game.reveal_tile(*agent.game.id_to_action(action))
                next_state = np.array(game.get_state()).flatten().reshape(1, agent.state_size)
                reward = agent.get_reward(game, result, action)
                total_reward += reward
                agent.update_model(state, action, reward, next_state, done)
                state = next_state
                done = game.is_finished()

            rewards.append(total_reward)
            outcomes.append(1 if result == 'won' else 0)
            print(f"Episode {episode + 1}: Game {result}, Total Score: {total_reward}")

            rewards_file.write(f"Episode {episode + 1}: {total_reward}\n")
            outcomes_file.write(f"Episode {episode + 1}: {'1' if result == 'won' else '0'}\n")

    return rewards, outcomes

if __name__ == "__main__":
    width, height, num_mines = 10, 10, 30
    episodes = 10
    game = Minesweeper(width, height, num_mines)
    agent = DeepQNAgent(game=game, num_episodes=episodes, state_size=width*height, action_size=width*height, learning_rate=0.01)
    rewards, outcomes = train(agent, game, episodes)

    plt.figure(figsize=(10, 6))
    plt.plot(rewards, label='Total Reward per Episode')
    plt.xlabel('Episode')
    plt.ylabel('Total Reward')
    plt.title('Training Progress: Total Reward per Episode')
    plt.legend()
    plt.tight_layout()

    plots_dir = 'data/plots'
    if not os.path.exists(plots_dir):
        os.makedirs(plots_dir)

    plot_path = os.path.join(plots_dir, 'training_rewards.png')
    plt.savefig(plot_path)
    print(f"Plot saved to {plot_path}")