import utils
from utils import *
from game_interface import *
from agent_interface import *
import sys
import traceback
from plot import Visualizer
from game_logic import DoodleJump
lastY = 0
def train():
    visualizer = Visualizer()

    game = DoodleJump()
    agent = DoodleJumpQLearningAgent(alpha=0.1, gamma=0.01, epsilon=0.9, eps_decay=0.9, eps_interval=400, eps_end=0.005)
    agent.Q = np.load("QQ/Q_1610105285.321793.npy")
    agent.visited = np.load("QQ/Visited_1610105285.3270879.npy")
    agent.save_counter = np.load("QQ/save_cunter_1610105285.3316953.npy")
    game.update((0, (X/2, -50)))
    game.run_once()
    gameState = getGameState(game)
    agent_pos = gameState['agent_pos']

    target_relative = agent.decide(gameState)
    target_absolute = relativeToAbsolute(target_relative[0], agent_pos)

    action = getAction(gameState, target_absolute)
    # update last info
    last_target_relative = target_relative
    last_gameState = gameState
    last_target_absolute = target_absolute
    last_action = action
    while (True):
        try:

            game.update(action)
            game.run_once()
            gameState = getGameState(game)
            agent_pos = gameState['agent_pos']
            is_died, is_hit = gameState['is_died'], gameState['is_hit']

            reward = (gameState['score'] - last_gameState['score'] - 10) if (not is_died) \
                else -1000

            if (is_died):
                if (gameState['relative_boards'] != []):
                    agent.observe(last_gameState, last_target_relative, gameState, reward)
                target_relative = last_target_relative
                target_absolute = last_target_absolute
                action = last_action
                visualizer.insert_data((game.score_for_display, game.death_time))
                print((game.score_for_display, game.death_time))
            # Make decision and update only when hit.
            elif (is_hit):
                # print("save counter %d", agent.save_counter)
                # print("visit counter %d", agent.visit_counter)
                # Training
                agent.observe(last_gameState, last_target_relative, gameState, reward)
                target_relative = agent.decide(gameState)
                target_absolute = relativeToAbsolute(target_relative[0], agent_pos)
                # Decision
                # input(target)
                # input(target_absolute)
                action = getAction(gameState, target_absolute)
                # input(action)
            else:
                action = last_action
                target_y_absolute = action[1][1]
                target_x_absolute = action[1][0]
                boards = gameState["raw_boards"]
                # print("%s %s" % (str(boards), str(target_y_absolute)))

                min_distance = 2*H
                for board in boards:
                    board_x_absolute = board[0][0]
                    board_y_absolute = board[0][1]
                    distance = manhattanDistance(board[0], action[1])
                    if distance < min_distance:
                        min_distance = distance
                        target_x_absolute = board_x_absolute
                        target_y_absolute = board_y_absolute
                # input("%s %s" % (str(target_x_absolute), str(target_y_absolute)))
                action = lrdecide(agent_pos[0], target_x_absolute, 5, target_y_absolute)
            # update last info
            last_gameState = gameState
            last_target_relative = target_relative
            last_target_absolute = target_absolute
            last_action = action
            # input(action)
            # os.system('cls')
        except KeyboardInterrupt:
            visualizer.plot_single()
            print("save counter %d", agent.save_counter)
            print("visit counter %d", agent.visit_counter)

            input()
            # exit()
        
if __name__ == "__main__":
    # main()
    train()