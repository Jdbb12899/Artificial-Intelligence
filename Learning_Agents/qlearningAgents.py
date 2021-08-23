# qlearningAgents.py
# ------------------
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


from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)

        "*** YOUR CODE HERE ***"
        
        self.values = util.Counter() # counter values

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"
        
        return self.values[(state, action)] # return states, actions
        
        #util.raiseNotDefined()

    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
        
        legalAction = self.getLegalActions(state) # initialize legal actions
        legalActionLen = len(legalAction) # find length of legal actions
        max_action = float('-inf') # initialize max_action
        qVal = None # initialize qVal
        
        if legalActionLen != 0: # while there are legal actions
            max_action = self.getPolicy(state) # set max action to best action of state
            qVal = self.getQValue(state, max_action) # calculate q value
            return qVal
        else:
            return 0.0 # no legal actions, terminal state, return 0.0
        
        #util.raiseNotDefined()

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"
        
        legalAction = self.getLegalActions(state) # initialize legal actions
        legalActionLen = len(legalAction) # find length of legal actions
        qValue = float('-inf') # initialize qValue to negative infinity
        qAction = None # initialize qAction to None
        currentQVal = None # initialize current q val
        
        if legalActionLen != 0: # while there are legal actions
            for actions in legalAction: # while action is legal
                currentQVal = self.getQValue(state, actions) #calculate q value
                if currentQVal == qValue:
                    qAction = random.choice((qAction, actions)) # random is better
                if currentQVal > qValue:
                    qValue = currentQVal # update qValue
                    qAction = actions # update qAction
            return qAction
        else:
            return None # no legal actions, terminal state, return None
        
        #util.raiseNotDefined()

    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        legalAction = self.getLegalActions(state) # get legal actions
        legalActionLen = len(legalAction) # find length of legal actions
        action = None
        "*** YOUR CODE HERE ***"
        
        if legalActionLen != 0: # while actions are legal
            if util.flipCoin(self.epsilon): # flip coin prob
                action = random.choice(legalAction) # random is better
            else:
                action = self.getPolicy(state) # update action
            return action
        else:
            return None # no legal actions, terminal state, return None
        
        #util.raiseNotDefined()

    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"
        
        qVal = self.values[(state,action)] # initialize qVal
        nextQVal = self.computeValueFromQValues(nextState) # initialize next qVal
        
        # update q val
        self.values[(state, action)] = (1 - self.alpha) * qVal + self.alpha * (reward + self.discount * nextQVal)
        
        #util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action


class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"
        
        featureVector = self.featExtractor.getFeatures(state, action) # featureVector for features
        qVal = 0 # initialize qVal for return
        
        for features in featureVector: # for features
            w = self.weights[features] # set w 
            qVal = qVal + (featureVector[features] * w) # use dot product w * featureVector
            
        return qVal # return Q(state, action)
        
        #util.raiseNotDefined()

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        "*** YOUR CODE HERE ***"
        
        featureVector = self.featExtractor.getFeatures(state, action) # featureVector for features
        qVal = self.getQValue(state, action) # set qVal
        qDifference = (reward + self.discount * self.getValue(nextState)- qVal) # calculate qDifference using discount
    
        for features in featureVector: # for features
            w = self.weights[features] # set w 
            # update w with features and qDifference
            self.weights[features] = (w + self.alpha * qDifference * featureVector[features])
        
        #util.raiseNotDefined()

    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            pass
