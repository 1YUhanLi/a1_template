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
from game import Actions
from game import Directions
from util import foodGridtoDic

import itertools
from itertools import product
from game import Grid
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

    util.raiseNotDefined()


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


def nullHeuristic(state, problem=None):
    """
    This heuristic is trivial.
    """
    return 0


def foodHeuristic(state, problem):
    """
    Your heuristic for the FoodSearchProblem goes here.

    This heuristic must be consistent to ensure correctness.  First, try to come
    up with an admissible heuristic; almost all admissible heuristics will be
    consistent as well.

    If using A* ever finds a solution that is worse uniform cost search finds,
    your heuristic is *not* consistent, and probably not admissible!  On the
    other hand, inadmissible or inconsistent heuristics may find optimal
    solutions, so be careful.

    The state is a tuple ( pacmanPosition, foodGrid ) where foodGrid is a Grid
    (see game.py) of either True or False. You can call foodGrid.asList() to get
    a list of food coordinates instead.

    If you want access to info like walls, capsules, etc., you can query the
    problem.  For example, problem.walls gives you a Grid of where the walls
    are.

    If you want to *store* information to be reused in other calls to the
    heuristic, there is a dictionary called problem.heuristicInfo that you can
    use. For example, if you only want to count the walls once and store that
    value, try: problem.heuristicInfo['wallCount'] = problem.walls.count()
    Subsequent calls to this heuristic can access
    problem.heuristicInfo['wallCount']
    """
    "*** YOUR CODE HERE for task1 ***"
     # Unpack the state into Pacman's position and the food grid.
    position, foodGrid = state
    # Convert the food grid into a list of food coordinates.
    foodList = foodGrid.asList()

    if not foodList:
        return 0

    # Initialize the distance to the closest food to infinity.
    distanceToClosestFood = float('inf')
    # Loop through each food item to find the distance from Pacman's position to the food.
    # Update distanceToClosestFood with the minimum of these distances.
    for food in foodList:
        distance = realdistance(position, food, problem)
        if distance < distanceToClosestFood:
            distanceToClosestFood = distance

    # Calculate the maximum distance between any two food points
    maxDistanceBetweenFoods = 0
    for food1 in foodList:
        for food2 in foodList:
            distance = realdistance(food1, food2, problem)
            if distance > maxDistanceBetweenFoods:
                maxDistanceBetweenFoods = distance
    
    if distanceToClosestFood == float('inf'):
        distanceToClosestFood = 0

    return maxDistanceBetweenFoods - distanceToClosestFood                                                               




    # comment the below line after you implement the algorithm
    util.raiseNotDefined()

def getfoodgrid(foodPosition, width, height):
    """
    Create a single-food grid based on the given position.
    """
    foodGrid = Grid(width, height, False)
    x, y = foodPosition
    # Set the grid cell at (x, y) to True, indicating food presence
    foodGrid[x][y] = True
    return foodGrid

def realdistance(startPosition, endPosition, problem):
        """
        Returns the real distance(not Manhattan Distance ) between two points, caching the result.
        """
        # Use cached distance if available
        key = (startPosition, endPosition)
        if key not in problem.heuristicInfo:
            singleFoodGrid = getfoodgrid(endPosition, problem.walls.width, problem.walls.height)
            singleFoodProblem = SingleFoodSearchProblem(pos=startPosition, food=singleFoodGrid, walls=problem.walls)
            # A* search to find the distance
            problem.heuristicInfo[key] = len(astar(singleFoodProblem))
        
        #Return the cached distance, defaulting to 0 if not found
        return problem.heuristicInfo.get(key, 0)
        


class MAPFProblem(SearchProblem):
    """
    A search problem associated with finding a path that collects all
    food (dots) in a Pacman game.

    A search state in this problem is a tuple ( pacmanPositions, foodGrid ) where
      pacmanPositions:  a dictionary {pacman_name: (x,y)} specifying Pacmans' positions
      foodGrid:         a Grid (see game.py) of either pacman_name or False, specifying the target food of that pacman_name. For example, foodGrid[x][y] == 'A' means pacman A's target food is at (x, y). Each pacman have exactly one target food at start
    """

    def __init__(self, startingGameState):
        "Initial function"
        "*** WARNING: DO NOT CHANGE!!! ***"
        self.start = (startingGameState.getPacmanPosition(), startingGameState.getFood())
        self.walls = startingGameState.getWalls()

    def getStartState(self):
        "Get start state"
        "*** WARNING: DO NOT CHANGE!!! ***"
        return self.start

    def isGoalState(self, state):
        "Return if the state is the goal state"
        "*** YOUR CODE HERE for task2 ***"
        # Extract pacmanPositions and foodGrid from the state
        pacmanPositions, foodGrid = state
        for name in pacmanPositions.keys():         
            for x in range(foodGrid.width):
                for y in range(foodGrid.height):
                    if foodGrid[x][y] == name:  # If food designated for a Pacman is found
                        return False  # Not all food has been consumed

    # Next, check if all cells are False, indicating no food left at all.
        for x in range(foodGrid.width):
            for y in range(foodGrid.height):
                if foodGrid[x][y] != False:  # If any cell is not False, food is present
                    return False  # Not all food has been consumed

    # If all designated food is consumed and no cell has food, the goal state is reached.
        return True

        
    

        # comment the below line after you implement the function
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
            Returns successor states, the actions they require, and a cost of 1.
            Input: search_state
            Output: a list of tuples (next_search_state, action_dict, 1)

            A search_state in this problem is a tuple consists of two dictionaries ( pacmanPositions, foodGrid ) where
              pacmanPositions:  a dictionary {pacman_name: (x,y)} specifying Pacmans' positions
              foodGrid:    a Grid (see game.py) of either pacman_name or False, specifying the target food of each pacman.

            An action_dict is {pacman_name: direction} specifying each pacman's move direction, where direction could be one of 5 possible directions in Directions (i.e. Direction.SOUTH, Direction.STOP etc)


        """
        "*** YOUR CODE HERE for task2 ***"
        # Initialize an empty list to hold successor states.
        successors = []
        pacmanPositions, foodGrid = state
        # Define possible directions a pacman can move.
        directions = [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST, Directions.STOP]
        # Initialize a dictionary to track possible movements for each pacman.
        movement = {pacman: [] for pacman in pacmanPositions}
        for pacman, pos in pacmanPositions.items():
                # Check each possible direction of movement.
                for direction in directions:
                    # Calculate the next position based on the current direction.
                    dx, dy = Actions.directionToVector(direction)
                    next_x, next_y = int(pos[0] + dx), int(pos[1] + dy)

                     # Check if the next position does not hit a wall.
                    if not self.walls[next_x][next_y]:
                        # If the move is valid, add it to the possible movements.
                        next_move = (next_x, next_y)
                        movement[pacman].append((direction, next_move))

        all_posible = list(product(*movement.values()))
        
        
        # Evaluate each combination of moves.
        for moves in all_posible:
            movement_dict = {}
            nextPositions = pacmanPositions.copy()
            next_FoodGrid = foodGrid.copy()
            # Create a reverse mapping from positions to pacman names.
            dic_mapping = {pos: pacman for pacman, pos in pacmanPositions.items()}
            is_swap = False
            
            # Check each move in the current combination.
            for pacman, (direction, next_move) in zip(pacmanPositions.keys(), moves):
                # Detect potential position swaps.
                if next_move in pacmanPositions.values() and dic_mapping[next_move] != pacman:
                    int_pos = pacmanPositions[pacman]
                    if pacmanPositions[dic_mapping[next_move]] == int_pos:
                        is_swap = True
                        break

                # Update the action and position for the current pacman.
                movement_dict[pacman] = direction
                if next_FoodGrid[next_move[0]][next_move[1]] == pacman:
                    # Consume the food at the new position, if applicable.
                    next_FoodGrid[next_move[0]][next_move[1]] = False
                nextPositions[pacman] = next_move

            # Add the new state to the successors list if no swap conflict was detected.
            if not is_swap:
                successors.append(((nextPositions, next_FoodGrid), movement_dict, 1))

        return successors
                
        # comment the below line after you implement the function
        util.raiseNotDefined()
    
    

    



def conflictBasedSearch(problem: MAPFProblem):
    """
        Conflict-based search algorithm.
        Input: MAPFProblem
        Output(IMPORTANT!!!): A dictionary stores the path for each pacman as a list {pacman_name: [action1, action2, ...]}.

    """
    "*** YOUR CODE HERE for task3 ***"
    


"###WARNING: Altering the following functions is STRICTLY PROHIBITED. Failure to comply may result in a grade of 0 for Assignment 1.###"
"###WARNING: Altering the following functions is STRICTLY PROHIBITED. Failure to comply may result in a grade of 0 for Assignment 1.###"
"###WARNING: Altering the following functions is STRICTLY PROHIBITED. Failure to comply may result in a grade of 0 for Assignment 1.###"


class FoodSearchProblem(SearchProblem):
    """
    A search problem associated with finding a path that collects all
    food (dots) in a Pacman game.

    A search state in this problem is a tuple ( pacmanPosition, foodGrid ) where
      pacmanPosition: a tuple (x,y) of integers specifying Pacman's position
      foodGrid:       a Grid (see game.py) of either True or False, specifying remaining food
    """

    def __init__(self, startingGameState):
        self.start = (startingGameState.getPacmanPosition(), startingGameState.getFood())
        self.walls = startingGameState.getWalls()
        self._expanded = 0  # DO NOT CHANGE
        self.heuristicInfo = {}  # A optional dictionary for the heuristic to store information

    def getStartState(self):
        return self.start

    def isGoalState(self, state):
        return state[1].count() == 0

    def getSuccessors(self, state):
        "Returns successor states, the actions they require, and a cost of 1."
        successors = []
        self._expanded += 1  # DO NOT CHANGE
        for direction in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST, Directions.STOP]:
            x, y = state[0]
            dx, dy = Actions.directionToVector(direction)
            next_x, next_y = int(x + dx), int(y + dy)
            if not self.walls[next_x][next_y]:
                nextFood = state[1].copy()
                nextFood[next_x][next_y] = False
                successors.append((((next_x, next_y), nextFood), direction, 1))
        return successors

    def getCostOfActions(self, actions):
        """Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return 999999"""
        x, y = self.getStartState()[0]
        cost = 0
        for action in actions:
            # figure out the next state and see whether it's legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]:
                return 999999
            cost += 1
        return cost


class SingleFoodSearchProblem(FoodSearchProblem):
    """
    A special food search problem with only one food and can be generated by passing pacman position, food grid (only one True value in the grid) and wall grid
    """

    def __init__(self, pos, food, walls):
        self.start = (pos, food)
        self.walls = walls
        self._expanded = 0  # DO NOT CHANGE
        self.heuristicInfo = {}  # A optional dictionary for the heuristic to store information


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    Q = util.Queue()
    startState = problem.getStartState()
    startNode = (startState, 0, [])
    Q.push(startNode)
    while not Q.isEmpty():
        node = Q.pop()
        state, cost, path = node
        if problem.isGoalState(state):
            return path
        for succ in problem.getSuccessors(state):
            succState, succAction, succCost = succ
            new_cost = cost + succCost
            newNode = (succState, new_cost, path + [succAction])
            Q.push(newNode)

    return None  # Goal not found


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    myPQ = util.PriorityQueue()
    startState = problem.getStartState()
    startNode = (startState, 0, [])
    myPQ.push(startNode, heuristic(startState, problem))
    best_g = dict()
    while not myPQ.isEmpty():
        node = myPQ.pop()
        state, cost, path = node
        if (not state in best_g) or (cost < best_g[state]):
            best_g[state] = cost
            if problem.isGoalState(state):
                return path
            for succ in problem.getSuccessors(state):
                succState, succAction, succCost = succ
                new_cost = cost + succCost
                newNode = (succState, new_cost, path + [succAction])
                myPQ.push(newNode, heuristic(succState, problem) + new_cost)

    return None  # Goal not found


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
cbs = conflictBasedSearch
