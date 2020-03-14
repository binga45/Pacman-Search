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
from util import PriorityQueue

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
    #print("Start:", problem.getStartState())
    node = problem.getStartState()
    if problem.isGoalState(problem.getStartState()): 
        return []
    explored = []
    frontier = util.Stack()
    frontier.push((node,[]))
    while True:
        if frontier.isEmpty(): return []
        node, path = frontier.pop()
        explored.append(node)
        if problem.isGoalState(node):
            return path
        successors = problem.getSuccessors(node)
        if successors:
            for successor,action, stepcost in successors:
                if successor not in explored:
                    #if  successor not in (state[0] for state in frontier.list) and problem.isGoalState(successor): return path+[action]
                    frontier.push((successor,path+[action]))
    #util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    node = problem.getStartState()
    if problem.isGoalState(problem.getStartState()): 
        return []
    explored = []
    frontier = util.Queue()
    frontier.push((node,[]))
    while True:
        if frontier.isEmpty(): return []
        node, path = frontier.pop()
        explored.append(node)
        if problem.isGoalState(node):
            return path
        successors = problem.getSuccessors(node)
        if successors:
            for successor,action, stepcost in successors:
                if successor not in explored and successor not in (state[0] for state in frontier.list):
                    #if  successor not in (state[0] for state in frontier.list) and problem.isGoalState(successor): return path+[action]
                    frontier.push((successor,path+[action]))
    #util.raiseNotDefined()

def iterativeDeepeningSearch(problem):
    """Search the tree iteratively for goal nodes."""
    "*** YOUR CODE HERE ***"
    cutoff = 0
    while True:
        node = problem.getStartState()
        if problem.isGoalState(problem.getStartState()): 
            return []
        explored = []
        frontier = util.Stack()
        frontier.push((node,[]))
        while True:
            if frontier.isEmpty(): break
            node, path = frontier.pop()
            explored.append(node)
            if problem.isGoalState(node):
                return path
            successors = problem.getSuccessors(node)
            if successors:
                for successor,action,stepcost in successors:
                    if successor not in explored and len(path)+1 <= cutoff and successor not in (state[0] for state in frontier.list):
                        #if problem.isGoalState(successor): return path+[action]
                        frontier.push((successor,path+[action]))
        cutoff +=1

    #util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    node = problem.getStartState()
    if problem.isGoalState(problem.getStartState()): 
        return []
    explored = []
    frontier = util.PriorityQueue()
    frontier.push((node,[]),0)
    while True:
        if frontier.isEmpty(): return []
        node, path = frontier.pop()
        explored.append(node)
        if problem.isGoalState(node):
            return path
        successors = problem.getSuccessors(node)
        if successors:
            for successor,action,stepcost in successors:
                if successor not in explored and successor not in (state[2][0] for state in frontier.heap):
                    #if  successor not in (state[0] for state in frontier.list) and problem.isGoalState(successor): return path+[action]
                    frontier.push((successor,path+[action]),problem.getCostOfActions(path+[action]))
                elif successor not in explored and (successor in (state[2][0] for state in frontier.heap)):
                    for state in frontier.heap:
                        if successor == state[2][0]:
                            oldPri = problem.getCostOfActions(state[2][1])
                    newPri = problem.getCostOfActions(path + [action])
                    # State is cheaper with his hew father -> update and fix parent #
                    if oldPri > newPri:
                        newPath = path + [action]
                        frontier.update((successor,newPath),newPri)
    #util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


class ExtendedPriorityQueueWithFunction(PriorityQueue):
    def  __init__(self, problem, priorityFunction):
        "priorityFunction (item) -> priority"
        self.priorityFunction = priorityFunction      # store the priority function
        PriorityQueue.__init__(self)        # super-class initializer
        self.problem = problem
    def push(self, item, heuristic):
        "Adds an item to the queue with priority from the priority function"
        PriorityQueue.push(self, item, self.priorityFunction(self.problem,item,heuristic))

def aStarSearch(problem, heuristic=nullHeuristic):
    "*** YOUR CODE HERE ***"
    cost = lambda problem, item,heuristic: problem.getCostOfActions(item[1])+heuristic(item[0],problem)
    frontier = ExtendedPriorityQueueWithFunction(problem, cost)
    explored = []
    node = problem.getStartState()
    if problem.isGoalState(problem.getStartState()): 
        return []
    frontier.push((problem.getStartState(),[]),heuristic)
    while True:
        if frontier.isEmpty(): return []
        node, path = frontier.pop()
        if node in explored:
            continue
        explored.append(node)
        if problem.isGoalState(node):
            return path
        successors = problem.getSuccessors(node)
        if successors:
            for successor,action,stepcost in successors:
                if successor not in explored:
                    newPath = path + [action]
                    frontier.push((successor,newPath),heuristic)
    #util.raiseNotDefined()
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
iddfs = iterativeDeepeningSearch