from utils import *
from game_interface import *
from agent_interface import *


def main():
    # Initializing... : Get Q-Learning Agent
    init_globals()
    agent = DoodleJumpQLearningAgent(alpha=0.02, gamma=0.8, epsilon=0.05)

    # First RUN : Do when the game starts
    gameState = retrieveGameState()
    # Decision
    action = agent.decide(gameState)
    actionY_absolute = relativeToAbsolute(action[0], gameState['agent_pos'])[1]
    # Write back to game
    writeBack(getFormated(gameState, action[0], actionY_absolute))
    # Prepare for the other runs.
    lastState, lastAction, lastActionY_absolute = gameState, action, actionY_absolute
    decisionList = []
    while (True):
        # Retrieve new game state
        gameState = retrieveGameState()
        # Only decide when hit the board
        if gameState['agent_speed'] > 13.5:
            # Training
            reward = gameState['score'] - lastState['score']
            agent.observe(lastState, lastAction, gameState, reward)
            # Decision
            action = agent.decide(gameState)
            actionY_absolute = relativeToAbsolute(action[0], gameState['agent_pos'])[1]
            # for debug!
            decisionList.append(gameState['agent_speed'])
        else:
            actionY_absolute = lastActionY_absolute

        print(decisionList)
        print("actionY_absolute %s" % str(actionY_absolute))
        print("action %s" % str(action))
        # Write back to game
        writeBack(getFormated(gameState, action[0], actionY_absolute))
        # Update last information
        lastState, lastAction, lastActionY_absolute = gameState, action, actionY_absolute

        # just for displaying debug info
        os.system("cls")



if __name__ == "__main__":
    main()


# if __name__ == "__main__":
#     from destination import pusu
#     while (True):
#         print(retrieveGameState()['agent_speed'])
#         pusu(retrieveGameState())

#         # gameState = retrieveGameState()
#         # action = (48, 79)
#         # input(gameState['agent_pos'])
#         # writeBack(getFormated(gameState, action))
#         os.system("cls")
