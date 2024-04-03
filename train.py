from Agent import Agent
from Game import Minesweeper

def train(agent, game, episodes=1000):
    for episode in range(episodes):
        game.reset()
        state = game.get_state()
        done = False
        total_reward = 0

        while not done:
            available_actions = game.get_available_actions()
            action_ids = [game.action_to_id(*action) for action in available_actions]
            selected_action_id = agent.select_action(action_ids)
            selected_action = game.id_to_action(selected_action_id)
            
            next_state, result = game.reveal_tile(*selected_action)
            reward = get_reward(result)
            total_reward += reward
            done = game.is_finished()
            
            agent.update_strategy(state, selected_action_id, reward, next_state, done)
            state = next_state

        print(f"Episode {episode + 1}: Game {result}, Total Score: {total_reward}")

                
def get_reward(result):
    """
    Define the reward function based on the result of an action.
    """
    if result == 'won':
        return 100
    elif result == 'lost':
        return -100
    elif result == 'continue':
        return 1
    else:
        return -10

if __name__ == "__main__":
    width, height, num_mines = 10, 10, 30
    episodes = 100
    
    game = Minesweeper(width, height, num_mines)
    agent = Agent(width, height)
    
    train(agent, game, episodes)
