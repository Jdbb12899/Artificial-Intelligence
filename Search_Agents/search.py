# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
   
    visited = [] #keep track of visited nodes
    node = (problem.getStartState(), []) #initialize first node
    searchStack = util.Stack() #create stack for DFS (LIFO)
    searchStack.push(node) #begin at first node
    
    if (searchStack.isEmpty() == True): #exit with error if stack is empty
        exit("Stack is empty!")
    
    while (searchStack.isEmpty() != True): #while stack has stuff in it
        state, actionPath = searchStack.pop() #start with first state, action
        if state not in visited: #if we havent visited this state
            visited.append(state) #add to list
            if problem.isGoalState(state): #check if its the goal state
                return actionPath #if so, success!
            else:
                successor = problem.getSuccessors(state) #if not continue
                for nextState, nextAction, pathCost in successor: #check next nodes and iterate
                    searchStack.push((nextState, actionPath + [nextAction]))
                    
    return actionPath #return successful path to goal state
    
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    
    visited = [] #keep track of visited nodes
    node = (problem.getStartState(), [], 0) #initialize first node
    searchQueue = util.Queue() #create queue for BFS (FIFO)
    searchQueue.push(node) #begin at first node
    
    if (searchQueue.isEmpty() == True): #exit with error if queue is empty
        exit("Queue is empty!")
    
    while (searchQueue.isEmpty() != True): #while stack has stuff in it
        state, actionPath, cost = searchQueue.pop() #start with first state, action, and cost
        if state not in visited: #if we havent visited this state
            visited.append(state) #add to list
            if problem.isGoalState(state): #check if its the goal state
                return actionPath #if so, success!
            else:
                successor = problem.getSuccessors(state) #if not continue
                for nextState, nextAction, pathCost in successor: #check next nodes and iterate
                    searchQueue.push((nextState, actionPath + [nextAction], cost + pathCost)) #avoid visited states
                    
    return actionPath #return successful path to goal state
    
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    
    visited = [] #keep track of visited nodes
    node = (problem.getStartState(), [], 0) #initialize first node
    searchPriorityQueue = util.PriorityQueue() #create priority queue for UCS (FIFO w/ priority)
    searchPriorityQueue.push(node, 0) #begin at first node
    
    if (searchPriorityQueue.isEmpty() == True): #exit with error if queue is empty
        exit("Queue is empty!")
    
    while (searchPriorityQueue.isEmpty() != True): #while stack has stuff in it
        state, actionPath, cost = searchPriorityQueue.pop() #start with first state, action, and cost
        if (state not in visited): #if we havent visited this state
            visited.append(state) #add to list
            if problem.isGoalState(state): #check if its the goal state
                return actionPath #if so, success!
            else:
                successor = problem.getSuccessors(state) #if not continue
                for nextState, nextAction, pathCost in successor: #check next nodes and iterate
                    searchPriorityQueue.push((nextState, actionPath + [nextAction], cost + pathCost), cost + pathCost) #avoid visited states, priority taken into account
                    
    return actionPath #return successful path to goal state
    
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    
    visited = [] #keep track of visited nodes
    node = (problem.getStartState(), [], 0) #initialize first node
    searchPriorityQueue = util.PriorityQueue() #create priority queue for UCS (FIFO w/ priority)
    searchPriorityQueue.push((node), nullHeuristic(problem.getStartState(), problem)) #begin at first node
    
    if (searchPriorityQueue.isEmpty() == True): #exit with error if queue is empty
        exit("Queue is empty!")
        
    while (searchPriorityQueue.isEmpty() != True): #while stack has stuff in it
        state, actionPath, cost = searchPriorityQueue.pop() #start with first state, action, and cost
        if (state not in visited): #if we havent visited this state
            visited.append(state) #add to list
            if problem.isGoalState(state): #check if its the goal state
                return actionPath #if so, success!
            else:
                successor = problem.getSuccessors(state) #if not continue
                for nextState, nextAction, pathCost in successor: #check next nodes and iterate
                    searchPriorityQueue.push((nextState, actionPath + [nextAction], cost + pathCost), (cost + pathCost) + heuristic(nextState, problem)) #avoid visited states, priority and heuristic taken into account
                    
    return actionPath #return successful path to goal state
    
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
