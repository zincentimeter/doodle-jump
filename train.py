import utils
from utils import *
from game_interface import *
from agent_interface import *
import sys
import traceback

def main():
    # Initializing... : Get Q-Learning Agent
    init_globals()
    agent = DoodleJumpQLearningAgent(alpha=0.1, gamma=0., epsilon=0.1)
    
    # First RUN : Do when the game starts
    gameState = getGameState()
    # Decision
    action = agent.decide(gameState)
    action_absolute = relativeToAbsolute(action[0], gameState['agent_pos'])
    message = getFormated(gameState, action_absolute[1], "agent._get_q_dict_str_debug(gameState)")
    # Write back to game
    writeBack(message)
    # Prepare for the other runs.
    lastState, lastAction, lastAction_absolute = gameState, action, action_absolute
    max_score = 0
    max_speed = 0
    while (True):
        # try:
        max_score = max(max_score, gameState['score'])
        max_speed = max(max_speed, gameState['agent_speed'])
        print("update counter = %s" % str(agent.save_counter))
        print("max score = %s" % max_score)
        print("max speed = %s" % max_speed)

        # Retrieve new game state
        gameState = getGameState()
        is_died, is_hit = gameState['is_died'], gameState['is_hit']
        reward = (gameState['score'] - lastState['score'] - 10) if (not is_died) \
            else -1000

        if (is_died):
            print(gameState)
            if (gameState['relative_boards'] != []):
                agent.observe(lastState, lastAction, gameState, reward)
            action = lastAction
            action_absolute = lastAction_absolute            
            message = "0" # Writeback omittable output
        # Make decision and update only when hit.
        elif (is_hit):
            # Training
            agent.observe(lastState, lastAction, gameState, reward)
            # Decision
            action = agent.decide(gameState)
            action_absolute = relativeToAbsolute(action[0], gameState['agent_pos'])
            message = getFormated(gameState, action_absolute[1], "", debug=False)
        else:
            action = lastAction
            action_absolute = lastAction_absolute
            message = getFormated(gameState, action_absolute[1], "", debug=False)

        
        # Write back to game
        writeBack(message)
        # Update last information
        lastState, lastAction, lastAction_absolute = gameState, action, action_absolute

        # just for displaying debug info
        if (is_hit):
            print("is hit!")
        else:
            # print("not hit!")
            pass
        os.system("cls")

if __name__ == "__main__":
    main()