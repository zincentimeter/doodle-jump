import utils
from utils import *
from game_interface import *
from agent_interface import *
import sys
import traceback

def main():
    # Initializing... : Get Q-Learning Agent
    init_globals()
    agent = DoodleJumpQLearningAgent(alpha=0.02, gamma=0.8, epsilon=0.05)
    # First RUN : Do when the game starts
    # gameState = retrieveGameState()
    while (True):
        gameState = getGameState()
        print("gameState type = %s\n payload = %s" % (str(type(gameState)), str(gameState)))
    exit()
    # Decision
    action = agent.decide(gameState)
    action_absolute = relativeToAbsolute(action[0], gameState['agent_pos'])
    # Write back to game
    writeBack(getFormated(gameState, action[0], action_absolute[1]))
    # Prepare for the other runs.
    lastState, lastAction, lastAction_absolute = gameState, action, action_absolute
    decisionList = []


    while (True):
        # try:
        # Retrieve new game state
        gameState = retrieveGameState()
        # Only decide when hit the board
        if gameState['agent_speed'] > 13.5:
            # Training
            reward = gameState['score'] - lastState['score']
            # agent.update_Q(lastState, lastAction, gameState, reward)
            agent.observe(lastState, lastAction, gameState, reward)
            # Decision
            action = agent.decide(gameState)
            action_absolute = relativeToAbsolute(action[0], gameState['agent_pos'])
            if action[0][0] < 0 or action[0][1] < 0:
                action = lastAction
                action_absolute = lastAction_absolute
            # for debug!
            # print("Q_matrix = %s" % str(agent.Q))
            decisionList.append(gameState['agent_speed'])
            # print
        else:
            action_absolute = lastAction_absolute
        # Write back to game
        writeBack(getFormated(gameState, action[0], action_absolute[1]))
        # Update last information
        lastState, lastAction, lastAction_absolute = gameState, action, action_absolute

        # just for displaying debug info
        os.system("cls")
        # except Exception as e:
        #     # if (not (isinstance(e, ValueError))) and (not (isinstance(e, KeyError))):
        #     exc_type, exc_value, exc_traceback_obj = sys.exc_info()
        #     input(str(exc_type))
        #     input(str(exc_value))
        #     traceback.print_tb(exc_traceback_obj)



if __name__ == "__main__":
    main()