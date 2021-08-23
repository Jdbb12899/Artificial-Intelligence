# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        
        ghostPosition = successorGameState.getGhostPositions() #keep track of next ghost position
        scoreFood = -1   #keep track of food score
        scoreGhost = -1  #keep track of ghost score
        
        for food in newFood.asList():
            scoreFood = 1/(util.manhattanDistance(newPos, food)) #find food

        for ghostProximity in ghostPosition:
             nearbyGhost = util.manhattanDistance(newPos, ghostProximity) #find ghost
             if nearbyGhost < 3: #if the ghost is nearby, getaway and find food
                 scoreGhost = -300 #escape ghost
                 scoreFood = 200 #find food
                 
        pacmanEval = successorGameState.getScore() + currentGameState.getScore() + scoreFood + scoreGhost #add up score
        
        return pacmanEval #return score

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        
        minimize = 0 #minimizer
        maximize = 0.0 #maximizer
        v = float("-inf") #initialize at -infinity
        direction = Directions.STOP #inititialize direction
        
        def minimaxagent(agent, depth, gameState):

            if gameState.isLose() or gameState.isWin() or depth == self.depth: #check if node is successful
                return self.evaluationFunction(gameState) 
            
            if agent == 0:  
                maximum = max(minimaxagent(1, depth, gameState.generateSuccessor(agent, actions)) for actions in gameState.getLegalActions(agent))
                return maximum #return max of minimax
                
            else:
                tmpAgent = (agent + 1)
                if gameState.getNumAgents() == tmpAgent: #track agent
                    tmpAgent = 0
                if tmpAgent == 0:
                    depth = depth + 1 #increment depth
                minimum = min(minimaxagent(tmpAgent, depth, gameState.generateSuccessor(agent, actions)) for actions in gameState.getLegalActions(agent))
                return minimum #return min of minimax
            
        for actions in gameState.getLegalActions(0): #check node action is legal move
            node = minimaxagent(1, 0, gameState.generateSuccessor(0, actions))
            if node > v: #set direction
                v = node
                direction = actions
                
        return direction
    
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        
        alpha = float("-inf") #initialize alpha as -infinity
        beta = float("inf") #initialize beta as +infinity
        
        def maxValue(gameState, depth, index, alpha, beta):
            v = float("-inf") #initialize v to -infinity internally
            depth = depth - 1 #decrement depth for ab check
          
            if gameState.isLose() or gameState.isWin() or depth < 0: #check if node is successful
                return (self.evaluationFunction(gameState), None)
            
            for actions in gameState.getLegalActions(index): #check legal moves
                nextState = gameState.generateSuccessor(index, actions) #set next state
                total = minValue(nextState, depth, index+1, alpha, beta)[0] #calc total for min
            
                if total > v:
                    v = total
                    maximum = actions #set max
              
                if v > beta:
                    return (v, maximum)
                alpha = max(alpha, v) #calc alpha
            
            maxVal = (v, maximum)  
            return maxVal

        def minValue(gameState, depth, index, alpha, beta):       
            v = float("inf") #initialize v to +infinity internally
            
            if gameState.isLose() or gameState.isWin() or depth < 0: #check if node is successful
                  return (self.evaluationFunction(gameState), None) 
            
            if index < (gameState.getNumAgents() - 1): #check alpha vs beta
                abCheck = minValue
                nextAgent = (index + 1)
            else:
                abCheck = maxValue
                nextAgent = 0
            
            for actions in gameState.getLegalActions(index): #check legal moves
                nextState = gameState.generateSuccessor(index, actions) #set next state
                total = abCheck(nextState, depth, nextAgent, alpha, beta)[0] #calc total for max
                
                if total < v:
                    v = total
                    minimum = actions #set min
                    
                if v < alpha:
                    return (v, minimum)
                beta = min(beta, v) #calc beta
                
            minVal = (v, minimum)
            return minVal
        
        alphabeta = maxValue(gameState, self.depth, 0, alpha, beta)[1]
        return alphabeta
        
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        Max = float("-inf") #initialize maximum for expectimax
        directions = Directions.STOP #initialize directions as STOP by default
        
        def Expectimax(agent, depth, gameState):
            if gameState.isLose() or gameState.isWin() or depth == self.depth: #check if node is successful
                return self.evaluationFunction(gameState)
            
            if agent == 0: #return maximize from legal moves
                maximum = max(Expectimax(1, depth, gameState.generateSuccessor(agent, actions)) for actions in gameState.getLegalActions(agent))
                return maximum
            else: #increment to successor agent
                successorAgent = agent + 1 #increment
                
                if gameState.getNumAgents() == successorAgent: #reset successor agent to 0
                    successorAgent = 0
                    
                if successorAgent == 0: #increment depth for search
                    depth = depth + 1
                # calculate sum of expectimax assuming legal moves
                Sum = sum(Expectimax(successorAgent, depth, gameState.generateSuccessor(agent, actions)) for actions in gameState.getLegalActions(agent))
                return Sum

        for actions in gameState.getLegalActions(0): #ensure move is legal
            agentState = gameState.generateSuccessor(0, actions)
            v = Expectimax(1, 0, agentState) #expectimax check root
            
            if v > Max: #check max and set direction
                Max = v
                directions = actions

        return directions
        
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    
    Similar to what was done in the first evaulation function, a food score and a ghost score are created.
    This time around, a score for capsules is created so that when capsules are collected, pacman will attack
    more frequently
    
    """
    
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    ghostPosition = currentGameState.getGhostPositions() #keep track of next ghost position
    scoreFood = -1   #keep track of food score
    scoreGhost = -1  #keep track of ghost score   
    powerUpPos = currentGameState.getCapsules() # keep track of powerups
    scorePowerUp = 0
    
    for powerUps in powerUpPos: #find power ups
        scorePowerUp = util.manhattanDistance(newPos, powerUps) #distance to power ups
        if powerUpPos == 0: #when found, attack ghosts
            scoreGhost = 1
            scoreFood = -1

    for food in newFood.asList():
            scoreFood = util.manhattanDistance(newPos, food) #find food

    for ghostProximity in ghostPosition:
            nearbyGhost = util.manhattanDistance(newPos, ghostProximity) #find ghost
            if nearbyGhost < 3: #if the ghost is nearby, getaway and find food
                scoreGhost = -3 #escape ghost
                scoreFood = 2 #find food
                
    pacmanEval = currentGameState.getScore() + currentGameState.getScore() + scoreFood + scoreGhost + scorePowerUp #add up score
        
    return pacmanEval #return score

    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
